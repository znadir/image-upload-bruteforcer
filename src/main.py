import concurrent.futures
import requests
import random
import time
import string
from loguru import logger
import sys


def ask_for_image_site():
    while True:
        site = input("Which image site do you want to use? (imgbb, postimg) ").lower()

        if site in ["imgbb", "postimg"]:
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

def check_img(domain_name:str, img_id:str, timeout = 0):
    time.sleep(timeout)
    response = requests.get(f'https://{domain_name}/{img_id}')

    is_valid = response.status_code == 200

    return is_valid

def main():
    logger.remove()
    logger.add(sys.stderr, format="{time:HH:mm:ss} | <level>{message}</level>")
    logger.level("INFO", color="<yellow>")

    site = ask_for_image_site()
    amount_gen = ask_for_number("How many random IDs do you want to check? ")
    amount_thread = ask_for_number("How many threads do you want to use? ")
    timeout = ask_for_number("How much timeout? (default 0) ", 0)

    if site == "imgbb":
        domain_name = "ibb.co"
        test_valid_id = "rbPzWq8"
        id_choices = string.ascii_letters + string.digits, 7
    elif site == "postimg":
        domain_name = "postimg.cc"
        test_valid_id = "D4792gr1"
        id_choices = string.ascii_letters + string.digits, 7
    else:
        raise ValueError("Invalid site name.")

    image_ids = [''.join(random.choices(id_choices[0], k=id_choices[1])) for _ in range(amount_gen)]
    invalid_ids = []
    valid_ids = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=amount_thread) as executor:
        future_data = {executor.submit(check_img, domain_name, img_id, timeout):img_id for img_id in image_ids}

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

    if not check_img(domain_name, test_valid_id):
        logger.error("Your IP might be banned/ratelimited from the image site.")
    else:
        logger.info("Your IP seems to be working fine with the image site.")

if __name__ == '__main__':
    main()
