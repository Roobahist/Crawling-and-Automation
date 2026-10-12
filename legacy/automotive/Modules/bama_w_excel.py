FileName = 'Bama.csv'
f1 = open(FileName , 'w' , encoding='utf-8')
headers = 'Eng_Brand$Per_Brand$CarName$Year$Company$Updown$Namayandegi$Price\n'
f1.write(headers)

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
