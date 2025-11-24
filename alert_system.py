import requests
import time

CRYPTO_ID = "bitcoin"   
CURRENCY = "usd"        
API_URL = "https://api.coingecko.com/api/v3/simple/price" 

VOLATILITY_THRESHOLD = 5.0 
CHECK_INTERVAL_SECONDS = 60 

def fetch_current_price(crypto_id: str, currency: str) -> Optional[float]:
    
    params = {
     'ids': crypto_id,
        'vs_currencies': currency
    }
     
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status() 
        data = response.json()
        current_price = data.get(crypto_id, {}).get(currency)
        
        if current_price is None:
            
            print(f"ERROR: Price data not found for {crypto_id}/{currency} in API response.")
            return None
            
        return float(current_price) 
        
    except requests.exceptions.RequestException as e:
        
        print(f"NETWORK ERROR: Could not fetch data. {e}")
        return None



def calculate_percentage_change(old_price: float, new_price: float) -> float:
    if old_price == 0:
        return 0.0 
    
    change = ((new_price - old_price) / old_price) * 100
    return abs(change)


def send_alert(crypto_id: str, percentage_change: float, current_price: float):
    """
    Prints a prominent alert message to the console using string formatting.
    """
    # Uses triple quotes and f-strings for clean, multi-line output
    alert_message = (
        f"\n{'='*60}\n"
        f"!!! 🚨 HIGH VOLATILITY ALERT for {crypto_id.upper()}! 🚨 !!!\n"
        f"Change since last check: {percentage_change:.2f}% "
        f"(Threshold: {VOLATILITY_THRESHOLD:.1f}%)\n"
        f"CURRENT PRICE: ${current_price:,.2f}\n"
        f"Time: {time.ctime()}\n"
        f"{'='*60}\n"
    )
    print(alert_message)

def run_alert_system():
    
    print("--- 🚀 Crypto Volatility Alert System Initializing (BTC/USD) 🚀 ---")
    print(f"Parameters: Threshold={VOLATILITY_THRESHOLD:.1f}%, Interval={CHECK_INTERVAL_SECONDS}s")
    print("-" * 60)

    initial_price = fetch_current_price(CRYPTO_ID, CURRENCY)
    
    if initial_price is None:
        print("\nFATAL ERROR: Initialization failed. Check network connection or API URL. Exiting.")
        return

    previous_price = initial_price
    print(f"✅ Initial Price Baseline Set: ${previous_price:,.2f}")
    
    
    while True:
        
        print(f"\nSleeping for {CHECK_INTERVAL_SECONDS} seconds...")
        time.sleep(CHECK_INTERVAL_SECONDS) 
        current_price = fetch_current_price(CRYPTO_ID, CURRENCY)
        
        if current_price is None:
            continue
        volatility = calculate_percentage_change(previous_price, current_price)
 
        print(f"Status: Price: ${current_price:,.2f} | Change since last check: {volatility:.2f}%")
        
        if volatility >= VOLATILITY_THRESHOLD:
            send_alert(CRYPTO_ID, volatility, current_price)
        
        previous_price = current_price
        
if __name__ == "__main__":
    run_alert_system()

