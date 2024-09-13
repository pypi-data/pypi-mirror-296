import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import joblib


class DataModule(nn.Module):
    def __init__(self, hparam):
        super(DataModule, self).__init__()
        self.hparam = hparam

    def load_data(self):
        data = pd.read_csv(self.hparam['DATA_DIR'])
        return data

    def augment_ds(self, ds, n_add_samples=50, categorical_channels=[], noise_fraction=0.1):
        '''As we are dealing with full- or partial factorial designs of experiment, we can augment data by
        adding a statistical noise.'''

        categorical_channels = [col for col in categorical_channels if col in ds.columns]
        categorical_df = ds[categorical_channels]
        numerical_df = ds.drop(columns=categorical_channels)

        std_devs = numerical_df.std()
        augmented_data = []

        for _ in range(n_add_samples):
            sample = numerical_df.sample(n=1)

            noise = noise_fraction * pd.Series(np.random.randn(*sample.shape).reshape(-1))  #* std_devs
            noisy_sample = sample + noise.values

            if not categorical_df.empty:
                original_categorical_sample = categorical_df.loc[sample.index]
                augmented_sample = pd.concat([original_categorical_sample.reset_index(drop=True), noisy_sample.reset_index(drop=True)], axis=1)
            else:
                augmented_sample = noisy_sample.reset_index(drop=True)
            augmented_data.append(augmented_sample)

        augmented_df = pd.concat(augmented_data, ignore_index=True)
        augmented_ds = pd.concat([ds, augmented_df], ignore_index=True)
        return augmented_ds

    def to_tensor(self, ds):
        ds = torch.tensor(ds, dtype=torch.float32)
        return ds

    def scaler(self, ds):
        Scaler = StandardScaler()
        ds = Scaler.fit_transform(ds)

        joblib.dump(Scaler, filename=self.hparam['LOG_DIR'] + '/scaler.gz')
        return ds

    def sampler(self, ds):
        train_size = int(0.6 * len(ds))
        val_size = int(0.2 * len(ds))
        test_size = len(ds) - train_size - val_size

        indices = torch.randperm(len(ds))
        train_indices = indices[:train_size]
        val_indices = indices[train_size:train_size + val_size]
        test_indices = indices[train_size + val_size:]

        ds_train, ds_val, ds_test = ds[train_indices], ds[val_indices], ds[test_indices]
        return ds_train, ds_val, ds_test

    def init_dataloader(self, ds, batch_size=1, shuffle=False):
        return DataLoader(ds, batch_size=batch_size, num_workers=0, shuffle=shuffle, drop_last=True, pin_memory=True)




