from rounded100 import rounded
from show import show
import csv

where_dic = {
    '1'  : 'rang_gel_jlo_ras'  ,
    '2'  : 'rang_gel_jlo_chap' ,
    '3'  : 'rang_gel_aqab_ras' ,
    '4'  : 'rang_gel_aqab_chap' ,
    '5'  : 'rang_dar_jlo_ras' ,
    '6'  : 'rang_dar_jlo_chap' ,
    '7'  : 'rang_dar_aqab_ras' ,
    '8'  : 'rang_dar_aqab_chap' ,
    '9'  : 'rang_sandoq' ,
    '10' : 'rang_saqf'  ,
    '11' : 'rang_kapot'  ,
    '12' : 'taviz_gel_jlo_ras'  ,
    '13' : 'taviz_gel_jlo_chap'  ,
    '14' : 'taviz_gel_aqab_ras'  ,
    '15' : 'taviz_gel_aqab_chap'  ,
    '16' : 'taviz_dar_jlo_ras'  ,
    '17' : 'taviz_dar_jlo_chap'  ,
    '18' : 'taviz_dar_aqab_ras'  ,
    '19' : 'taviz_dar_aqab_chap'  ,
    '20' : 'taviz_sandoq'  ,
    '21' : 'taviz_saqf'  ,
    '22' : 'taviz_kapot' 
}

with open('KharabiHa\Base_Coef.csv','rt')as f:
    base_coef = csv.reader(f)
    for row in base_coef:
        a = row
    a = a[0]
    alist = a.split('$')

coef_dic = {
    'rang_gel_jlo_ras'  :float( alist[0]) ,
    'rang_gel_jlo_chap' :float( alist[1]) ,
    'rang_gel_aqab_ras' :float( alist[2]) ,
    'rang_gel_aqab_chap' :float( alist[3]) ,
    'rang_dar_jlo_ras' :float( alist[4]) ,
    'rang_dar_jlo_chap' :float( alist[5]) ,
    'rang_dar_aqab_ras' :float( alist[6]) ,
    'rang_dar_aqab_chap' :float( alist[7]) ,
    'rang_sandoq' :float( alist[8]) ,
    'rang_saqf'  :float( alist[9]) ,
    'rang_kapot'  : float(alist[10]) ,
    'taviz_gel_jlo_ras'  : float(alist[11]) ,
    'taviz_gel_jlo_chap'  : float(alist[12]) ,
    'taviz_gel_aqab_ras'  : float(alist[13]) ,
    'taviz_gel_aqab_chap'  : float(alist[14]) ,
    'taviz_dar_jlo_ras'  : float(alist[15]) ,
    'taviz_dar_jlo_chap'  : float(alist[16]) ,
    'taviz_dar_aqab_ras'  : float(alist[17]) ,
    'taviz_dar_aqab_chap'  : float(alist[18]) ,
    'taviz_sandoq'  : float(alist[19]) ,
    'taviz_saqf'  : float(alist[20]) ,
    'taviz_kapot': float(alist[21])  
}



def multiply (base_price , coef):
    # print(base_price*coef,'---->',rounded(base_price*coef))
    return rounded(base_price*coef)

                               
def calculate( price , where , where_dic , coef_dic):
    answer = price
    for i in where:
        answer = multiply (answer , coef_dic[where_dic[str(i)]])

    return show(answer)

# a = calculate(100000000 , [1,2,3,4] , where_dic , coef_dic)
# print(a)
# out = 89,800,000

            