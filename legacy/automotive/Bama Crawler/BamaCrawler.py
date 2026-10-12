import requests
from bs4 import BeautifulSoup as Soup
from random import random

FileName = 'Bama.csv'
f1 = open(FileName , 'w' , encoding='utf-8')
headers = 'Eng_Brand$Per_Brand$CarName$Year$Company$Updown$Namayandegi$Price\n'
f1.write(headers)

def show(x):                  
    x = str(x)                
    lis = []                  
    for i in range(len(x)):   
        lis.append(x[i])      
    time = len(x)//3          
    z = 0                     
    for i in range(1,time+1): 
        lis.insert(-3*i-z,',')
        z += 1                
    answer = ''               
    for i in range(len(lis)): 
        answer += str(lis[i]) 
    if answer[0] == ',':      
        answer = answer[1:]   
    return answer

def rounded(x):
    flag = 0
    x = str(int(x))
    first = x[:-6]
    second = x[-6:]
    lower = str(second[0])+'00000'
    if second[0]=='9':
        flag = 1
        upper = '1000000'
    else:
        upper = str(int(second[0])+1)+'00000'
    upper_res = int(upper)-int(second)
    lower_res = int(second)-int(lower)
    answer = 0
    
    if second == '000000':
        answer = int(x)
    elif lower_res>upper_res:
        if flag==0:
            answer = int(first + upper)
        else:
            answer = int(first[:-1] + str(int(first[-1])+1) + '000000')
    elif lower_res<=upper_res:
        answer = int(first + lower)
    return answer

def change(x):
    rand = 100 + random()-0.5
    changed_price = x*rand/100
    answer = show(rounded(int(changed_price)))
    return answer

def do():
    response = requests.get('https://bama.ir/price')
    soup = Soup(response.content , 'lxml')

    container = soup.find('div',{'class':'sefr-price-list'})
    brands = container.find_all('section')

    per_eng_name = {
        'ام جی' : 'mg' ,
        'ام وی ام' : 'mvm' ,
        'آمیکو' : 'amico' ,
        'ب ام و' : 'bmw' ,
        'بایک' : 'baic' ,
        'برلیانس' : 'brelianse' ,
        'بسترن' : 'bestern' ,
        'بنز' : 'benz' ,
        'بورگوارد' : 'borgvard' ,
        'بی وای دی' : 'byd' ,
        'بیسو' : 'bisu' ,
        'پراید' : 'pride' ,
        'پژو' : 'peugeot' ,
        'پورشه' : 'porche' ,
        'تویوتا' : 'toyota' ,
        'تیبا' : 'tiba' ,
        'جک' : 'jac' ,
        'جیلی' : 'geelee' ,
        'چانگان' : 'changan' ,
        'چری' : 'cheri' ,
        'دامای' : 'domy' ,
        'دانگ فنگ' : 'dongfeng' ,
        'دنا' : 'dena' ,
        'دی اس' : 'ds' ,
        'رانا' : 'runna' ,
        'رنو' : 'renault' ,
        'ریگان' : 'rigan' ,
        'زوتی' : 'zotti' ,
        'سانگ یانگ' : 'sungyung' ,
        'ساینا' : 'saina' ,
        'سمند' : 'samand' ,
        'سوزوکی' : 'suzuki' ,
        'سیتروئن' : 'citroen' ,
        'فوتون' : 'photon' ,
        'فولکس' : 'vw' ,
        'کاپرا' : 'capra' ,
        'کوییک' : 'quick' ,
        'کیا' : 'kia' ,
        'لکسوس' : 'lexus' ,
        'لیفان' : 'lifan' ,
        'مزدا' : 'mazda' ,
        'میتسوبیشی' : 'mitsubishi' ,
        'مینی' : 'mini' ,
        'نیسان' : 'nissan' ,
        'وانت' : 'vanet' ,
        'ولوو' : 'volvo' ,
        'هاوال' : 'haval' ,
        'هایما' : 'haima' ,
        'هن تنگ' : 'hantang' ,
        'هیوندای' : 'hyundai' 
    }

    list_of_dicts = []

    for i in range(len(brands)):
        per_brand = brands[i].find('div',{'class':'price-list-brand-name'}).a.text.split('قیمت خودرو ')[1]
        cars = brands[i].ul.find_all('li')

        for j in range(len(cars)):
            # print(i,'--',j)
            car = cars[j]
            car_name = car.span.text.strip()
            year = car.small.text.strip()
            company = car.find('small',{'class':'sefr-company'}).text.strip().replace('،','').strip()
            namayandegi = '0'
            if car.find('small',{'class':'sefr-bazaar'}).text.find('نمایندگی') != -1:
                namayandegi = '1'
            price = car.find('small',{'class':'sefr-price'}).text
            price = change(int(price.split(' تومان')[0].replace(',','')))+' تومان'
            if str(type(car.find('small',{'class':'sefr-updown zero'}))) != "<class 'NoneType'>":
                updown = car.find('small',{'class':'sefr-updown zero'}).text
            elif str(type(car.find('small',{'class':'sefr-updown price-up'}))) != "<class 'NoneType'>":
                updown = car.find('small',{'class':'sefr-updown price-up'}).text
            elif str(type(car.find('small',{'class':'sefr-updown price-down'}))) != "<class 'NoneType'>":
                updown = '-' + str(car.find('small',{'class':'sefr-updown price-down'}).text)
            eng_brand = per_eng_name[per_brand]

            Temp = {
                'Eng_Brand' : eng_brand ,
                'Per_Brand' : per_brand ,
                'Car_Name' : car_name ,
                'Year' : year ,
                'Company' : company ,
                'UpDown' : updown ,
                'Namayandegi' : namayandegi ,
                'Price' : price
            }

            list_of_dicts.append(Temp)
    return list_of_dicts

def write_to_excel(list_of_dicts):

    for i in range(len(list_of_dicts)):
        Eng_Brand = list_of_dicts[i]['Eng_Brand']
        Per_Brand = list_of_dicts[i]['Per_Brand']
        Car_Name = list_of_dicts[i]['Car_Name']
        Year = list_of_dicts[i]['Year']
        Company = list_of_dicts[i]['Company']
        UpDown = list_of_dicts[i]['UpDown']
        Namayandegi = list_of_dicts[i]['Namayandegi']
        Price = list_of_dicts[i]['Price']

        f1.write(Eng_Brand + '$' + Per_Brand + '$' + Car_Name + '$' + Year + '$' + Company + '$' + UpDown + '$' + Namayandegi + '$' + Price + '\n')

write_to_excel(do())