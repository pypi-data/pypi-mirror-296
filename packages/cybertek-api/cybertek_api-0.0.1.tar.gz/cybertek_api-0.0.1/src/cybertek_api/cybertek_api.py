import requests

def log_request_to_db(api_log_url, script_name, endpoint_url, status_code):
    """
    Logs script execution details to a custom API endpoint that writes to a database.

    Parameters:
        api_logging_url (str): The URL of the custom logging API endpoint.
        script_name (str): The name of the script being executed.
        endpoint_url (str): The API endpoint that the script is calling.
        status_code (int): The HTTP status code received from the API.

    Raises:
        HTTPError: If the logging API request fails.
    """
    # Prepare the log data
    log_data = {
        "script_name": script_name,
        "api_endpoint": endpoint_url,
        "status_code": status_code
    }

    # Send the log data as a JSON payload to the custom logging API
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(api_log_url, json=log_data, headers=headers)
        response.raise_for_status()  # Raise exception if the request fails
        print("Log successfully sent.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to log request data: {str(e)}")
