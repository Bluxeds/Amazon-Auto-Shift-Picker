STALL_AFTER_LOGIN = 2 # Seconds the program will stall after logging in before starting to interact with the AtoZ shift management

EARLIEST_TIME = "00:00"

LATEST_TIME = "00:00"

LONGEST_SHIFT = 10

WEEKDAYS = [
"Monday",
"Tuesday",
"Wednesday",
"Thursday",
"Friday",
"Saturday",
"Sunday"
]

START_DATE = "Dec 22" 
END_DATE = "Dec 27" 

CHROME_PROFILE_DIRECTORY_PATH = r""

LOGIN_URL = "https://atoz-login.amazon.work"

Amazon_Login = ""

HOURS_TO_RUN = 3  # Hours

SECONDS_BETWEEN_CHECKS = 5 # Seconds to wait once all days are checked for available shifts to recheck all days again

import time
import random
from datetime import datetime
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


def get_date_object(date_str):
    """
    The function `get_date_object` parses a date string in the format "%b %d" and adjusts the year based
    on the current date if needed.
    
    :param date_str: The function `get_date_object` takes a date string in the format "%b %d" (e.g.,
    "Dec 25") and returns a datetime object with the correct year adjusted based on the current date. If
    the input date is in the future compared to the current date, it will
    :return: The function `get_date_object` returns a datetime object with the year adjusted based on
    the current date. If the input date string is in the format "%b %d" (e.g., "Dec 25"), it will return
    a datetime object with the same month and day but with the year adjusted to the current year or the
    next/previous year depending on the current month and the input month
    """
    try:
        dt = datetime.strptime(date_str, "%b %d")
        
        now = datetime.now()
        year = now.year
        
        if now.month == 12 and dt.month == 1:
            year += 1
        elif now.month == 1 and dt.month == 12:
            year -= 1
            
        return dt.replace(year=year)
    except ValueError:
        return None

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

                schedule_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div/nav/div[2]/div/ul/li[2]/button")))
                schedule_button.click()

                find_shifts_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div/nav/div[2]/div/ul/li[2]/div/ul/li[4]/div/a"))) 
                find_shifts_button.click()
                print("Navigated to Find Shifts.")

            except Exception as e:
                print(f"Navigation failed: {e}")
                return 
            
            print(f"Checking schedule from {START_DATE} to {END_DATE}...")

            start_dt = get_date_object(START_DATE)
            end_dt = get_date_object(END_DATE)

            if not start_dt or not end_dt:
                print("ERROR: START_DATE or END_DATE is invalid or empty. Please check config.")
                return

            # We look up to 60 days ahead max to prevent infinite loops.
            # The code inside will 'break' much earlier once it hits the END_DATE.
            for i in range(1, 60):
                
                # XPaths
                day_container_xpath = f"//*[@id='atoz-app-root']/div[1]/div/div[2]/div/div[{i}]"
                day_name_xpath = f"{day_container_xpath}/div/div[1]"
                day_date_xpath = f"{day_container_xpath}/div/div[2]"
                
                try:
                    day_date_element = self.wait.until(EC.presence_of_element_located((By.XPATH, day_date_xpath)))
                    date_text = day_date_element.text.strip().replace("\n", " ") 
                    
                    current_dt = get_date_object(date_text)
                    
                    if current_dt is None:
                        print(f"Could not parse date '{date_text}' for Day {i}. Skipping.")
                        continue

                    # Check A: Are we past the end date?
                    if current_dt > end_dt:
                        print(f"--- Reached {date_text}. This is after {END_DATE}. Stopping check. ---")
                        break # <--- THIS STOPS THE LOOP
                    
                    # Check B: Are we before the start date?
                    if current_dt < start_dt:
                        print(f"Day {i} ({date_text}) is before {START_DATE}. Skipping.")
                        continue # <--- Skip this iteration, check next day
                    
                    # Check C: Weekday Filter (Only check if we are in date range)
                    day_name_element = self.driver.find_element(By.XPATH, day_name_xpath)
                    full_day_text = day_name_element.text.strip()
                    
                    is_allowed_weekday = False
                    for allowed_day in WEEKDAYS:
                        if allowed_day in full_day_text:
                            is_allowed_weekday = True
                            break
                    
                    if not is_allowed_weekday:
                        print(f"--- Day {i} ({full_day_text}, {date_text}) is excluded by Weekday filter. Skipping. ---")
                        continue

                    print(f"--- Checking Day {i}: {full_day_text}, {date_text} ---")
                    
                    day_button = self.driver.find_element(By.XPATH, day_container_xpath)
                    day_button.click()
                    time.sleep(2) 

                    shift_container_xpath = "//*[@id='atoz-app-root']/div[1]/div/div[3]/div[1]/div/div[3]/div[2]/div"
                    shift_rows = self.driver.find_elements(By.XPATH, shift_container_xpath)
                    
                    if len(shift_rows) == 0:
                        print("  No shifts found.")

                    for j, row in enumerate(shift_rows, start=1):
                        try:
                            time_xpath = f"//*[@id='atoz-app-root']/div[1]/div/div[3]/div[1]/div/div[3]/div[2]/div[{j}]/div/div[1]/div[1]/div[1]/div[1]/div/strong"
                            button_xpath = f"//*[@id='atoz-app-root']/div[1]/div/div[3]/div[1]/div/div[3]/div[2]/div[{j}]/div/div[2]/div/button"

                            time_element = row.find_element(By.XPATH, time_xpath)
                            time_text = time_element.text 
                            
                            if "-" in time_text:
                                start_str, end_str = time_text.split("-")
                                start_parsed = parse_hour(start_str.strip())
                                
                                # Shift Time Checks
                                if parse_hour(EARLIEST_TIME) <= start_parsed <= parse_hour(LATEST_TIME):
                                    end_parsed = parse_hour(end_str.strip())
                                    duration = time_diff(end_parsed, start_parsed)
                                    
                                    if duration <= LONGEST_SHIFT:
                                        print(f"    MATCH! Found {duration}hr shift: {time_text}")
                                        add_button = row.find_element(By.XPATH, button_xpath)
                                        
                                        if "Add" in add_button.get_attribute("aria-label") or "Add" in add_button.text:
                                            self.wait_and_click(add_button)
                                            # Confirm success modal
                                            try:
                                                done_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='AddOpportunityModalSuccessDoneButton']")))
                                                done_button.click()
                                                print("    Shift Added Successfully!")
                                            except:
                                                pass
                        except:
                            continue

                except Exception as e:
                    # If we run out of days on the slider (Element not found), we stop
                    print(f"End of schedule slider reached or error at Day {i}. Stopping.")
                    break

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
            time.sleep(5) # Can be adjusted to reduce/increase wait times between checks for available shifts
    browser.exit()

if __name__ == "__main__":
    main()
