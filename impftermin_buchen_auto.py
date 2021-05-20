from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import requests
from os.path import dirname, abspath

CHROME_DRIVER_PATH = f"{dirname(abspath(__file__))}/webdrivers/v90/chromedriver.exe"
CENTRE_IDS = {
        "arena": 158431,
        "messe": 158434,
        "velodrom": 158435,
        "erika": 158437,
        "tegel": 158436,
        "tempelhof": 158433
}
OPEN_URL = "https://api.impfstoff.link/?v=0.3&robot=1"

# Note to devs: If you use our API, please add query string robot=1 and respect the rate limit of 1x/1000ms.
"""
div class=availabilities-message
        button
        span class=dl-button-label, innertext ist label mit termin= "Nächster Termin am 26. Mai 2021"
"""

def check_available_btn():
        try:
                available_div = driver.find_element_by_class_name("availabilities-message")
                available_btn = available_div.find_element_by_tag_name("button")
                available_msg = available_btn.find_element_by_tag_name("span")
                print(available_msg.text)
        except NoSuchElementException:
                print("!!!no available Impftermin!!!")

def check_available_options():
        try:
                selector_element = driver.find_element_by_id("booking_motive")
                selector_element_children = selector_element.find_elements_by_tag_name("option")
                select = Select(selector_element)
        except NoSuchElementException:
                check_available_btn()
                return
        ## select by visible text
        #select.select_by_visible_text('Banana')
        ## select by value 
        #select.select_by_value('1')
        for option in selector_element_children[1:]:
                option_val = option.get_attribute("value")
                print(f"\t{option_val}")
                select.select_by_value(option_val)
                sleep(3)
                check_available_btn()
                sleep(1)

def check_all_places():
        for place in CENTRE_IDS.keys():
                print(f"---> checking {place}")
                booking_site_path = f"https://www.doctolib.de/institut/berlin/ciz-berlin-berlin?pid=practice-{CENTRE_IDS[place]}"
                driver.get(booking_site_path)
                check_available_options()
                sleep(2)


driver = webdriver.Chrome(CHROME_DRIVER_PATH)
def main():
        """ booking_site_path = f"https://www.doctolib.de/institut/berlin/ciz-berlin-berlin?pid=practice-{CENTRE_IDS['tempelhof']}"
        driver.get(booking_site_path)
        check_available_options() """
        check_all_places()
        return
        response = requests.get(OPEN_URL)
        if response.status_code in range(100, 201):
                print("successful update")
                content = response.json()
                for place in content['stats']:
                        if place['open'] == True:
                                print(f"{place['name']} has an available Impftermin, opening booking site")
                                booking_site_path = f"https://www.doctolib.de/institut/berlin/ciz-berlin-berlin?pid=practice-{CENTRE_IDS[place['id']]}"
                                driver.get(booking_site_path)
                                check_available_options()
                                break

if __name__ == "__main__":
        main()

# https://api.impfstoff.link/?v=0.3
