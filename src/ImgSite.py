import requests
import time


class ImgSite():
    """
    Abstract class for image sites.
    """
    def __init__(self, domain_name:str, test_valid_id:str, id_choices:tuple):
        """
        Initialize the ImgSite object.

        Parameters:
        domain_name (str): The domain name of the image site.
        test_valid_id (str): A valid ID to test IP.
        """
        self.domain_name = domain_name
        self.test_valid_id = test_valid_id
        self.id_choices = id_choices

    def check_img(self, img_id:str, timeout = 0):
        if timeout > 0:
            time.sleep(timeout)

        response = requests.get(f'https://{self.domain_name}/{img_id}')

        return response.status_code == 200