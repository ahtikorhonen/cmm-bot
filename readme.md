A single threaded asynchronous crypto market making bot for Bybit spot instruments.

Features:
* maintains two real time order books for a certain instrument through websocket connections
* calculates a fair value estimate based on the order book states
* calculates a spread based on the past volume
* skews quotes based on current inventory
* sends quotes via Bybit API