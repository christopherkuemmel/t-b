# -*- coding: utf-8 -*-
# Copyright 2022 Christopher Kümmel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This module contains code for creating Crypto Candle Datasets."""
import numpy as np
import pandas as pd
from torch.utils.data import Dataset


class CryptoCandleDataset(Dataset):
    """Crypto Candle Dataset Reader"""

    def __init__(self,
                 crypto_df: pd.DataFrame,
                 history_seq_len: int,
                 mapping: list,
                 transform: callable = None):
        """
        Args:
            crypto_df (pd.DataFrame): The DataFrame containing the crypto data.
            history_seq_len (int): Whether to include historical data. e.g.
                the last N timesteps. This will modify the output shape!
            mapping (list(str)): A list of strings referencing the columns in
                the DataFrame, which should be returned by calling an item.
                This will modify the output shape!
            transform (callable): Transforms to apply to the dataset or batch.

        Output shape of getting on item is:
            [(batch_size), history_seq_len, len(mapping)]
        """
        # mapping = ['open', 'high', 'low', 'close', 'volume']
        self.mapping = mapping
        self.history_seq_len = history_seq_len
        self.crypto_df = crypto_df
        self.transform = transform

    def __len__(self) -> int:
        """Computes the lenght of the dataset."""
        return len(self.crypto_df) - self.history_seq_len

    def __getitem__(self, idx: int) -> np.array:
        """Retrieves a specific item of the dataset.

        Args:
            idx (int): Index of specific element of the dataset.

        Returns:
            element (np.array): numpy array with the specific column mapped
                values, including N timestaps of historical data.
                Output shape of item is:
                    [history_seq_len, len(mapping)]

        Raises:
            IndexError: If index is out of range on the dataset.
        """
        item = self.crypto_df.iloc[
            idx:idx + self.history_seq_len].loc[:, self.mapping].to_numpy()

        if self.transform:
            item = self.transform(item)

        return item
