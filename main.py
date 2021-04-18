import time
from selenium import webdriver
import math
from bs4 import BeautifulSoup


f = open("data.tsv","w")
headers = ["S.no","District","Institution","CovidBeds-Total","CovidBeds-Occupied","CovidBeds-Vacant","OxygenSupportedBeds-Total","OxygenSupportedBeds-Occupied",
"OxygenSupportedBeds-Vacant","NonOxygenSupportedBeds-Total","NonOxygenSupportedBeds-Occupied",
"NonOxygenSupportedBeds-Vacant","ICUBeds-Total","ICUBeds-Occupied","ICUBeds-Vacant","VENTILATOR-Total","VENTILATOR-Occupied","VENTILATOR-Vacant","Last-Updated","Remarks"]

f.write("\t".join(headers))
f.write('\n')

driver = webdriver.Chrome("chromedriver")
url = "https://stopcorona.tn.gov.in/beds.php"
driver.get(url)
numberOfPg = math.ceil(int(driver.find_element_by_id("dtBasicExample_info").text.split()[-2])//10)

def getData():
    body = driver.find_element_by_css_selector("tbody").get_attribute('innerHTML')
    
    soup = BeautifulSoup(body,'html.parser')
    HTML_data = soup.find_all("tr")
    data = []
    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)

    for i in data:
        i[-1] = i[-1].strip()
        i[-1] = i[-1].replace('\n','')
        f.write("\t".join(i))
        f.write('\n')

for _ in range(numberOfPg):
    #body = driver.find_element_by_css_selector("tbody").text
    getData()

    button = driver.find_element_by_css_selector(".paginate_button.next")
    button.click()

getData()
f.close()
driver.close()