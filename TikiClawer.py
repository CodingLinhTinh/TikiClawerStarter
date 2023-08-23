## Model của app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from unidecode import unidecode
import uuid
import re
import ast
import time

chrome_driver_path = './chromedriver-win64/chromedriver-win64/chromedriver.exe'
# Create ChromeOptions instance and set window size
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--window-size=800,600')

class TikiClawer:
    def __init__(self) -> object:
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
        self.sleep_time = 3 # giây
        self.search_input_xpath = '//*[@id="main-header"]/div/div/div[2]/div[1]/div[1]/div/div/input'
        
        # Khởi tạo 
        self.name = ""
        self.type_txt = ""
        self.cat_txt = "Balo"
        self.post_name = ""
        self.discounted_price = ""
        self.regular_price = ""
        self.brand = ""
        self.image = ""
        self.description = ""
        
        
    # Lấy link
    def getUrl(self, url):
        self.driver.get(url)
        
    # Lấy link sản phẩm
    def getProductLinks(self, xpath):
        productLinks = self.driver.find_elements(By.XPATH, xpath)
        productLinks = [link.get_attribute("href") for link in productLinks]
        return productLinks
    
    # Dừng tiến trình    
    def stopProcess(self):
        self.driver.quit()
        
    # Nhập text muốn tìm
    def sendSearchInput(self, text):
        search_input = self.driver.find_element(By.XPATH, self.search_input_xpath)
        
        search_input.send_keys(text)
        search_input.send_keys(Keys.ENTER)
        time.sleep(self.sleep_time)
        
    # Trả về 1 list các sản phẩm chứa tên sản phẩm 
    def getListProduct(self, xapth):
        list = self.driver.find_elements(By.XPATH, xapth)
        list_names = [ i.text for i in list ]
        return list_names
    
    # Trả về 1 text của 1 web element
    def getProductInfo(self, xpath):
        info = self.driver.find_elements(By.XPATH, xpath)
        if info:
            info = self.driver.find_element(By.XPATH, xpath)
            return info.text
        else:
            return "Không tìm thấy sản phẩm"
    
    # Tạo ID cho sản phẩm
    def generate_item_id(self):
        timestamp = int(time.time() * 1000)
        uuid_str = str(uuid.uuid4())
        item_id = f"{timestamp}-{uuid_str}"
        return item_id
        
    
    # Lấy hình
    def getImages(self):
        images = ""
        imagesEL = self.driver.find_elements(By.XPATH, '//a[contains(@data-view-id, "pdp_main_view_photo")]')
        
        for el in imagesEL:
            el.click()
            imageContainer = self.driver.find_element(By.XPATH, '//div[contains(@class, "thumbnail")]').get_attribute('innerHTML')
            if re.search(r'<picture class="webpimg-container">', imageContainer):
                images = images + re.search(r'src="([^"]+)"', imageContainer).group(1) + ", "
            self.images = images
            
    # Lấy Mô tả
    def getDescription(self):
        self.description = self.driver.find_element(By.XPATH,'//div[contains(@class, "ToggleContent__View-sc-1dbmfaw-0 wyACs")]').get_attribute("innerHTML")
    
    # Trả về 1 list prices
    def getPrices(self, xpath):
        # lấy giá
        try:
            flash_sale = self.driver.find_elements(By.CLASS_NAME, "flash-sale-price")
            if flash_sale:
                flash_sale_regular_price_xpath = '//*[@id="__next"]/div[1]/main/div[3]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/div/span[1]'
                flash_sale_discount_price_xpath = '//*[@id="__next"]/div[1]/main/div[3]/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/div[1]/span'

                self.discounted_price = self.getProductInfo(flash_sale_discount_price_xpath)
                self.regular_price = self.getProductInfo(flash_sale_regular_price_xpath)
            else: 
                prices = self.getListProduct(xpath)
                # 0: giá khuyến mãi, 1: giá gốc
                # nếu len == 1 cho chỉ có giá gốc
                if len(prices) == 1:
                    self.regular_price = prices[0].replace(".", " ")
                    self.discounted_price = ""
                    
                # nếu len == 3 là có % nên pop()
                elif len(prices) == 3:
                    prices.pop()
                    self.discounted_price = prices[0].replace(".", " ")
                    self.regular_price = prices[1].replace(".", " ")
                else:
                    self.discounted_price = prices[0].replace(".", " ")
                    self.regular_price = prices[1].replace(".", " ")

        except Exception as e:
            print(e)
    
    # Lấy tên thương hiệu
    def getBrand(self, xpath):
        try:
            brand_name = self.driver.find_element(By.XPATH, xpath) 
            self.brand = brand_name.text
        except Exception as e:
            pass
    
    # slug sản phẩm
    def createPostName(self, txt):
        self.post_name = txt.lower()
        self.post_name = self.post_name.replace("- ","")
        self.post_name = self.post_name.replace("+ ","")
        self.post_name = self.post_name.replace(", "," ")
        self.post_name = self.post_name.replace("/ ", " ")
        self.pot_name = self.post_name.replace("/", " ")
        self.post_name = self.post_name.replace(" ", "-")
        self.post_name = self.post_name.replace("--", "-")
        self.post_name = self.post_name.replace("|-", "")
    
    # Lưu vào 1 list
    def appendtoTotalProduct(self, list):
        try:
            list.append({
                "ID": self.generate_item_id(),
                "Type": "simple",
                "SKU": "",
                "Name": self.name,
                "Published": 1,
                "Is featured?": 0,
                "Visibility in catalog": "visible",
                "Short description": "",
                "Description": self.description,
                "Date sale price start": "",
                "Date sale price ends": "",
                "Tax status": "taxable",
                "Tax class": "Standard",
                "In stock?": 1,
                "Stock": 100,
                "Low stock amount": "",
                "Backorders allowed?": 0,
                "Sold individually?": 0,
                "Weight (kg)": 0.1,
                "Length (cm)": "",
                "Width (cm)": "",
                "Height (cm)": "",
                "Allow customer reviews?": 1,
                "Purchase note": "",
                "Sale price": self.discounted_price,
                "Regular price": self.regular_price,
                "Categories": self.cat_txt,
                "Tags": self.post_name,
                "Shipping class": "Standard",
                "Images": self.image,
                "Download limit": "",
                "Download expiry days": "",
                "Parent": "",
                "Grouped products": "",
                "Upsells": "",
                "Cross-sells": "",
                "External URL": "",
                "Button text": "",
                "Position": 0,
                "Meta: content_width": "default_width",
                "Attribute 1 name": "Brand",
                "Attribute 1 value(s)": self.brand,
                "Attribute 1 visible": 1,
                "Attribute 1 global": 1,
                })
            
            print(self.name + " Added!")
        except Exception as e:
            pass
    
    # Lưu tên các sản phẩm trong 1 file.txt
    def savingData(self, data, path):
        with open(path, "a+", encoding="utf-8") as file:
            file.seek(0) # con trỏ sẽ được đưa về vị trí đầu tiên của tệp, cho phép đọc dữ liệu từ đầu tệp mà không cần mở lại tệp
            existing_data = file.read().splitlines()
            for element in data:
                if str(element) not in existing_data:
                    file.write(str(element) + "\n")
        print(path + " created or updated!")


    
    # Dựa vào các data trong data.txt
    def exportData(self, path):
        list = []
        with open(path, 'r', encoding="utf-8") as file:

            for line in file:
                line = line.strip("\n")
                your_dict = ast.literal_eval(line)
                list.append(your_dict)
        return list 
    
    def createCSV(self, data, path):
        try:
            # Convert list of dictionaries to pandas dataframe
            df = pd.DataFrame(data)

            # Save dataframe to CSV file
            df.to_csv(path, sep="@", index=False)

        except Exception as e:
            pass 
    
     
    
    
        
		