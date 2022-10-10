# t&b

Transformers and Blockchain
## Table of Contents

- [t&b](#tb)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
    - [Downloading Crypto Data](#downloading-crypto-data)
    - [Iterate Crypto Data](#iterate-crypto-data)
  - [Contributing](#contributing)
  - [Credits](#credits)
  - [License](#license)

## Getting Started

### Installation

1. `pip install -r requirements.txt`

### Downloading Crypto Data

```python
from tnb.data.cryptodatarequest import CryptoDataRequest

currency = 'BTC/USDT'
exchange ='BTC/USDT'
start_date = 1495032490  # miliseconds from epoch
end_date = 1652798890  # miliseconds from epoch

cdr = CryptoDataRequest()
crypto_df = cdr.request(currency, exchange, start_date, end_date)
```
### Iterate Crypto Data

```python
crypto_data = pd.read_csv('crypto_data.csv')

loader_params = {
  'batch_size': 1,
  'shuffle': False,
}

historical_seq_len = 50
mapping = ['open', 'high', 'low', 'close', 'amount']

ccd = CryptoCandleDataset(crypto_data, historical_seq_len, mapping)
train_loader = DataLoader(ccd, **loader_params)

for step, batch in enumerate(train_loader):
    # TODO: do your thing!
```
## Contributing

## Credits

## License

Copyright 2022 Christopher Kümmel

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.