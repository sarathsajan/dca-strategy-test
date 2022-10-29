import ccxt

# provide an api_key and secret_key as keyword arguments
secret_key = '8jAExqtrfOf7e8xfC1xVJG8rWZWoL8KsjFGnH9PE'
API_key = 'SHdVuqbKLO9gVszF9qc4kI6VsBvfmDbtol11Sdlpv0af5viRe8vKgXqkB24RZdf3'

# connect wazirx
wazirx = ccxt.wazirx()
wazirx.apiKey = API_key
wazirx.secret = secret_key

amount = 3
price = 17.44

wazirx.create_order('WRX/INR', 'limit', 'sell', amount, price)