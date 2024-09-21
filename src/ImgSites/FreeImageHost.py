from ImgSite import ImgSite
import string


class FreeImageHost(ImgSite):
    def __init__(self):
        domain_name = "freeimage.host/i"
        test_valid_id = "div70Cu"
        id_choices = string.ascii_letters + string.digits, 7

        super().__init__(domain_name, test_valid_id, id_choices)