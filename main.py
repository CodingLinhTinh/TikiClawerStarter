from TikiClawer import TikiClawer
from data import *
import time 

# Const
tiki_url = "https://tiki.vn/search?q="
product_txt_path = "data/data.txt"
file_path = "data/data.csv"

keywords = "balo"

tiki = TikiClawer()

tiki.getUrl(tiki_url + keywords)
productLinks = tiki.getProductLinks(productLinksXpath)

total_products = []

time.sleep(3)

for link in productLinks:
    # đi vào đường link sản phẩm đó
    tiki.getUrl(link)

    # lấy tên sản phẩm đó
    tiki.name = tiki.getProductInfo(name_xpath)
    
    if tiki.name == "Không tìm thấy sản phẩm":
        continue
    else:
        # lấy giá
        tiki.getPrices(prices_xpath)

        # lấy brand
        tiki.getBrand(brand_name_xpath)
        
        # lấy ảnh
        tiki.getImages()

        # lấy Description
        tiki.getDescription()

        tiki.appendtoTotalProduct(total_products)
        
print(len(total_products))

# Lưu file.txt ở đường dẫn nào đó
tiki.savingData(total_products, product_txt_path)

# lấy data từ data.txt
data = tiki.exportData(product_txt_path)

# chuyển thành file csv
tiki.createCSV(data, file_path)

tiki.stopProcess()
        

