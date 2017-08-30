<h1>bittrex_v2</h1>

Bittrex V2 API wrapper for Python3. The API version is currently in beta (some endpoints may be fallen, see Testing section below). Inspired in [platelminto](https://github.com/platelminto) [java wrapper](https://github.com/platelminto/java-bittrex-2).

### Installation

Install bittrex_v2 by running:

    git clone https://github.com/mondeja/bittrex_v2.git
    cd bittrex_v2
    python setup.py install

### Testing
Bittrex API v2 is currently in beta version, so that certain endpoints may be fallen. Execute `tests.py` for check all. 

For test private commands methods you must provide key and secret in `secrets.json` file. For test `get_order(<uuid>)` method, you must provide a close order uuid in CONFIGURATION SECTION (`tests.py`).

________________________________

### Development progress:

|**Method**|**Developed**|**Documented**|**Tested**|
|:-------------------------|:-:|:-:|:-:|
|**PUBLIC COMMANDS**                   |
|`get_market_summary`      | ✔ | ✘ | ✔ |
|`get_market_summaries`    | ✔ | ✘ | ✔ |
|`get_currencies`          | ✔ | ✘ | ✔ |
|`get_wallet_health`       | ✔ | ✘ | ✔ |
|`get_market_orderbook`    | ✔ | ✘ | ✔ |
|`get_ticks`               | ✔ | ✘ | ✔ |
|**PRIVATE COMMANDS**                  |
|`get_order`               | ✔ | ✘ | ✔ |
|`get_open_orders`         | ✔ | ✘ | ✔ |
|`get_order_history`       | ✔ | ✘ | ✔ |
|`get_balance`             | ✔ | ✘ | ✔ |
|`cancel`                  | ✔ | ✘ | ✔ |
|`withdraw`                | ✔ | ✘ | ✔ |
|`place_order`             | ✔ | ✘ | ✘ |
|`get_withdrawal_history`  | ✔ | ✘ | ✔ |
|`get_deposit_history`     | ✔ | ✘ | ✔ |
|`get_pending_deposits`    | ✔ | ✘ | ✔ |
|`get_deposit_address`     | ✔ | ✘ | ✔ |
|`generate_deposit_address`| ✔ | ✘ | ✔ |

____________________________________

#### Contribute

- Issue Tracker: github.com/mondeja/bittrex_v2/issues
- Source Code: github.com/mondeja/bittrex_v2

#### Support

If you are having issues, please let me know (mondejar1994@gmail.com).

#### License

Copyright (c) 2017 Álvaro Mondéjar Rubio <mondejar1994@gmail.com>.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation, advertising
materials, and other materials related to such distribution and use
acknowledge that the software was developed by Álvaro Mondéjar Rubio. The
name of the Álvaro Mondéjar Rubio may not be used to endorse or promote
products derived from this software without specific prior written
permission.

THIS SOFTWARE IS PROVIDED “AS IS” AND WITHOUT ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


