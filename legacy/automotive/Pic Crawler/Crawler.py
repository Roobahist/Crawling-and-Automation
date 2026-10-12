from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

# def initialize():
FileName = 'PicInfo.csv'
f1 = open(FileName , 'w' , encoding='utf-8')
headers = 'Maker$Model$PicName\n'
f1.write(headers)

Driver = webdriver.Chrome()
Driver.get('https://www.hamrah-mechanic.com/car-inspection/')
Driver.maximize_window()
# ignored_exceptions=[StaleElementReferenceException,TimeoutException]

wait = WebDriverWait(Driver,60,ignored_exceptions=(StaleElementReferenceException,TimeoutException))
print(wait._ignored_exceptions)

Maker = Driver.find_element_by_id('makeselect')
Model = Driver.find_element_by_id('modelselect')
Year = Driver.find_element_by_id('makeyearselect')
Type = Driver.find_element_by_id('typeSelect')
ID = 1


# def do():
Makerlist = Maker.find_elements_by_tag_name('option')[1:]

for i in range(len(Makerlist)):
    time.sleep(1)
    Makerlist[i].click()
    Modellist = []
    print('i',Makerlist[i].text)
    # time.sleep(1)
    # wait.until(lambda Driver : Driver.find_element_by_xpath('//*[@id="modelselect"]/option[1]') != None)
    if (wait.until(EC.element_located_to_be_selected((By.XPATH,'//*[@id="modelselect"]/option[1]')))):
    # if (wait.until(EC.refreshed(EC.staleness_of(Driver.find_element((By.XPATH,'//*[@id="modelselect"]/option[1]')))))):
        Modellist = Model.find_elements_by_tag_name('option')[1:]
    else:
        Driver.refresh()
        wait.until(EC.element_located_to_be_selected((By.XPATH,'//*[@id="modelselect"]/option[1]')))
        Modellist = Model.find_elements_by_tag_name('option')[1:]
        print('refresh')
        

    for j in range(len(Modellist)):
        Modellist[j].click()
        Yearlist = []
        print('j',Modellist[j].text)
        # time.sleep(1)
        # wait.until(lambda Driver : Driver.find_element_by_xpath('//*[@id="makeyearselect"]/option[1]') != None)
        if (wait.until(EC.element_located_to_be_selected((By.XPATH,'//*[@id="makeyearselect"]/option[1]')))):
        # if (wait.until(EC.refreshed(EC.staleness_of(Driver.find_element((By.XPATH,'//*[@id="makeyearselect"]/option[1]')))))):
            Yearlist = Year.find_elements_by_tag_name('option')[1:]
        else:
            Driver.refresh()
            wait.until(EC.element_located_to_be_selected((By.XPATH,'//*[@id="makeyearselect"]/option[1]')))
            Yearlist = Year.find_elements_by_tag_name('option')[1:]
            print('refresh')

        if len(Yearlist) == 0:
            ID += 1
            continue

        Yearlist[0].click()

        if (wait.until(EC.element_located_to_be_selected((By.XPATH,'//*[@id="typeSelect"]/option[1]')))):
            # if (wait.until(EC.refreshed(EC.staleness_of(Driver.find_element((By.XPATH,'//*[@id="typeSelect"]/option[1]')))))):
            Typelist = Type.find_elements_by_tag_name('option')[1:]
        else:
            Driver.refresh()
            wait.until(EC.element_located_to_be_selected((By.XPATH,'//*[@id="typeSelect"]/option[1]')))
            Typelist = Type.find_elements_by_tag_name('option')[1:]
            print('refresh')

        Typelist[0].click()

        tehran = Driver.find_element_by_xpath('//*[@id="CitySelect"]/option[7]')
        tehran.click()

        flag=1
        while(flag):
            try:
                if (wait.until(lambda Driver : Driver.find_element_by_xpath('//*[@id="carimage"]').is_displayed() != False)):
                    time.sleep(4)
                    image = Driver.find_element_by_xpath('//*[@id="carimage"]')
                    image_name = str(ID)+'.png'
                    image.screenshot(image_name)
                    ID += 1
                    flag = 0
                else:
                    Driver.refresh()
                    (wait.until(lambda Driver : Driver.find_element_by_xpath('//*[@id="carimage"]').is_displayed()))
                    time.sleep(4)
                    image = Driver.find_element_by_xpath('//*[@id="carimage"]')
                    image_name = str(ID)+'.png'
                    image.screenshot(image_name)
                    ID += 1
                    flag = 0
            except StaleElementReferenceException as e:
                print('Stale')
                pass
        String = Makerlist[i].text + '$' + Modellist[j].text + '$' + image_name + '\n'
        f1.write(String)
