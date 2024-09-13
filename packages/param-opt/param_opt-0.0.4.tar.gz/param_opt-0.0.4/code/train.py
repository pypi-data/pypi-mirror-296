# Xavier initialisation is a method used to initialise the weights of neural networks, particularly
# for layers using activation functions like sigmoid or tanh.
# The goal of Xavier initialisation is to maintain the variance of the input and output of each layer in the network,
# thereby preventing the vanishing or exploding gradient problems that can occur during training.
# By scaling the weights inversely proportional to the square root of the number of input and output neurons, the input
# snd output variance are kept roughly the same, which helps stabilising the training process

# TensorBoard is a powerful visualization tool provided by TensorFlow and commonly used with PyTorch to monitor
# and log various aspects of your machine learning experiments. It allows you to track metrics, visualize the
# computation graph, display images, and more, making it easier to debug and optimize your models.

# Garbage collection (GC) is a form of automatic memory management used in programming languages and environments
# like Python. The purpose of garbage collection is to reclaim memory that is no longer in use by the program,
# thus preventing memory leaks and ensuring efficient use of system resources.

import gc #import garbage collection
import math #import math for mathematical operations
import random #import random for generating random number
import numpy as np #import numpy for numerical operations
from tqdm import tqdm #import tqdm for progress bars
import torch #import torch for deep learning opeartions
import torch.nn as nn #import torch.nn for neural network components
from torch.utils.tensorboard import SummaryWriter #import tensorboard for logging

from model.net import Net, save_model #import custom model and save function
from dataloader import get_tuk_dataloaders, get_ctc_dataloaders, get_haw_dataloaders #import custom dataloaders

class TrainModel():
    def __init__(self, hparam):
        # initialise the training process with the given hyperparameters
        # hparam: dictionary containing hyperparameters for the model
        self.hparam = hparam #store the hyperparameters
        #start the training process and retrieve the model and validation loss
        self.model, self.loss_val = self.training(hparam)

    @staticmethod
    def init_weights(m):
        # initialise weights for the neural network layers using xavier initialisation
        # m: a layer of the neural network
        if type(m) == nn.Linear: #apply only to linear layers
            torch.nn.init.xavier_uniform_(m.weight) # xavier uniform initialisation for weights
            m.bias.data.fill_(0.01) # initialise biases to 0.01

    def train_step(self, dl_train, model, optimizer, device):
        # perform one training step over the training data
        model.train() #set the model to training mode
        total_loss = 0.0 #initialise the total loss
        for x, y in dl_train: #iterate over the training data loader
            optimizer.zero_grad() #clear gradients
            x, y = x.to(device), y.to(device) #move data to the appropriate device

            y_hat = model(x) #forward pass through the model
            loss = nn.functional.mse_loss(y_hat, y) #compute mean squared error loss

            loss.backward() #backpropagation
            optimizer.step() #optimisation of model weights
            total_loss += loss.item() #accumulate the total loss
        return total_loss / len(dl_train) #return the average training loss

    def val_step(self, dl_val, model, device):
        # perform one validation step over the validation data
        model.eval() #set the model to evaluation mode
        total_loss = 0.0 #initialise the total loss
        with torch.no_grad(): #disable gradient computation
            for x, y in dl_val: #iterate over the validation data loader
                x, y = x.to(device), y.to(device) #move data to appropriate device

                y_hat = model(x) #forwards pass through the model
                loss = nn.functional.mse_loss(y_hat, y) #compute mean squared error loss
                total_loss += loss.item() #accumulate the total loss
        return total_loss / len(dl_val) #return the average validation

    def training(self, hparam):
        #main training loop for the model
        random.seed(hparam['SEED']) #set the random seed for reproducibility
        np.random.seed(hparam['SEED']) # set the numpy random seed
        torch.manual_seed(hparam['SEED']) #set the torch random seed
        logger = SummaryWriter(log_dir=hparam['LOG_DIR']) #set up tensor board logger

        # select the appropriate dataloader based on dataset
        if 'tuk' in hparam['DATA_DIR']:
            dl_train, dl_val, dl_test = get_tuk_dataloaders(hparam)
        elif 'ctc' in hparam['DATA_DIR']:
            dl_train, dl_val, dl_test = get_ctc_dataloaders(hparam)
        elif 'haw' in hparam['DATA_DIR']:
            dl_train, dl_val, dl_test = get_haw_dataloaders(hparam)

        #device = 'cuda' if torch.cuda.is_available() else 'cpu'
        device = 'cpu' # change to 'cuda' if using gpu
        model = Net(input_dim=hparam['INPUT_DIM'], hidden_dim=hparam['HIDDEN_DIM'], output_dim=hparam['OUTPUT_DIM'], \
                    n_layers=hparam['N_LAYERS'], dropout=hparam['DROPOUT'])
        #initialise the model
        model.apply(self.init_weights) #initialise the model weights
        model.to(device) #move model to appropriate device

        optimizer = torch.optim.Adam(model.parameters(), lr=hparam['LR'], weight_decay=hparam['WEIGHT_DECAY']) #setup optimiser

        print(hparam, "\n\n") #print hyperparameters
        print(f"**********************************************************************\n"
              f"Model structure: {model}\n") #print model structure
        print(f"Number of parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad)}") #print number of trainable parameters
        print("***********************************************************************\n")

        with tqdm(range(hparam["MAX_EPOCHS"]), unit="epoch") as tepoch: #progress bar for epochs
            for e in tepoch: #iterate over epochs
                l_train = self.train_step(dl_train, model, optimizer, device) #perform a training step
                logger.add_scalar('train loss', l_train, e) # log training loss
                if math.isnan(l_train): #check for NaN values
                    break #exit if NaN is encountered

                if e % 50 == 0 and e != 0: #every 50 epochs validate the model
                    l_val = self.val_step(dl_val, model, device) #perform a validation step
                    tepoch.set_postfix(loss_train=l_train, loss_val=l_val) #update progress bar with losses
                    logger.add_scalar('val loss', l_val, e) #log validation loss
                else:
                    tepoch.set_postfix(loss_train=l_train) #update progress bar with training loss only
            l_test = self.val_step(dl_test, model, device) #final test step after training

        save_model(model=model, path=hparam['LOG_DIR']) #save the trained model
        gc.collect() #perform garbage collection
        torch.cuda.empty_cache() #clear cuda cache if used
        logger.close() #close the tensorboard logger

        print(f'\ntrain loss: {l_train}\nval loss: {l_val}\ntest loss: {l_test}') #print final loss
        return model, l_val #return the trained model and validation loss


if __name__ == '__main__':
    #define hyperparameters for training
    hparam = {
        "SEED": 42,
        "DATA_DIR": "../data/tuk/usw.csv",
        "LOG_DIR": "../exp/exp_tuk",
        "N_AUG_SAMPLES": 200,
        "BATCH_SIZE": 16,
        "SPLIT_LOC": 5,

        "INPUT_DIM": 3,
        "HIDDEN_DIM": 64,
        "OUTPUT_DIM": 1,
        "N_LAYERS": 5,
        "DROPOUT": 0.1,

        "MAX_EPOCHS": 5000,
        "LR": 0.005,
        "WEIGHT_DECAY": 0.0001,

        "OPT_LR": 0.5,
        "OPT_EPOCHS": 150,
        "OPT_ENSEMBLE": 1
    }

    training = TrainModel(hparam=hparam) # Instantiate and run the training process
