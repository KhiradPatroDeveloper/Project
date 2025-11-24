#1.Configuration Module(Global Settings)
def get_config():
    """Returns essential configuration parameters."""
    return 
        "CRYPTO": "bitcoin",
        "CURRENCY": "usd",
        "VOLATILITY_THRESHOLD": 5.0, # Percentage change to trigger alert
        "API_URL": "https://api.coingecko.com/api/v3/simple/price"

 #2.Data Retrieval Module 
def get_price_data(config):
    """Fetches the current price and 24h change."""
    try:
        params = {'ids': config["CRYPTO"], 'vs_currencies': config["CURRENCY"], 'include_24hr_change': 'true'}
        response = requests.get(config["API_URL"], params=params)
        data = response.json()
        
        # Basic check for price data
        price = data[config["CRYPTO"]][config["CURRENCY"]]
        change_24h = data[config["CRYPTO"]]["usd_24h_change"]
        return price, change_24h
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None

 #3.Calculation Module 
def check_volatility(change_24h, threshold):
    """Calculates if volatility exceeds the set threshold."""
    # Uses basic arithmetic operator: abs() for absolute value
    return abs(change_24h) >= threshold

 #4.Alerting/Notification 
def send_alert(crypto, price, change_24h):
    """Prints a console notification for high volatility."""
    direction = "UP" if change_24h > 0 else "DOWN"
    # Basic string formatting
    print("\n" + "="*30)
    print(f"🚨 VOLATILITY ALERT for {crypto.upper()}! 🚨")
    print(f"Current Price: ${price:,.2f}")
    print(f"24h Change: {direction} by {abs(change_24h):.2f}%")
    print("="*30)

 #5.Main Execution(Top Down Flow)
if __name__ == "__main__":
    config = get_config()
    price, change = get_price_data(config)
    
    if price is not None and change is not None:
        if check_volatility(change, config["VOLATILITY_THRESHOLD"]):
            send_alert(config["CRYPTO"], price, change)
        else:
            # Basic conditional output
            print(f"Price is stable. {config['CRYPTO'].capitalize()} 24h change: {change:.2f}% (Threshold: {config['VOLATILITY_THRESHOLD']:.2f}%)")