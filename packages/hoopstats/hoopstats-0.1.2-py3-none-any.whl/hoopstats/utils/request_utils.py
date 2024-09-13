from .decorator_utils import timeout

from requests import get, Response
from typing import Optional
from requests.exceptions import RequestException


@timeout(seconds=10)
def get_wrapper(url: str) -> Optional[Response]:
    """
    Requests.Get() Wrapper with a timeout 

    Args:
        url (str): GET Url 

    Returns:
        Optional[Response]: Response Object if status is 200 
    """
    try:
        response = get(url)
        response.raise_for_status()
        if response.status_code == 200:
            return response
        else:
            print(f"Non-200 status code received: {response.status_code}")
            return None
    except RequestException as e:
        print(f"Request failed: {e}")
        return None
