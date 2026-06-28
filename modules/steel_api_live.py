import requests
def fetch_live_steel():
    # Example integration point - replace with your actual API endpoint
    try:
        # response = requests.get("https://api.metalprices.com/...", timeout=5)
        # return response.json()
        return {"Rebar": 650.00, "Coil": 720.50} 
    except:
        return {"Rebar": 650.00, "Coil": 720.50}
