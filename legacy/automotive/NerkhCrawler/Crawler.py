from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

# def initialize():
FileName = 'HazineKarshenasi.csv'
f1 = open(FileName , 'w' , encoding='utf-8')
headers = 'ID$Maker$Model$Year$Type$Price\n'
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
# return Driver,Maker,Model,Year,Type

# def do():
Makerlist = Maker.find_elements_by_tag_name('option')[38:]

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


        for k in range(len(Yearlist)):
            Yearlist[k].click()
            Typelist = []
            print('k',Yearlist[k].text)
            # time.sleep(1)
            # wait.until(lambda Driver: Driver.find_element_by_xpath('//*[@id="typeSelect"]/option[1]') != None)
            if (wait.until(EC.element_located_to_be_selected((By.XPATH,'//*[@id="typeSelect"]/option[1]')))):
            # if (wait.until(EC.refreshed(EC.staleness_of(Driver.find_element((By.XPATH,'//*[@id="typeSelect"]/option[1]')))))):
                Typelist = Type.find_elements_by_tag_name('option')[1:]
            else:
                Driver.refresh()
                wait.until(EC.element_located_to_be_selected((By.XPATH,'//*[@id="typeSelect"]/option[1]')))
                Typelist = Type.find_elements_by_tag_name('option')[1:]
                print('refresh')


            for h in range(len(Typelist)):
                Typelist[h].click()
                print('h',Typelist[h].text)
                # time.sleep(1)
                # wait.until(lambda Driver: Driver.find_element_by_xpath('//*[@id="CitySelect"]/option[1]') != None)
                # wait.until(EC.element_located_to_be_selected((By.XPATH,'//*[@id="CitySelect"]/option[7]')))
                tehran = Driver.find_element_by_xpath('//*[@id="CitySelect"]/option[7]')
                tehran.click()

                price = ''
                flag=1
                while(flag):
                    try:
                        if (wait.until(lambda Driver : Driver.find_element_by_xpath('//*[@id="lblHazine"]').text != '')):
                            price = Driver.find_element_by_xpath('//*[@id="lblHazine"]').text
                            flag = 0
                        else:
                            Driver.refresh()
                            wait.until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="lblHazine"]'),'تومان'))
                            price = Driver.find_element_by_xpath('//*[@id="lblHazine"]').text
                            print('refresh')
                            flag = 0
                    except StaleElementReferenceException as e:
                        print('Stale')
                        pass


                String = str(ID) + '$' + Makerlist[i].text + '$' + Modellist[j].text + '$' + Yearlist[k].text + '$' + Typelist[h].text + '$' + price + '\n'
                f1.write(String)

                ID += 1

# do()