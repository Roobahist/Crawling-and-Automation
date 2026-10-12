import csv

with open('KharabiHa\Base_Coef.csv','rt')as f:
    base_coef = csv.reader(f)
    for row in base_coef:
        a = row
    a = a[0]
    alist = a.split('$')

coef_dic = {
    'rang_gel_jlo_ras'  : alist[0] ,
    'rang_gel_jlo_chap' : alist[1] ,
    'rang_gel_aqab_ras' : alist[2] ,
    'rang_gel_aqab_chap' : alist[3] ,
    'rang_dar_jlo_ras' : alist[4] ,
    'rang_dar_jlo_chap' : alist[5] ,
    'rang_dar_aqab_ras' : alist[6] ,
    'rang_dar_aqab_chap' : alist[7] ,
    'rang_sandoq' : alist[8] ,
    'rang_saqf'  : alist[9] ,
    'rang_kapot'  : alist[10] ,
    'taviz_gel_jlo_ras'  : alist[11] ,
    'taviz_gel_jlo_chap'  : alist[12] ,
    'taviz_gel_aqab_ras'  : alist[13] ,
    'taviz_gel_aqab_chap'  : alist[14] ,
    'taviz_dar_jlo_ras'  : alist[15] ,
    'taviz_dar_jlo_chap'  : alist[16] ,
    'taviz_dar_aqab_ras'  : alist[17] ,
    'taviz_dar_aqab_chap'  : alist[18] ,
    'taviz_sandoq'  : alist[19] ,
    'taviz_saqf'  : alist[20] ,
    'taviz_kapot': alist[21]  
}

print(coef_dic)