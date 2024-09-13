import torch
import torch.nn as nn


class Net(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, n_layers, dropout):
        super(Net, self).__init__()

        act = nn.ReLU() # nn.Tanh() # nn.Sigmoid()

        self.net = nn.Sequential()
        for layer in range(n_layers - 1):
            if layer == 0:
                self.net.add_module('layer_{}'.format(layer), nn.Linear(input_dim, hidden_dim))
            else:
                self.net.add_module('layer_{}'.format(layer), nn.Linear(hidden_dim, hidden_dim))
            self.net.add_module('activation_{}'.format(layer), act)
            self.net.add_module('dropout_{}'.format(layer), nn.Dropout(dropout))
        self.net.add_module('layer_{}' .format(n_layers), nn.Linear(hidden_dim, output_dim))

    def forward(self, x):
        return self.net(x)


def save_model(model, path):
    torch.save(model.state_dict(), path + '/model.pth')
    print(f'model saved under {path}/model.pth')


def load_model(hparam):
    model = Net(input_dim=hparam['INPUT_DIM'], hidden_dim=hparam['HIDDEN_DIM'], output_dim=hparam['OUTPUT_DIM'], \
                n_layers=hparam['N_LAYERS'], dropout=hparam['DROPOUT'])
    model.load_state_dict(torch.load(hparam['LOG_DIR'] + '/model.pth'))
    return model

