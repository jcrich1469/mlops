from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from prefect import flow, task
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

PAGE_PROPERTIES = '//*[@id="l-searchResults"]'

POSTCODE='E5'


@task
def scrape_rightmove(): 
    chrome_options = Options() 
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    with webdriver.Chrome(service=service, options=chrome_options) as driver:

        driver.get('https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=OUTCODE%5E1859&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false')        
        properties_element = driver.find_element(By.XPATH, PAGE_PROPERTIES)
        properties = [p for p in get_properties(properties_element.get_attribute('outerHTML'))]
        

        # for all the next properties, 0-23 lists... 
    
        next_url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=OUTCODE%5E1859&index={}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords='
        max_index = int(driver.find_element(By.XPATH, '//span[@class="searchHeader-resultCount"]').text)     
        urls = [next_url.format(index) for index in range(24,max_index,24)]
          
        for url in urls:
            
            try:
                driver.get(url)

                properties_element = driver.find_element(By.XPATH, PAGE_PROPERTIES)
            
                properties += [p for p in get_properties(properties_element.get_attribute('outerHTML'))]
            
            except Exception as e:
                print(e)
        
        
        for p in properties:
            print(p)
        print(len(properties))

def get_properties(html_content):
    
    #print(html_content)
    html_soup = BeautifulSoup(html_content,'html.parser')
    # Use find_all to search for all tags with class 'myclass'
    

    property_cards = html_soup.find_all(class_="propertyCard")
    

    for property_card_e in property_cards:
        
        yield {'address':property_card_e.find(class_='propertyCard-address').text,'properties':property_card_e.find(class_='property-information').find_all('span').text,'price':property_card_e.find(class_='propertyCard-priceValue').text}



    
@flow
def rightmove_scraping_flow():
    scrape_rightmove()

# Execute the flow
if __name__ == "__main__":
    rightmove_scraping_flow()

