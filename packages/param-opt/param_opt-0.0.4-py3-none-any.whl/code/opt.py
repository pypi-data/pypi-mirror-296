from model import * #import all classes and models from the model module
from utils import * #import all utility functions
from tqdm import tqdm #import tqdm for creating progress bars

class ReconstructParams():
    def __init__(self, hparam, model):
        self.hparam = hparam #store the provided hyperparameters
        self.optimizer = None #placeholder for the optimizer
        self.loss = nn.MSELoss() #mean squared error loss function

        #load the model if not provided, otherwise use the provided model
        self.model = load_model(hparam) if model is None else model

    def init_autodiff_vars(self, input, autodiff):
        #split the input tensor along the first dimension
        split_input = torch.split(tensor=input, split_size_or_sections=1, dim=0)

        t_list = []
        for t, i in zip(split_input, autodiff):
            t.requires_grad_(i) #set requires_grad based on the autodiff
            t_list.append(t) #append the tensor to the list
        return t_list #return the list of tensors

    def get_best_rec(self, res_dict):
        # find the key corresponding to the minimum loss_y in the dictionary
        min_key = min(res_dict, key=lambda k: res_dict[k]['loss_y'])
        return res_dict[min_key]['x_rec'], res_dict[min_key]['loss_x'], res_dict[min_key]['loss_y']

    def reconstruct(self, x_list, y, x_gt, y_gt, create_gif=False):
        #concatenate the list of tensors into a single tensor along the first dimension
        x_rec = torch.cat(x_list, dim=0)
        x_guess = torch.clone(x_rec).detach() #clone and detach x_rec to create x_guess
        x_gt = x_gt.detach() # detach x_gt to ensure it doesnt require gradients

        y_guess = y #set y_guess as the target output
        y_gt = y_gt #ground truth output remains the same

        with tqdm(range(self.hparam['OPT_EPOCHS']), unit='epoch') as tepoch:
            for e in tepoch:
                self.optimizer.zero_grad() #reset gradients
                x_rec = torch.cat(x_list, dim=0) # x_list gets updated, by the optimizer.
                # reconstruct x by concatenating the tensors
                y_hat = self.model(x_rec) #predict the output using the model

                loss_y = self.loss(y_guess, y_hat) #calculate the loss
                loss_y.backward() # backpropagate the loss
                self.optimizer.step() #update the parameters

                if create_gif:
                    #plot the reconstruction process if create_gif is True
                    plot_reconstruction(
                        hparam=self.hparam,
                        x_gt=x_gt, x_guess=x_guess, x_rec=x_rec, y_gt=y_gt,
                        y_guess=y_guess, y_rec=y_hat, epoch=e
                    )
        loss_x = self.loss(x_guess, x_rec)
        #calculate the loss between the guess and the reconstructed x

        #TODO remove plot function here
        plot_optimization_surface(hparam=self.hparam, model=self.model, x_rec=x_gt)
        #plot the optimisation surface (optional, based on TODO)
        return x_rec.detach().cpu(), loss_x.detach().cpu().item(), loss_y.detach().cpu().item()
        #return the final reconstructed tensor and losses
    def reconstruct_with_ensemble(self, x_list, y, x_gt, y_gt):
        rec_dict = {} #dictionary to store results of each ensemble run

        for m in range(self.hparam['OPT_ENSEMBLE']):
            torch.manual_seed(m) #set the manual seed for reproducibility
            x, loss_x, loss_y = self.reconstruct(x_list=x_list, y=y, x_gt=x_gt, y_gt=y_gt, create_gif=False)
            rec_dict[m] = {'x_rec': x, 'loss_x': loss_x, 'loss_y': loss_y}
            #store results

        for elem in rec_dict:
            print(rec_dict[elem]) #print each result in the dictionary

        #get the best reconstruction based on the lowest loss_y
        x_rec, loss_x, loss_y = self.get_best_rec(rec_dict)
        return x_rec, loss_x, loss_y #return the best reconstructed tensor and corresponding losses

    def find_params(self, x, y, x_gt, y_gt, autodiff, ensemble=True, create_gif=False):
        #device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # clone the input tensor to create an initial guess
        x_guess = torch.clone(x)
        # initialise autodiff variables (tensor with gradients)
        x_prep_list = self.init_autodiff_vars(input=x, autodiff=autodiff)
        # initialise the optimiser with the specified learning rate
        self.optimizer = torch.optim.Adam(x_prep_list, lr=self.hparam['OPT_LR']) # TODO check for opt params

        if ensemble:
            #perform reconstruction using the ensemble method
            x, loss_x, loss_y = self.reconstruct_with_ensemble(x_list=x_prep_list, y=y, x_gt=x_gt, y_gt=y_gt)
        else:
            # perform single reconstruction
            x, loss_x, loss_y = self.reconstruct(x_list=x_prep_list, y=y, x_gt=x_gt, y_gt=y_gt, create_gif=create_gif)

        print(f'\nreconstruction results')
        print(f'x_assumption: {x_guess.numpy().tolist()}\nx_reconstruction: {x.numpy().tolist()}\nloss_x_reconstruction: {loss_x}\nloss_y_reconstruction: {loss_y}')
        return x, loss_x, loss_y # return the reconstructed tensor and losses


if __name__ == '__main__':
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
    # initialise the reconstructParams class with the provided hyperparameters
    reconstruction = ReconstructParams(hparam=hparam, model=None)
    #example input and output tensors
    x = torch.tensor([1000,200,0], dtype=torch.float32)
    y = torch.tensor([1000], dtype=torch.float32)
    rec_vars = [False, False, True]
    x_rec, x_loss, y_loss = reconstruction.find_params(x=x, y=y, autodiff=rec_vars, ensemble=False, create_gif=True)
    make_gif(hparam=hparam)
