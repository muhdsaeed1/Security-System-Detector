import requests
from datetime import datetime

# Define the recipients here
recipients = ["1234567890", "9876543210"]  # Add recipient phone numbers


def get_api_key():
    json_array = {
        "auth": {
            "username": "hamzashehu43@yahoo.com",
            "password": "08036110256"
        }
    }
    try:
        # Send a POST request to the API endpoint to obtain the API key
        response = requests.post(
            'https://api.ebulksms.com:8080/getapikey.json', json=json_array)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON to extract the API key
            response_data = response.json()
            api_key = response_data.get('apikey')

            if api_key:
                return api_key
            else:
                print("API key not found in the response.")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


API_KEY = get_api_key()


def send_sms():
    now = datetime.now()
    formatted_now = now.strftime("%d/%m/%y %H:%M:%S")
    try:
        # Create the SMS payload in the specified JSON format
        sms_payload = {
            "SMS": {
                "auth": {
                    "username": "hamzashehu43@yahoo.com",
                    "apikey": API_KEY
                },
                "message": {
                    "sender": "Alx Final Project",
                    "messagetext": f"Motion detected at {formatted_now}",
                    "flash": "0"
                },
                "recipients": {
                    "gsm": recipients
                },
                "dndsender": 1
            }
        }

        # Send a POST request to the SMS sending API
        response = requests.post(
            "https://api.ebulksms.com:8080/sendsms.json", json=sms_payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            response_data = response.json()

            # Check the response for success or failure
            if response_data.get("status") == "SUCCESS":
                print("SMS sent successfully.")
            else:
                print(
                    f"Failed to send SMS. Error message: {response_data.get('message')}")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Call the send_sms() function to send SMS messages
send_sms()
