from ImgSite import ImgSite
import string


class PostImg(ImgSite):
    def __init__(self):
        domain_name = "postimg.cc"
        test_valid_id = "D4792gr1"
        id_choices = string.ascii_letters + string.digits, 7

        super().__init__(domain_name, test_valid_id, id_choices)