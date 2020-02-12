from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time


# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\where\you\download\the\chromedriver.exe')
driver = webdriver.Chrome()
driver.get("https://www.coursera.org/search?query=data%20science&")
# Click review button to go to the review section



csv_file = open('reviews.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
# Page index used to keep track of where we are.
index = 1
while True:
    try:
        time.sleep(.3)
        print("Scraping Page number " + str(index))
        index = index + 1
        # Find all the reviews on the page
        wait_review = WebDriverWait(driver, 10)
        reviews = wait_review.until(EC.presence_of_all_elements_located((By.XPATH,'//li[@class="ais-InfiniteHits-item"]')))

        for review in reviews:
            # Initialize an empty dictionary for each review
            review_dict = {}
            # Use relative xpath to locate the title, text, username, date, rating.
            # Once you locate the element, you can use 'element.text' to return its string.
            # To get the attribute instead of the text of each element, use 'element.get_attribute()
            try:

                title = review.find_element_by_xpath('.//h2[@class="color-primary-text card-title headline-1-text"]').text
                doc_ = review.find_element_by_xpath('.//a[@class="rc-DesktopSearchCard anchor-wrapper"]').get_attribute('href')
                wait_button = WebDriverWait(driver, 10)
                time.sleep(3)

                #doc_ = wait_button.until(EC.element_to_be_clickable((By.XPATH,'//a[@class="rc-DesktopSearchCard anchor-wrapper"]'))).get_attribute('href')
                #"""p_button.click()
                #acturl = browser.current_url
                #driver.back()"""
                driver.execute_script("window.open('');")
                time.sleep(3)
                # Switch to the new window
                driver.switch_to.window(driver.window_handles[1])
                driver.get(doc_)
                time.sleep(3)
                #content = review.find_element_by_xpath('.//div[@id="rc-MetatagsWrapper"]').text
                content = review.find_element_by_xpath('.//div[@class="Box_120drhm-o_O-displayflex_poyjc-o_O-wrap_rmgg7w"]').text
                """content = driver.find_element_by_tag_name("body").get_attribute("innerText")"""

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3.5)

            except:
                pass
            review_dict['title'] = title
            review_dict['content'] = content
            writer.writerow(review_dict.values())

            driver.execute_script("arguments[0].scrollIntoView();", review)
            time.sleep(.3)
                # OPTIONAL PART 1b
            # Click the read more button if it exists in order to collapse the text for the current review




        # Locate the next button on the page.
        wait_button = WebDriverWait(driver, 10)
        next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pagination_right_arrow_button"]')))
        next_button.click()
        time.sleep(.3)
    except Exception as e:
        print(e)
        csv_file.close()
        driver.close()
        break
