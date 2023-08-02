import pandas as pd
import jaydebeapi
import pyodbc
from sqls import SqlQueries
import numpy as np
from datetime import datetime as DT
import os
from dotenv import load_dotenv

dotenv_path = os.path.join('.env')
load_dotenv(dotenv_path)

server = os.environ.get('server_erp')
database = os.environ.get('database_erp')
username = os.environ.get('username_erp')
password = os.environ.get('password_erp')
cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

server = os.environ.get('server_kupol')
username = os.environ.get('username_kupol')
password = os.environ.get('password_kupol')
database = os.environ.get('database_kupol')
port = os.environ.get('port_kupol')
jdbc_driver = r'C:\Dev\compare_reports\jconnect\jconn4.jar'

conn = jaydebeapi.connect('com.sybase.jdbc4.jdbc.SybDriver', f'jdbc:sybase:Tds:{server}:{port}/{database}', {'user': username, 'password': password},
                          jdbc_driver)

columns_isrs_1c = ['Registrator','Registrator_name','Registrator_number','date_doc','Nomen_code','Name',	
                   'SO_Number','Seria','PN_1C', 'Qty_itog_1C','Status'
                    ]

columns_isrs_KUPOL = ['ISRDate','IDISR','StoreFrom','StoreTo','ELT_BN','ELT_ID','QTY_Released','PN_Kupol','SN','BalanceCode',
                      'KUPoLErrorText','GUID1C','KeyWordTranslation','Description',	
                      'StatusISR','StatusLog'
                      ]

StatusISR_to_exclude = ['Инструмент', 'Перемещение между одинаковыми складами', 'Собственник LMS', 'Собственник не НордСтар']

def get_isrs_from_1c():
    df = pd.read_sql_query(SqlQueries.get_isrs_from_1c(),cnxn,
                           dtype={'date_doc': pd.StringDtype()})
    df = pd.DataFrame(df, columns=columns_isrs_1c)
    df = df.fillna('null')
    df = df.groupby(['Registrator','Registrator_name','Registrator_number','date_doc','Nomen_code','Name',	
                   'SO_Number','Seria','PN_1C', 'Status'], as_index=False).sum('Qty_itog_1C')
    #excel = df.to_excel(r'isrs_from_1С.xlsx', engine='xlsxwriter')
    print("Данные из 1С получены")
    return df

def get_isrs_from_kupol():
    df = pd.read_sql_query(SqlQueries.get_isrs_from_kupol(),conn)
    print("Данные из КУПОЛ получены")
    #excel = df.to_excel(r'isrs_from_kupol.xlsx', engine='xlsxwriter')
    return df

def merge_isrs():
    df_isrs_1c = pd.DataFrame(get_isrs_from_1c(),columns=columns_isrs_1c)
    df_isrs_kupol = pd.DataFrame(get_isrs_from_kupol(),columns=columns_isrs_KUPOL)
    df_merge = df_isrs_1c.merge(df_isrs_kupol, left_on=['Nomen_code','SO_Number','Seria'], right_on=['GUID1C','IDISR','ELT_BN'], how='outer')
    #df_merge = df_merge.fillna({'date_doc':df_merge['ISRDate']})
    
    df_merge_first_sverka = df_merge[(df_merge['Seria'].notnull())&(df_merge['ELT_BN'].notnull())]

    df_isrs_1c_null = df_merge[df_merge['ELT_BN'].isnull()]
    df_isrs_1c_null = pd.DataFrame(df_isrs_1c_null, columns=columns_isrs_1c)
    df_isrs_kupol_null = df_merge[df_merge['Seria'].isnull()]
    df_isrs_kupol_null = pd.DataFrame(df_isrs_kupol_null, columns=columns_isrs_KUPOL)
    df_merge_null = df_isrs_1c_null.merge(df_isrs_kupol_null, left_on=['Nomen_code','date_doc','Seria'], right_on=['GUID1C','ISRDate','ELT_BN'], how='outer')

    df_merge_second_sverka = df_merge_null[(df_merge_null['Seria'].notnull())&(df_merge_null['ELT_BN'].notnull())]
            
    #df_concat_proverka = pd.concat([df_merge_first_sverka,df_merge_null])

    df_concat_isrs_1c_null = df_merge_null[df_merge_null['ELT_BN'].isnull()]
    df_concat_isrs_1c_null = pd.DataFrame(df_concat_isrs_1c_null, columns=columns_isrs_1c)
    df_concat_isrs_1c_null = df_concat_isrs_1c_null.groupby(['date_doc', 'PN_1C', 'Nomen_code', 'Status'], as_index=False).sum('Qty_itog_1C')
    df_concat_isrs_kupol_null = df_merge_null[df_merge_null['Seria'].isnull()]
    df_concat_isrs_kupol_null = pd.DataFrame(df_concat_isrs_kupol_null, columns=columns_isrs_KUPOL)
    df_concat_isrs_kupol_null = df_concat_isrs_kupol_null.groupby(['ISRDate', 'PN_Kupol', 'GUID1C', 'StatusISR', 'StatusLog','StoreFrom', 'StoreTo'], as_index=False).sum('QTY_Released')
    df_concat_merge_null = df_concat_isrs_1c_null.merge(df_concat_isrs_kupol_null, left_on=['Nomen_code','date_doc',], right_on=['GUID1C','ISRDate'], how='outer')

    df_concat_proverka = pd.concat([df_merge_first_sverka, df_merge_second_sverka, df_concat_merge_null])

    df_concat_proverka['date_doc_all'] = df_concat_proverka['date_doc'].fillna(df_concat_proverka['ISRDate'])
    df_concat_proverka['PN_all'] = df_concat_proverka['PN_1C'].fillna(df_concat_proverka['PN_Kupol'])
    df_concat_proverka['date_doc_all'] = pd.to_datetime(df_concat_proverka['date_doc_all'])
    df_concat_proverka['Qty_itog_1C'] = df_concat_proverka['Qty_itog_1C'].fillna(0)
    df_concat_proverka['QTY_Released'] = df_concat_proverka['QTY_Released'].fillna(0)
    df_concat_proverka['Proverka'] = df_concat_proverka.apply(lambda x: x['QTY_Released']-x['Qty_itog_1C'], axis=1)
    #df_concat_proverka['status_all'] = 
    df_concat_proverka = df_concat_proverka[~df_concat_proverka.StatusISR.isin(StatusISR_to_exclude)]
    #print("Стыковка завершена")
    excel = df_concat_proverka.to_excel(f'C:\DEV\compare_reports_KUPOL_1C\compare_reports_KUPOL_1C\save\isrs_report\isrs_sverka_from_kupol_{DT.now():%Y-%m-%d_%H-%M}.xlsx', engine='xlsxwriter')
    return excel


#print(get_isrs_from_1c())
#print(get_isrs_from_kupol())
print(merge_isrs())