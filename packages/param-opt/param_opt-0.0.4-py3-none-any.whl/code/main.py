# Hyperparameters are configuration settings used to control the training process of machine
# learning models. Unlike model parameters, which are learned during training (e.g., weights
# in a neural network), hyperparameters are set before the training process begins and remain
# constant throughout. They play a crucial role in determining the performance and efficiency
# of the model.

# Dropout is a regularization technique used in neural networks to prevent overfitting. Overfitting
# occurs when a model learns not only the underlying pattern in the training data but also the noise,
# leading to poor generalization to new, unseen data. During training, dropout works by randomly “dropping
# out” a fraction of the neurons in a layer, meaning those neurons are temporarily removed from the network,
# along with all their incoming and outgoing connections. This is done independently for each training example
# and each forward pass. By randomly dropping neurons, dropout forces the network to learn redundant
# representations of the data, thus reducing the reliance on specific neurons and making the model more robust.

# Parallel workers refer to multiple computational units (such as CPU cores or GPU units) that work simultaneously
# to perform tasks more efficiently. In the context of machine learning and hyperparameter optimization, parallel
# workers can be used to speed up the process by running multiple experiments or training sessions concurrently.

import random #for settig random seed
import optuna #for hyperparameter optimisation
import json #for reading and writing JSON files
import multiprocessing #for parallel processing
import os #for interacting with the operating system
import numpy as np #for numerical operations on arrays
import torch #for deep learning operations

from train import TrainModel #custom training program for other file
from model import load_model #custom program for loading
from opt import ReconstructParams #import for parameter reconstruction
from utils import * #import all utility functions

class HparamSearch:
    def __init__(self, hparam):
        self.hparam = hparam #store the provided hyperparameters
        self.study_dir = hparam['LOG_DIR'] #directory where study logs and results will be saved

        # Ensure the directory exists
        if not os.path.exists(self.study_dir):
            os.makedirs(self.study_dir) #create directory if it does not exist

        # set random seeds for reproducibility
        random.seed(hparam['SEED']) #seed the random number generator
        np.random.seed(hparam['SEED']) #seed the NumPy random number generator
        torch.manual_seed(hparam['SEED']) #seed the Pytorch random number generator
        torch.cuda.manual_seed(hparam['SEED']) #seed the CUDA random number generator

        db_file = 'hparam_studies.db' #name of the SQLite database file
        db_path = os.path.join(self.hparam['STUDY_DIR'], db_file) #full path to the database file

        # create or load an Optuna study for hyperparameter optimisation
        self.study = optuna.create_study(direction='minimize', storage='sqlite:///' + db_path, study_name=hparam['ID'], load_if_exists=True)

    def experimental_run(self, trial):
        # setup trial-specific parameters
        trial_id = self.hparam['ID'] + '_exp_' + str(trial.number) #unique ID for each trial
        trial_log_dir = os.path.join(self.study_dir, trial_id) #Directory for trial specific logs

        trial_hparam = self.hparam.copy() #create a copy of the hyperparameters
        trial_hparam['ID'] = trial_id #update the ID for this trial
        trial_hparam['LOG_DIR'] = trial_log_dir #update the log directory for this trial

        trial_hparam['MAX_EPOCHS'] = trial.suggest_int('max_epochs', 1000, 5000, step=100) #number of epochs
        trial_hparam['N_LAYERS'] = trial.suggest_int('n_layers', 3, 10) #number of layers
        trial_hparam['HIDDEN_DIM'] = trial.suggest_int('hidden_dim', 8, 128) #size of each layer
        trial_hparam['DROPOUT'] = trial.suggest_float('dropout', 0.0, 0.2, step=0.01) #dropout rate
        trial_hparam['LR'] = trial.suggest_float('lr', 0.001, 0.01, step=0.001) #learning rate

        # setting up pipeline / setting up and training the model with the suggested hyperparameters
        try:
            criterion = TrainModel(hparam=trial_hparam).loss_val #train the model and obtain the loss value
        except Exception as e:
            print(f"Error during trial {trial.number}: {e}") #print error message if training fails
            criterion = float('inf') #set the loss to infinity if an error occurs
        return criterion #return the loss value for the trial

    def optimize_study(self, n_trials=32, n_workers=4):
        with multiprocessing.Pool(n_workers) as pool: #optimise the study using multiprocessing
            pool.map(self.worker_function, [n_trials // n_workers] * n_workers) #distribute trials across workers

    def worker_function(self, n_trials): #optimise the study for a given number of trials
        self.study.optimize(self.experimental_run, n_trials=n_trials) #run the optimisation

def single_training(hparam):
    training = TrainModel(hparam=hparam) #initialise and train the model with the given hyperparameters
    model = training.model #retrieve the trained model
    print('Training finished') #print message when training is done
    return model #return the trained model

def single_reconstruction(hparam, model, create_gif=True):
    if model is None: model = load_model(hparam)
    ensemble = hparam['OPT_ENSEMBLE'] if hparam['OPT_ENSEMBLE'] > 1 else False #load the model if not provided

    reconstruction = ReconstructParams(hparam=hparam, model=model) #initialise the recunstruction process

    if 'tuk' in hparam['LOG_DIR']:
        x_gt, y_gt = np.array([[2000., 300., 100.]]), np.array([[1029.22]]) #ground thruth values
        x, y = np.array([[2000.,0.,0.]]), np.array([[1000.]]) #initial values
        rec_vars = [False, True, True] #variables to be optimised

    elif 'ctc/rect' in hparam['LOG_DIR']:
        x_gt, y_gt = np.array([[500, 68, 16, 500, 16, 0]]), np.array([[14027.50]])
        x, y = np.array([[0, 0, 0, 0, 0, 0]]), np.array([[14000]])
        rec_vars = [True, True, True, True, True, True]

    elif 'ctc/round' in hparam['LOG_DIR']:
        x_gt, y_gt = np.array([[1000, 80, 5, 800, 5, 0, 1]]), np.array([[5231.36]])
        x, y = np.array([[1000, 80, 5, 0, 5, 0, 1]]), np.array([[5230]])
        rec_vars = [False, False, False, True, False, False, False]
    # transform input and ground truth values
    x, y = xy_transform(hparam, x, y)
    x_gt, y_gt = xy_transform(hparam, x_gt, y_gt)

    # convert to tensors
    x, y, x_gt, y_gt = to_tensor(x), to_tensor(y), to_tensor(x_gt), to_tensor(y_gt)

    # perform parameter reconstruction
    x_rec, x_loss, y_loss = reconstruction.find_params(
        x=x, y=y, x_gt=x_gt, y_gt=y_gt, #inputs and ground thruths
        autodiff=rec_vars, ensemble=ensemble, #reconstruction settings
        create_gif=create_gif #wether to create a GIF of the reconstruction process
    )

    if create_gif: make_gif(hparam=hparam) #create GIF if requested
    print('Reconstruction finished.') #print message when reconstruction is finisehd

def single_training_and_reconstruction(hparam, create_gif=True):
    model = single_training(hparam) #train the model
    single_reconstruction(hparam, model, create_gif=create_gif) #perform reconstruction with the trained model
    return

if __name__ == '__main__':

    hparam = {
        "ID": "tuk",
        "SEED": 42,
        "DATA_DIR": "../data/tuk/usw.csv",
        "STUDY_DIR": "../exp",
        "LOG_DIR": "../exp/exp_tuk",
        "N_AUG_SAMPLES": 200,
        "BATCH_SIZE": 16,
        "SPLIT_LOC": 3,

        "INPUT_DIM": 3,
        "HIDDEN_DIM": 64,
        "OUTPUT_DIM": 1,
        "N_LAYERS": 5,
        "DROPOUT": 0.1,

        "MAX_EPOCHS": 5000,
        "LR": 0.005,
        "WEIGHT_DECAY": 0.0001,

        "OPT_LR": 0.5,
        "OPT_EPOCHS": 1, #150,
        "OPT_ENSEMBLE": 1
    }
    
    # model = single_training(hparam)

    model = None
    single_reconstruction(hparam, model, create_gif=True)
    
    #single_training_and_reconstruction(hparam, create_gif=False)


    """

    hparam_list = json.load(open('../exp/hparams/hparams.json')) #load list of hyperparameters from JSON file
    for i in hparam_list:
        hs = HparamSearch(hparam=hparam_list[i]) #initialise HparamSearch for each set of hyperparameters 
        n_workers = 10 #number of parallel workers
        n_trials = 64

        hs.optimize_study(n_trials=n_trials, n_workers=n_workers)
    """
def Test(a):
    print(f"Import klappt{a}")