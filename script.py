from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import csv
import time


class Scraper:
    def __init__(self, place, pages) -> None:
        self.place = place
        self.pages = pages
        self.search_name()

    def search_name(self):
        # Set up Chrome options for headless mode
        options = Options()
        options.add_argument('--headless')  
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        url = f"https://www.google.com/travel/search?q={self.place}"
        driver.get(url)

        wait = WebDriverWait(driver, 15)  

        data = {
            'name': [],
            'price': [],
            'link': [],
            'rating': []
        }

        def scrape_page_data():
            divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pjDrrc')))
            links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.PVOOXe')))

            for count, div in enumerate(divs):
                try:
                    name = div.find_element(By.CSS_SELECTOR, 'h2').text
                    price = div.find_element(By.CLASS_NAME, 'Q01V4b').text
                    link = links[count].get_attribute('href')

                    try:
                        rating = div.find_element(By.CLASS_NAME, 'ta47le').get_attribute('aria-label')
                    except:
                        rating = 'N/A' 

                    data['name'].append(name)
                    data['price'].append(price)
                    data['link'].append(link)
                    data['rating'].append(rating)
                except Exception as e:
                    print("Product details not found:", e)

            print(f"Scraped {len(data['name'])} items so far.")

        # Scrape the first page
        scrape_page_data()

        for page in range(eval(self.pages)):
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                time.sleep(1)
                next_button.click()
                time.sleep(3)  # Wait for the new page to load
                scrape_page_data()
            except Exception as e:
                print("No more pages to click through or Next button not found:", e)
                break  # Exit the loop if no more pages

        driver.quit()
        
        # Save data to a CSV file
        with open('hotels_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'Rating', 'Link'])
            for i in range(len(data['name'])):
                writer.writerow([data['name'][i], data['price'][i], data['rating'][i], data['link'][i]])

        print("Data saved to hotels_data.csv")
