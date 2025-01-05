A single threaded asynchronous crypto market making bot for Bybit perpetual contracts.
To run the bot create Bybit API key and secret and compile the cython function(s) by running
"python setup.py build_ext --inplace" in the parent directory.

Features:
* maintains two real time order books for a certain instrument through websocket connections
* calculates a fair value estimate based on the current order book states
* calculates a spread based on short-term volatility
* skews quotes based on current inventory
* sends quotes via Bybit API

TODO:
* implement bybit private and public APIs
* add logging
* calculate skew based on inventory
* parse websocket messages with cython [X]

Improvement Ideas:
* Implement exchange data feeds with picows for higher performance
  https://picows.readthedocs.io/en/latest