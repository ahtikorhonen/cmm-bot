TESTNET = True

# Base endpoints
WS_ENDPOINT = "wss://stream.bybit.com/v5/public/linear"
INSTRUMENT_INFO = "/v5/market/instruments-info?category=linear&symbol={symbol}"

# Position endpoints
OPEN_ORDERS = "/v5/order/realtime"
CURRENT_POSITION = "/v5/position/list"
CLOSED_PNL = "/v5/position/closed-pnl"
WALLET_BALANCE = "/v5/account/wallet-balance"

# Order endpoints
CREATE_ORDER = "/v5/order/create"
AMEND_ORDER = "/v5/order/amend"
CANCEL_SINGLE = "/v5/order/cancel"
CANCEL_ALL = "/v5/order/cancel-all"