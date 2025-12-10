STALL_AFTER_LOGIN = 2 # Seconds the program will stall after logging in before starting to interact with the AtoZ shift management

NUMBER_OF_DAYS = 0

EARLIEST_TIME = "00:00"

LATEST_TIME = "00:00"

LONGEST_SHIFT = 0

WEEKDAYS = [
"Monday",
"Tuesday",
"Wednesday",
"Thursday",
"Friday",
"Saturday",
"Sunday"
]


CHROME_PROFILE_DIRECTORY_PATH = r""

LOGIN_URL = "https://atoz-login.amazon.work"

Amazon_Login = ""

HOURS_TO_RUN = 0  # Hours

SECONDS_BETWEEN_CHECKS = 0 # Seconds to wait once all days are checked for available shifts to recheck all days again

import time
import random
import undetected_chromedriver as uc
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions


HOMEPAGE_IDENTIFIER = "//*[@id='atoz-app-root']/div[2]/div[1]/div[3]/h2"
MENU_BURGER = "//*[@id='atoz-global-nav-header']/div/div/header/div/div/nav/ul/li[1]/button"


class Browser:

    def __init__(self):
        self.options = ChromeOptions()
        self.options.add_argument(f"--user-data-dir={CHROME_PROFILE_DIRECTORY_PATH}")
        self.driver = uc.Chrome(options=self.options)
        self.driver.get("https://atoz-login.amazon.work")
        self.wait = WebDriverWait(self.driver, 10)
        
    def wait_and_click(self, element):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))
        time.sleep(random.uniform(0.3, 0.7))
        element.click()

    def delay_typing(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0, 0.1))

    def is_logged_in(self):
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, HOMEPAGE_IDENTIFIER))
                )
            except Exception as error:
                print(f"Error | {error}")

    def login(self):
            print("Checking for existing session...")

            if self.is_logged_in():
                print("Already logged in! Skipping login sequence.")
                return  

            print("Session not found. Attempting login...")

            try:
                uname = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='associate-login-input']"))
                )
                self.delay_typing(uname, Amazon_Login)

                login_button = self.driver.find_element(By.XPATH, "//*[@id='login-form-login-btn']")
                self.wait_and_click(login_button)
                
                try:
                    short_wait = WebDriverWait(self.driver, 5) 
                    short_wait.until(EC.presence_of_element_located((By.XPATH, HOMEPAGE_IDENTIFIER)))
                    print("Login successful after first step! bypassing secondary steps.")
                    return 
                except:
                    print("Homepage not detected immediately. Proceeding to secondary login...")

            except Exception as error:
                print(f"Error during Step 1 | {error}")

            try:
                uname2 = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='input-id-4']"))
                )
                self.delay_typing(uname2, Amazon_Login)

                login_button2 = self.driver.find_element(By.XPATH, "//*[@id='root']/div[1]/div[2]/div/div[2]/div/button")
                self.wait_and_click(login_button2)

            except Exception as error:
                pass 

            try:
                passkey_element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div[1]/div[2]/div/div[2]/div[2]/div[1]/button"))
                )
                self.wait_and_click(passkey_element)
                
                print("--- MANUAL INTERACTION REQUIRED ---")
                print("Please complete the Windows Hello/Security Key prompt in the browser.")
                
            except Exception as error:
                pass

            print(f"Waiting for homepage element: {HOMEPAGE_IDENTIFIER}")
            try:
                # Waits 60 seconds for the user to type in their passkey
                WebDriverWait(self.driver, 60).until(
                    EC.presence_of_element_located((By.XPATH, HOMEPAGE_IDENTIFIER))
                )
                print("Login Successful! Homepage detected. Resuming script...")

            except TimeoutException: 
                print("Timed out waiting for login. Exiting.")
                self.driver.quit()
                exit()
        
        
    def save_cookies(self):
        cookies = self.driver.get_cookies()
        json.dump(cookies, open("cookies", "wt", encoding="utf8"))

    def exit(self):
        self.driver.quit()


    def back_home(self):
        menu_burger =  self.wait.until(
                EC.presence_of_element_located((By.XPATH, MENU_BURGER))
            )
        menu_burger.click()
        
        time.sleep(2) 
        
        home_nav_button = self.driver.find_element(By.XPATH, "//*[@id='side-nav-item-top-level-home_nav_item_0']")
        home_nav_button.click()


    def find_shifts(self):
            print("Attempting to navigate to shifts...")
            
            try:
                burger_menu = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='atoz-global-nav-header']/div/div/header/div/div/nav/ul/li[1]/button"))) 
                burger_menu.click()
                print("Clicked Burger Menu.")

                schedule_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div/nav/div[2]/div/ul/li[2]/button")))
                schedule_button.click()
                print("Clicked Schedule.")

                find_shifts_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div/nav/div[2]/div/ul/li[2]/div/ul/li[4]/div/a"))) 
                find_shifts_button.click()
                print("Clicked Find Shifts.")

            except Exception as e:
                print(f"Navigation failed: {e}")
                return 
            
            print(f"Starting to check schedule for {NUMBER_OF_DAYS} days...")

            for i in range(1, NUMBER_OF_DAYS + 1):
                
                day_container_xpath = f"//*[@id='atoz-app-root']/div[1]/div/div[2]/div/div[{i}]"
                
                # XPath for the text inside that container (e.g., "Wednesday")
                day_label_xpath = f"{day_container_xpath}/div/div[1]"
                
                try:
                    day_label_element = self.wait.until(EC.presence_of_element_located((By.XPATH, day_label_xpath)))
                    
                    full_day_text = day_label_element.text.strip() # e.g. "Wednesday" or "Wednesday\nDec 10"
                    
                    is_allowed_day = False
                    for allowed_day in WEEKDAYS:
                        if allowed_day in full_day_text:
                            is_allowed_day = True
                            print(f"--- Day {i} is {allowed_day}. Proceeding... ---")
                            break
                    
                    if not is_allowed_day:
                        print(f"--- Day {i} ({full_day_text}) is not in allowed list. Skipping. ---")
                        continue 

                    day_button = self.driver.find_element(By.XPATH, day_container_xpath)
                    day_button.click()
                    
                    time.sleep(2) 

                except Exception as e:
                    print(f"Could not read/click Day {i}: {e}")
                    continue 

                shift_container_xpath = "//*[@id='atoz-app-root']/div[1]/div/div[3]/div[1]/div/div[3]/div[2]/div"
                shift_rows = self.driver.find_elements(By.XPATH, shift_container_xpath)
                
                print(f"Found {len(shift_rows)} potential shifts.")

                for j, row in enumerate(shift_rows, start=1):
                    try:
                        time_xpath = f"//*[@id='atoz-app-root']/div[1]/div/div[3]/div[1]/div/div[3]/div[2]/div[{j}]/div/div[1]/div[1]/div[1]/div[1]/div/strong"
                        button_xpath = f"//*[@id='atoz-app-root']/div[1]/div/div[3]/div[1]/div/div[3]/div[2]/div[{j}]/div/div[2]/div/button"

                        time_element = row.find_element(By.XPATH, time_xpath)
                        time_text = time_element.text 
                        print(f"  Shift {j}: Found time '{time_text}'")
                        
                        if "-" in time_text:
                            start_str, end_str = time_text.split("-")
                            start_parsed = parse_hour(start_str.strip())
                            earliest_parsed = parse_hour(EARLIEST_TIME)
                            latest_parsed = parse_hour(LATEST_TIME)

                            if start_parsed >= earliest_parsed and start_parsed <= latest_parsed:
                                
                                end_parsed = parse_hour(end_str.strip())
                                duration = time_diff(end_parsed, start_parsed)
                                
                                if duration <= LONGEST_SHIFT:
                                    print(f"    MATCH! Shift fits criteria ({duration} hrs). Attempting to add...")
                                    add_button = row.find_element(By.XPATH, button_xpath)
                                    
                                    if "Add" in add_button.get_attribute("aria-label") or "Add" in add_button.text:
                                        self.wait_and_click(add_button)
                                        try:
                                            done_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='AddOpportunityModalSuccessDoneButton']")))
                                            done_button.click()
                                            print("    Shift successfully added!")
                                        except:
                                            print("    No success modal appeared.")
                                    else:
                                        print("    Button was not an 'Add' button.")
                                else:
                                    print(f"    Skipping: Shift too long ({duration} hrs).")
                            else:
                                print("    Skipping: Start time outside preferred window.")
                        
                    except Exception as ex:
                        continue

def parse_hour(hora):
    hour, mint = hora.split(":")
    minute = "".join([i for i in mint if i.isdigit()])
    section = mint[len(minute):]
    hour, minute = int(hour), int(minute)
    if section == "pm" and hour != 12:
        hour += 12
    return (hour, minute)

def earlier_time(time1, time2):
    if time1[0] > time2[0]:
        return time2
    elif time1[0] < time2[0]:
        return time1
    elif time1[1] > time2[1]:
        return time2
    else:
        return time1

def time_diff(time1, time2):
    if time1[0] < time2[0]:
        midnight_offset = 24 - time2[0]
        time2 = list(time2)
        time2[0] = - midnight_offset
    diff = time1[0] - time2[0]
    diff -= time1[1] / 60
    diff += time2[1] / 60
    return diff

def main():
    start = time.time()
    browser = Browser()
    browser.login()
    while time.time() - start < HOURS_TO_RUN * 60 * 60:
        browser.find_shifts()
        browser.back_home()
        done = time.time()
        while time.time() - done < SECONDS_BETWEEN_CHECKS:
            time.sleep(60) # Can be adjusted to reduce/increase wait times between checks for available shifts
    browser.exit()

if __name__ == "__main__":
    main()
