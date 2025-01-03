A single threaded asynchronous crypto market making bot for Bybit perpetual contracts.

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
* parse websocket messages with cython