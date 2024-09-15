import requests

def health_check(url):
    """
    Function to check the health of a website.
    """
    try:
        response = requests.get(url)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def make_verification_required_request(url,token):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    try:
        response = requests.get(url, headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        return None, str(e)

def simple_response_make_verification_required_request(url,token):
    headers = {
        'Authorization': f'Bearer {token}',
    }
    try:
        response = requests.get(url, headers=headers)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)

def connection(url):
    try:
        response = requests.get(url)
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)
