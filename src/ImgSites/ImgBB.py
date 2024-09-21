from ImgSite import ImgSite
import string

class ImgBB(ImgSite):
    def __init__(self):
        domain_name = "ibb.co"
        test_valid_id = "rbPzWq8"
        id_choices = string.ascii_letters + string.digits, 7

        super().__init__(domain_name, test_valid_id, id_choices)