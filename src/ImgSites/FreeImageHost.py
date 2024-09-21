from ImgSite import ImgSite
import string
import requests
import time


class FreeImageHost(ImgSite):
    def __init__(self):
        domain_name = "freeimage.host/i"
        test_valid_id = "div70Cu"
        id_choices = string.ascii_letters + string.digits, 7

        super().__init__(domain_name, test_valid_id, id_choices)

    def check_img(self, img_id:str, timeout = 0):
        if timeout > 0:
            time.sleep(timeout)

        # save resources by doing only head request
        response = requests.head(f'https://{self.domain_name}/{img_id}')

        return response.status_code != 404