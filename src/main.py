import concurrent.futures
import random
from loguru import logger
import sys
from ImgSites.PostImg import PostImg
from ImgSites.ImgBB import ImgBB
from ImgSites.FreeImageHost import FreeImageHost


SUPPORTED_IMG_SITES = ["freeimagehost", "imgbb", "postimg"]

def ask_for_image_site():
    while True:
        site = input(f"Which image site do you want to use? ({', '.join(SUPPORTED_IMG_SITES)}) ").lower()

        if site in SUPPORTED_IMG_SITES:
            break
        else:
            logger.error("Please enter a valid image site.")

    return site

def ask_for_number(input_text, default_val = None):
    while True:
        amount = input(input_text)

        if default_val is not None and amount == "":
            return default_val

        if amount.isdigit():
            break
        else:
            logger.error("Please enter a valid number.")

    return int(amount)

def main():
    logger.remove()
    logger.add(sys.stderr, format="{time:HH:mm:ss} | <level>{message}</level>")
    logger.level("INFO", color="<yellow>")

    site = ask_for_image_site()
    amount_gen = ask_for_number("How many random IDs do you want to check? ")
    amount_thread = ask_for_number("How many threads do you want to use? ")
    timeout = ask_for_number("How much timeout? (default 0) ", 0)

    if site == "imgbb":
        img_site = ImgBB()
    elif site == "postimg":
        img_site = PostImg()
    elif site == "freeimagehost":
        img_site = FreeImageHost()
    else:
        raise ValueError("Invalid site name.")

    image_ids = [''.join(random.choices(img_site.id_choices[0], k=img_site.id_choices[1])) for _ in range(amount_gen)]
    invalid_ids = []
    valid_ids = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=amount_thread) as executor:
        future_data = {executor.submit(img_site.check_img, img_id, timeout):img_id for img_id in image_ids}

        for future in concurrent.futures.as_completed(future_data):
            img_id = future_data[future]

            try:
                is_valid = future.result()

                if is_valid:
                    valid_ids.append(img_id)
                    logger.success(f"ID {img_id} is valid.")
                else:
                    invalid_ids.append(img_id)
                    logger.error(f"ID {img_id} is invalid.")

            except Exception as exc:
                logger.error(f"An error occurred with {img_id}: {exc}")

    logger.info("------- Summary -------")
    logger.info("Found {} invalid IDs for {} random IDs".format(len(invalid_ids), amount_gen))

    if len(valid_ids) > 0:
        logger.success(f"Valid IDs: {', '.join(valid_ids)}")
    else:
        logger.error("No valid IDs found.")

    if not img_site.check_img(img_site.test_valid_id):
        logger.error("Your IP might be banned/ratelimited from the image site.")
    else:
        logger.success(f"Your IP seems to be working fine with {site}.")

if __name__ == '__main__':
    main()
