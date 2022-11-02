from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException , StaleElementReferenceException , JavascriptException
from selenium.webdriver.chrome.options import Options

FileName = 'Price_Data.csv'
f1 = open(FileName , 'w' , encoding='utf-8')
headers = 'Maker$Model$Year$Type$Prices$ex_price$ex_date\n'
f1.write(headers)
chrome_options = Options()
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(options=chrome_options)

initial_i = 0
initial_j = 0
initial_k = 0
initial_l = 0
#initial_m = 0

# url = "https://www.hamrah-mechanic.com/carprice/"
cnt = 0

iteration = 0

def do(initial_i,initial_j,initial_k,initial_l):

    global iteration
    global cnt

    browser.get("https://www.hamrah-mechanic.com/carprice/")

    wait = WebDriverWait(browser,20)

    browser.maximize_window()

    maker = browser.find_element_by_name('ctl00$ContentPlaceHolder1$makeselect')
    model = browser.find_element_by_name('ctl00$ContentPlaceHolder1$modelselect')
    year = browser.find_element_by_name('ctl00$ContentPlaceHolder1$makeyearselect')
    type2 = browser.find_element_by_name('ctl00$ContentPlaceHolder1$typeSelect')

    makerlist = maker.find_elements_by_tag_name('option')

    for i in range(len(makerlist)):
        # if i==49:
        #     browser.quit()
        if i < initial_i:
            # print(str(i))
            continue
        if i==0:
            if makerlist[i].text.find('انتخاب') != -1 :
                continue
        makerlist[i].click()
        # print('maker = ----',makerlist[i].text)

        flag1 = 1
        while(flag1):
            try:
                wait.until(EC.element_located_to_be_selected((By.XPATH , '//*[@id="ContentPlaceHolder1_modelselect"]/option[1]')))
                flag1 = 0
            except TimeoutException as e:
                # url = browser.current_url
                do(i,0,0,0)
                pass

        modellist = model.find_elements_by_tag_name('option')
        for j in range(len(modellist)):
            if i == initial_i and j < initial_j :
                # print(str(i)+'-'+str(j))
                continue
            if j==0:
                if modellist[j].text.find('انتخاب') != -1 :
                    continue
            modellist[j].click()
            # print('model = ---',modellist[j].text)
            flag2 = 1
            while(flag2):
                try:
                    wait.until(EC.element_located_to_be_selected((By.XPATH , '//*[@id="ContentPlaceHolder1_makeyearselect"]/option[1]')))
                    flag2 = 0
                except TimeoutException as e:
                    # url = browser.current_url
                    do(i,j,0,0)
                    pass

            yearlist = year.find_elements_by_tag_name('option')
            for k in range(len(yearlist)):
                if i == initial_i and j == initial_j and k < initial_k :
                    # print(str(i)+'-'+str(j)+'-'+str(k))
                    continue
                if k==0:
                    if yearlist[k].text.find('انتخاب') != -1 :
                        continue
                yearlist[k].click()
                # print('year = --',yearlist[k].text)

                flag3 = 1
                while (flag3):
                    try :
                        wait.until(EC.element_located_to_be_selected((By.XPATH , '//*[@id="ContentPlaceHolder1_typeSelect"]/option[1]')))
                        flag3 = 0
                    except TimeoutException as e:
                        # url = browser.current_url
                        do(i,j,k,0)
                        pass

                typelist = type2.find_elements_by_tag_name('option')
                for l in range(len(typelist)):
                    if i == initial_i and j == initial_j and k == initial_k and l < initial_l:
                        # print(str(i)+'-'+str(j)+'-'+str(k)+'-'+str(l))
                        continue
                    if l==0:
                        if typelist[l].text.find('انتخاب') != -1:
                            continue

                    iteration += 1
                    if iteration % 2 == 0:
                        print('---------- iteration =',iteration ,' ----------')

                    if l==0:
                        typelist[l].click()
                    else:
                        yearlist[0].click()
                        yearlist[k].click()
                        typelist = type2.find_elements_by_tag_name('option')
                        typelist[l].click()


                    # print('type2 = -',typelist[l].text)

                    flag4 = 1
                    while(flag4):
                        try:
                            wait.until(EC.text_to_be_present_in_element((By.XPATH , '//*[@id="ContentPlaceHolder1_lblprice"]'),'تومان'))
                            flag4 = 0
                        except TimeoutException as e:
                            # url = browser.current_url
                            do(i,j,k,l)
                            pass
                    
                    prices = []

                    whiteprice = browser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_lblprice"]').text
                    prices.append(whiteprice)

                    # print('price =',whiteprice)

                    colors = {
                        'black' : browser.find_element_by_xpath('//*[@id="drpselectcolor2"]/span') ,
                        'silver' : browser.find_element_by_xpath('//*[@id="drpselectcolor3"]/span') ,
                        'red' : browser.find_element_by_xpath('//*[@id="drpselectcolor4"]/span') ,
                        'darkgrey' : browser.find_element_by_xpath('//*[@id="drpselectcolor5"]/span') ,
                        'other' : browser.find_element_by_xpath('//*[@id="drpselectcolor6"]/span')
                    }

                    for m in range(len(list(colors.keys()))):
                        if cnt != 2:
                            colors[list(colors.keys())[m]].click()

                        print(m)

                        # print('m---',m)
                        # print('cnt --- ',cnt)

                        if cnt == 2:
                            prices.append('Warning')

                        # print(prices)

                        flag5 = 1
                        
                        while(flag5 and cnt<2):
                            try:
                                wait.until(lambda browser : browser.execute_script('return jQuery.active') == 0)
                                price = browser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_lblprice"]').text
                                prices.append(price)
                                flag5 = 0
                            except TimeoutException as e:
                                cnt += 1
                                do(i,j,k,l)
                                pass
                        

                        if m+1 ==len(list(colors.keys())):
                            print('hereee')

                            flag6 = 1
                            while(flag6):
                                try:
                                    wait.until(lambda browser : browser.execute_script('return jQuery.active') == 0)
                                    flag6 = 0
                                    print('jqdone')
                                except TimeoutException as e:
                                    pass

                            for n in range (browser.execute_script('return Highcharts.charts.filter(item => item !== undefined)["length"]')):
                                print('heree',browser.execute_script('return Highcharts.charts.filter(item => item !== undefined)["length"]'))
                                try:
                                    try:
                                        js_script_1 = 'return Highcharts.charts.filter(item => item !== undefined)['+str(n)+'].series[0].yData'
                                        # print(js_script_1)
                                        js_script_2 = 'return Highcharts.charts.filter(item => item !== undefined)['+str(n)+'].series[0].xAxis["names"]'
                                        # print(js_script_2)
                                        # print('-----------')
                                        # print(browser.execute_script(js_script_1) != [20,60,20])

                                        wait.until(lambda browser: len(browser.execute_script(js_script_1)) != 0)
                                        # print('hereee')
                                        if browser.execute_script(js_script_1) == [20,60,20] and browser.execute_script('return Highcharts.charts.filter(item => item !== undefined)["length"]') == 1:
                                            ex_price = 'No_Chart'
                                            ex_date = 'No_Chart'
                                        if browser.execute_script(js_script_1) != [20,60,20]:
                                            ex_price = browser.execute_script(js_script_1)
                                            ex_date = browser.execute_script(js_script_2)
                                            # print('here')
                                        else:
                                            # print('pass')
                                            pass
                                    except JavascriptException as e:
                                        # print('jse')
                                        pass
                                except TimeoutException as e:
                                    print('---Timeout---')
                                    ex_price = 'Check This'
                                    ex_date = 'Check This'
                                    pass


                            # print('1111')

                            # try:
                            #     wait.until(lambda browser: len(browser.execute_script('return Highcharts.charts[Highcharts.charts["length"]-1].series[0].yData')) != 0)
                            #     # print(browser.execute_script('return Highcharts.charts[Highcharts.charts["length"]-1].series[0].yData'))
                            #     if browser.execute_script('return Highcharts.charts[Highcharts.charts["length"]-1].series[0].yData') != [20, 60, 20]:
                            #         # print('2222')
                            #         ex_price = browser.execute_script('return Highcharts.charts[Highcharts.charts["length"]-1].series[0].yData')
                            #         ex_date = browser.execute_script('return Highcharts.charts[Highcharts.charts["length"]-1].series[0].xAxis["names"]')
                            #     else:
                            #         # print('3333')
                            #         if browser.execute_script('return Highcharts.charts["length"]') > 1:
                            #             # print('4444')
                            #             ex_price = browser.execute_script('return Highcharts.charts[Highcharts.charts["length"]-2].series[0].yData')
                            #             ex_date = browser.execute_script('return Highcharts.charts[Highcharts.charts["length"]-2].series[0].xAxis["names"]')

                            # except TimeoutException as e:
                            #     ex_price = 'Check This'
                            #     ex_date = 'Check This'
                            #     pass


                    cnt = 0
                    print(str(i)+'-'+str(j)+'-'+str(k)+'-'+str(l))
                    String = makerlist[i].text + '$' + modellist[j].text + '$' + yearlist[k].text + '$' + typelist[l].text + '$' + str(prices) + '$' + str(ex_price) + '$' + str(ex_date) + '\n'
                    f1.write(String)

    browser.quit()

do(10,14,1,0)
    


