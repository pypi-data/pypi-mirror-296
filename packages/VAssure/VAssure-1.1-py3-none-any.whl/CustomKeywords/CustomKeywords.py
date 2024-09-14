import time
from datetime import datetime, timedelta
from SeleniumLibrary.base import keyword
import pytz
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException, NoSuchElementException

TIMEZONE_OFFSET_MAP = {
    'UTC-12': 'Etc/GMT+12',
    'UTC-11': 'Pacific/Niue',
    'UTC-10': 'Pacific/Honolulu',
    'UTC-9': 'America/Anchorage',
    'UTC-8': 'America/Los_Angeles',
    'UTC-7': 'America/Denver',
    'UTC-6': 'America/Chicago',
    'UTC-5': 'America/New_York',
    'UTC-4': 'America/Barbados',
    'UTC-3': 'America/Argentina/Buenos_Aires',
    'UTC-2': 'Atlantic/South_Georgia',
    'UTC-1': 'Atlantic/Azores',
    'UTC+0': 'Etc/GMT',
    'UTC+1': 'Europe/Brussels',
    'UTC+2': 'Europe/Athens',
    'UTC+3': 'Europe/Moscow',
    'UTC+3:30': 'Asia/Tehran',
    'UTC+4': 'Asia/Dubai',
    'UTC+4:30': 'Asia/Kabul',
    'UTC+5': 'Asia/Karachi',
    'UTC+5:30': 'Asia/Kolkata',  # India Standard Time
    'UTC+5:45': 'Asia/Kathmandu',
    'UTC+6': 'Asia/Dhaka',
    'UTC+6:30': 'Asia/Cocos',
    'UTC+7': 'Asia/Bangkok',
    'UTC+8': 'Asia/Singapore',
    'UTC+8:45': 'Australia/Perth',
    'UTC+9': 'Asia/Tokyo',
    'UTC+9:30': 'Australia/Adelaide',
    'UTC+10': 'Australia/Sydney',
    'UTC+10:30': 'Australia/Lord_Howe',
    'UTC+11': 'Pacific/Noumea',
    'UTC+12': 'Pacific/Fiji'
}

class CustomKeywords:

    @keyword
    def get_browser_driver(self):
        return BuiltIn().get_library_instance('SeleniumLibrary').driver

    @keyword
    def interact_with_form_element(self, driver: WebDriver, locator, interaction_type, *values):
        """
        Interacts with various form elements based on the given locator and interaction type.

        Supported interaction types:
        - 'input_text': Input text into a text field.
        - 'select_dropdown': Select an option from a dropdown.
        - 'select_radio': Select a radio button.
        - 'select_checkbox': Select a checkbox.
        - 'click_element': Click an element.
        - 'get_text': Get text from an element.

        Examples:
        | Interact With Form Element | ${driver} | id=username_field    | input_text    | testuser          |
        | Interact With Form Element | ${driver} | id=country_dropdown | select_dropdown | United States    |
        | Interact With Form Element | ${driver} | id=gender_male      | select_radio    |                 |
        | Interact With Form Element | ${driver} | id=agree_checkbox   | select_checkbox |                 |
        | Interact With Form Element | ${driver} | id=click_element   | click_element |                 |
        | Interact With Form Element | ${driver} | id=get_text   | get_text |                 |
        """
        by_locator, locator_value = self.split_the_locator(locator)
        def perform_action(driver: WebDriver, element, timeout=60):
            if interaction_type == 'input_text':
                try:
                    element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))
                    element.clear()
                    element.send_keys(values[0])
                except ElementNotInteractableException:
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", element)
                    element.clear()
                    element.send_keys(values[0])
            elif interaction_type == 'select_dropdown':
                if element.tag_name == 'select':
                    try:
                        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))
                        element.clear()
                        element.send_keys(values[0])
                    except ElementNotInteractableException:
                        driver.execute_script(
                            "arguments[0].scrollIntoView(true);", element)
                        element.clear()
                        element.send_keys(values[0])
                elif element.tag_name in ['div', 'input', 'textarea']:
                    try:
                        element.click()
                        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))
                        time.sleep(1)
                        element.clear()
                        element.send_keys(values[0])
                    except ElementNotInteractableException:
                        driver.execute_script(
                            "arguments[0].scrollIntoView(true);", element)
                        element.clear()
                        element.send_keys(values[0])
                    dropdown_options_locator = (
                        By.XPATH, f"//li[contains(.,'{values[0]}')]")
                    WebDriverWait(driver, timeout).until(
                        EC.visibility_of_any_elements_located(dropdown_options_locator))
                    element.send_keys(Keys.ARROW_DOWN)
                    element.send_keys(Keys.ENTER)
                else:
                    raise ValueError(
                        f"Unsupported element type for dropdown: {element.tag_name}")
            elif interaction_type in ['select_radio', 'select_checkbox']:
                try:
                    time.sleep(1)
                    element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))
                    element.click()
                except (ElementNotInteractableException, TimeoutException, ElementClickInterceptedException):
                    time.sleep(1)
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    element.click()
            elif interaction_type in ['click_element']:
                try:
                    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by_locator, locator_value)))
                    time.sleep(1)
                    element.click()
                except ElementNotInteractableException:
                    driver.execute_script(
                        "arguments[0].scrollIntoView(true);", element)
                    element.click()
            elif interaction_type == 'get_text':
                try:
                    element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))
                    return element.text
                except AttributeError:
                    return ''
            else:
                raise ValueError(f"Unsupported interaction type: {interaction_type} with {by_locator}")
        return self.retry_action(perform_action, driver, by_locator, locator_value)

    def retry_action(self, action, driver, by_locator, locator_value, timeout=60, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                element = self.wait_for_element(driver, by_locator, locator_value, timeout)
                return action(driver, element)
            except (StaleElementReferenceException, ElementNotInteractableException):
                retries += 1
        raise RuntimeError(f"Failed to perform action after multiple retries")

    @keyword
    def split_the_locator(self, locator):
        locator_type, locator_value = locator.split(':', 1)
        by_locator = self.get_by_locator(locator_type)
        return by_locator.strip(), locator_value.strip()

    @keyword
    def set_past_date_and_close_calendar(self, driver: WebDriver, locator, delta, date_format='%d %b %Y', timeout=60):
        # Calculate the date two days from now
        
        current_date = datetime.now()
        two_days_due_date = current_date - timedelta(days=int(delta))
        formatted_date = two_days_due_date.strftime(date_format)

        # Enter the date into the input field
        by_locator, locator_value = self.split_the_locator(locator)
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))
        element.clear()
        element.send_keys(formatted_date)
        element.click()
        highlighted_date_locator = (By.XPATH, f"//div[@title='{formatted_date}']")
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable(highlighted_date_locator)).click()
        # Press Tab key to move focus to the next element
        # element.send_keys(Keys.TAB)

    @keyword
    def scroll_to_top_of_the_page(self, driver: WebDriver, timeout=60):
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        ).send_keys(Keys.CONTROL + Keys.HOME)
    
    @keyword
    def wait_for_element_visibility(self, driver: WebDriver, locator, timeout=60):
        try:
            by_locator, locator_value = self.split_the_locator(locator)
            time.sleep(1)
            WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by_locator, locator_value)))
            return True
        except TimeoutException:
            return False
    
    @keyword
    def wait_for_element_invisibility(self, driver: WebDriver, locator, timeout=60):
        try:
            by_locator, locator_value = self.split_the_locator(locator)
            time.sleep(1)  # Adding a small delay before checking for invisibility
            WebDriverWait(driver, timeout).until_not(EC.presence_of_element_located((by_locator, locator_value)))
            return True
        except TimeoutException:
            return False
        
    @keyword
    def extract_name(self, email):
        stripped_email = email.split('@')[0].strip()
        name = stripped_email.split('.')[-1]
        return name
    
    @keyword
    def navigate_to_the_latest_record(self, driver: WebDriver, locatorOne, document_num, locatorTwo, timeout=60):
        try:
            # Click before entering text in the text field
            by_locator, locator_value = self.split_the_locator(locatorOne)
            element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by_locator, locator_value)))
            element.click()
            element.send_keys(document_num)

            # Click enter key
            element.send_keys(Keys.ENTER)

            # Replace placeholder in search result with document_num
            search_record = locatorTwo.replace("placeholder", document_num)
            by_locator2, locator_value2 = self.split_the_locator(search_record)

            # Click if element is visible
            try:
                WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator2, locator_value2))).click()
            except NoSuchElementException:
                return f'No such element found: {locatorTwo}'
        except Exception as e:
            # Handle any other exceptions
            print(f"An error occurred: {e}")
            return False
        
    @keyword
    def select_document_type_from_drop_down(self, driver: WebDriver, locatorOne, locatorTwo, timeout=60):
        try:
            # Wait until the search bar filter dropdown is visible
            by_locator1, locator_value1 = self.split_the_locator(locatorOne)
            element1 = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by_locator1, locator_value1)))
            element1.click()
            # Wait until the document type element is visible
            by_locator2, locator_value2 = self.split_the_locator(locatorTwo)
            time.sleep(1)
            element2 = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by_locator2, locator_value2)))
            element2.click()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            # Take a screenshot here if needed
            return False
    
    @keyword
    def scroll_to_element_and_click(self, driver: WebDriver, locator, timeout=60):
        try:
            # Wait for the element to be clickable
            by_locator, locator_value = self.split_the_locator(locator)
            locator = self.wait_for_element(driver, by_locator, locator_value)
            element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by_locator, locator_value)))
            # Scroll to the element
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()

            # Click on the element
            element.click()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            # Take a screenshot here if needed
            return False
        
    @keyword    
    def click_elementOne_until_elementTwo_visibility(self, driver: WebDriver, element1, element2, max_attempts=2, timeout=60):
        try:
            for _ in range(max_attempts):
                try:
                    by_locator2, locator_value2 = self.split_the_locator(element2)
                    time.sleep(1)
                    if self.wait_for_element(driver, by_locator2, locator_value2, timeout):
                        return True  # Element 2 is visible, exit the loop
                    else:
                        by_locator1, locator_value1 = self.split_the_locator(element1)
                        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator1, locator_value1)))
                        time.sleep(1)
                        element.click()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    return False
            
            raise Exception("Maximum attempts reached. Element 2 is not visible.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    @keyword
    def wait_for_element(self, driver: WebDriver, locator_type, locator_value, timeout=60):
        try:
            element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((locator_type, locator_value)))
            if element.is_displayed:
                return True
            else:
                return False
        except Exception as e:
            print(f"An error occurred while checking element visibility: {e}")
            return False
        
    @keyword
    def click_element_until_radio_or_checkbox_checked(self, driver: WebDriver, locator, max_attempts=2, timeout=60):
        try:
            for _ in range(max_attempts):
                try:
                    # Wait for the element to be present or visible depending on the locator type
                    by_locator, locator_value = self.split_the_locator(locator)
                    time.sleep(1)
                    element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))

                    # Scroll to the element
                    time.sleep(1)
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    element.click()
                    # Check if the element is a radio button or checkbox and if it's checked
                    if element.get_attribute("type") in ["radio", "checkbox"] and (element.is_selected() or element.get_attribute("checked") == "true" or element.get_attribute("value") == "true"):
                        return True  # Element is checked, exit the loop
                    else:
                        continue
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue
            
            raise Exception("Maximum attempts reached. Element was not checked.")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    @keyword
    def set_future_date_with_delta_and_close_calendar(self, driver: WebDriver, locator, delta, date_format='%d %b %Y', timeout=60):
        # Calculate the date two days from now
        
        current_date = datetime.now()
        two_days_due_date = current_date + timedelta(days=int(delta))
        formatted_date = two_days_due_date.strftime(date_format)

        # Enter the date into the input field
        by_locator, locator_value = self.split_the_locator(locator)
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))
        element.clear()
        element.send_keys(formatted_date)
        element.click()
        highlighted_date_locator = (By.XPATH, f"//div[@title='{formatted_date}']")
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable(highlighted_date_locator)).click()

    @keyword
    def set_todays_date_and_close_calender(self, driver: WebDriver, locator, date_format="%d %b %Y", timeout=60):
        """Sets today's date in an input field with locator"""
        current_date = datetime.now()
        formatted_current_date = current_date.strftime(date_format)
        # Enter the date into the input field
        by_locator, locator_value = self.split_the_locator(locator)
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))
        element.clear()
        element.send_keys(formatted_current_date)
        element.click()
        highlighted_date_locator = (By.XPATH, f"//div[@title='{formatted_current_date}']")
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable(highlighted_date_locator)).click()


    @keyword
    def navigate_back(self, driver: WebDriver):
        driver.back()

    @keyword
    def replace_placeholders_and_return_locator(self, driver: WebDriver, locator, placeholder, value, timeout=30):
        by_locator, locator_value = self.split_the_locator(locator)
        locator_value = locator_value.replace(placeholder, value)  # Replace placeholder with value
        time.sleep(1)
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by_locator, locator_value)))
        return element

    @keyword
    def get_by_locator(self, locator_type):
        if locator_type == 'css':
            return By.CSS_SELECTOR
        elif locator_type == 'id':
            return By.ID
        elif locator_type == 'class':
            return By.CLASS_NAME
        elif locator_type == 'link_text':
            return By.LINK_TEXT
        elif locator_type == 'partial_link_text':
            return By.PARTIAL_LINK_TEXT
        elif locator_type == 'name':
            return By.NAME
        else:  # Default to XPath
            return By.XPATH
        
    @keyword
    def get_future_date_with_delta_in_PDT_timezone(self, delta, date_format):
        """
        The given function returns the date N no of days ahead of the current date in PDT format.
 
        Examples:
        | get future date with delta in PDT timezone |${days_to_be_added_to_current_date}    |date_format=%d%m%Y|
        | get future date with delta in PDT timezone |${days_to_be_added_to_current_date}    |date_format=%d/%m/%Y|
        | get future date with delta in PDT timezone |${days_to_be_added_to_current_date}    |date_format=%m/%b/%Y|
        | get future date with delta in PDT timezone |${days_to_be_added_to_current_date}    |date_format=%m/%d/%Y|
        """
 
        current_date = datetime.now()
        #the PDT IST date diffrence (-12:30 hours from IST)
        current_date_pdt = current_date - timedelta(hours=12, minutes=30)
        future_date_pdt = current_date_pdt + timedelta(days=int(delta))
        formatted_date = future_date_pdt.strftime(date_format)
        return formatted_date
   
    @keyword
    def get_future_date_with_delta_in_required_format(self, delta, date_format):
        """
        The given function returns the date N no of days ahead of the current date in PDT format.
 
        Examples:
        | get future date with delta in PDT timezone |${days_to_be_added_to_current_date}    | date_format=%d%m%Y |
        | get future date with delta in PDT timezone |${days_to_be_added_to_current_date}    | date_format=%d/%m/%Y |
        | get future date with delta in PDT timezone |${days_to_be_added_to_current_date}    | date_format=%m/%b/%Y |
        | get future date with delta in PDT timezone |${days_to_be_added_to_current_date}    | date_format=%m/%d/%Y |
        """
        current_date = datetime.now()
        delta_days_due_date = current_date + timedelta(days=int(delta))
        formatted_date = delta_days_due_date.strftime(date_format)
        return formatted_date
 
    @keyword
    def remove_leading_zeros_from_date(self, date_string):
        """
        The given function returns the date after removing the leading zeros.
 
        Examples:
        | get future date with delta in PDT timezone | ${date} |
        """
        day, month, year = date_string.split('/')
        day = str(int(day))
        month = str(int(month))
        year = str(int(year))
        formatted_date = f"{day}/{month}/{year}"    
        return formatted_date

    @keyword
    def remove_exsisting_date_value_with_backspace_rare_case(self, driver: WebDriver, locator):
        """
        The given function removes the default date from a text field after the past date has been apended infront of the default date.
        Caution: If the exsisting date value(dd mmm yyyy) is not cleared by using the element.clear() or Keys.BACK_SPACE then only we can utilise this function which can be a very rare case 
        Examples:
        | special case text field date value | ${driver} | id=date_text_field
        """
        iterator = 11
        by_locator, locator_value = self.split_the_locator(locator)
        element = WebDriverWait(driver, timeout=60).until(EC.element_to_be_clickable((by_locator, locator_value)))
        try:
            element = WebDriverWait(driver, timeout=60).until(EC.element_to_be_clickable((by_locator, locator_value)))
            time.sleep(1)
            element.click()
        except ElementNotInteractableException:
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", element)
            element.click()
        element.send_keys(Keys.ARROW_LEFT)    
        for _ in range(iterator):
                try:
                    element.send_keys(Keys.BACK_SPACE)
                except Exception as e:
                    print(f"An error occurred: {e}")            
    
    @keyword
    def get_desired_date_format_based_on_timezone(self, date_format, delta=0, timezone_offset='UTC-8'): 
        """
        The given function returns the date N number of days ahead of the current date in the specified timezone and format.
        If no timezone is specified, the default is UTC+0.

        Examples:
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%d%m%Y | timezone_offset=UTC+1 | 06082024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%m%d%Y | timezone_offset=UTC+1 | 08062024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%d/%m/%Y | timezone_offset=UTC+10:30 | 06/08/2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%m/%b/%Y | timezone_offset=UTC+9:30 | 06/Aug/2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%m/%d/%Y | timezone_offset=UTC-5 | 08/06/2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%d %b %Y | timezone_offset=UTC+4 | 06 Aug 2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%d %m %Y | timezone_offset=UTC+4 | 06 08 2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%Y-%m-%d | timezone_offset=UTC+0 | 2024-08-06 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%d-%m-%Y | timezone_offset=UTC+0 | 06-08-2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%d %B %Y | timezone_offset=UTC+0 | 06 August 2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%B %d, %Y | timezone_offset=UTC+0 | August 06, 2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%Y/%m/%d | timezone_offset=UTC+0 | 2024/08/06 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%A, %d %B %Y | timezone_offset=UTC+0 | Tuesday, 06 August 2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%y-%m-%d | timezone_offset=UTC+0 | 24-08-06 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%d %a %b %Y | timezone_offset=UTC+0 | 06 Tue Aug 2024 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%d-%b-%y | timezone_offset=UTC+0 | 06-Aug-24 |
        | get future date with delta in timezone | ${days_to_be_added_to_current_date} | date_format=%m-%d-%y | timezone_offset=UTC+0 | 08-06-24 |
        """
        # Get the timezone string from the offset
        timezone_str = TIMEZONE_OFFSET_MAP.get(timezone_offset, 'Etc/GMT')
        
        try:
            timezone = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            raise ValueError(f"Unknown timezone: '{timezone_str}'")
        
        current_date_in_timezone = datetime.now(timezone)
        future_date_in_timezone = current_date_in_timezone + timedelta(days=float(delta))
        formatted_date = future_date_in_timezone.strftime(date_format)
        return formatted_date