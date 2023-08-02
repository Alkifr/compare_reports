import pandas as pd
import jaydebeapi
import pyodbc
from sqls import SqlQueries
import numpy as np
from datetime import datetime as DT
import time
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

#cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='cp1252')
#cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='cp1252')
#cnxn.setencoding(encoding='cp1252')
#cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding="utf-8")

server = os.environ.get('server_kupol')
username = os.environ.get('username_kupol')
password = os.environ.get('password_kupol')
database = os.environ.get('database_kupol')
port = os.environ.get('port_kupol')
jdbc_driver = r'C:\Dev\compare_reports\jconnect\jconn4.jar'

conn = jaydebeapi.connect('com.sybase.jdbc4.jdbc.SybDriver', f'jdbc:sybase:Tds:{server}:{port}/{database}', {'user': username, 'password': password},
                          jdbc_driver)

columns1c = ['Registrator', 'date_doc', 'SO_Number', 'Seria', 'PN', 'Nomen_code', 'qty', 'order_', 'Analitika_rashodov', 'registration_number', 'users']
columnsKupol = ['name_store', 'elt_bn', 'elt_id', 'pn', 'GUID1C', 'qty_released', 'qty_restocked', 'idsof_', 'SOFdate_', 'registrationnumber', 'statusSO', 'StatusLog', 'KUPoLErrorText']
columnsKupol_x = ['name_store_x', 'elt_bn_x', 'elt_id_x', 'pn_x', 'qty_released_x', 'qty_restocked_x', 'idsof__x', 'SOFdate__x', 'registrationnumber_x', 'statusSO_x', 'StatusLog_x','KUPoLErrorText_x']
columns_all = ['Registrator', 'date_doc', 'SO_Number', 'Seria', 'PN', 'qty', 'order_', 'Analitika_rashodov', 'registration_number', 'users',
               'name_store', 'elt_bn', 'elt_id', 'pn', 'qty_released', 'qty_restocked', 'idsof_', 'SOFdate_', 'registrationnumber', 'statusSO', 'StatusLog','KUPoLErrorText']

def decode_sketchy_utf16(raw_bytes):
    s = raw_bytes.decode("utf-16le", "ignore")
    try:
        n = s.index('\u0000')
        s = s[:n]  # respect null terminator
    except ValueError:
        pass
    return s

prev_converter = cnxn.get_output_converter(pyodbc.SQL_WVARCHAR)
cnxn.add_output_converter(pyodbc.SQL_WVARCHAR, decode_sketchy_utf16)
#col_info = crsr.columns("Clients").fetchall()
#cnxn.add_output_converter(pyodbc.SQL_WVARCHAR, prev_converter)  # restore previous behaviour


def get_1c_regist():
    df = pd.read_sql_query(SqlQueries.get_1c_registr(), con=cnxn, 
                           dtype={'date_doc': pd.StringDtype()})
    #df = pd.DataFrame(df, columns=columns1c)
    #excel = df.to_excel(r'output_regist_1c_to_excel.xlsx', engine='xlsxwriter')
    print('1С выгружен успешно')
    #excel = df.to_excel(r'output_regist_1c_to_excel.xlsx', engine='xlsxwriter')
    return df
    #return excel

def get_kupol_so():
    df = pd.read_sql_query(SqlQueries.get_queries_so_from_kupol(), con=conn)
    #df = pd.DataFrame(df, columns=columnsKupol)
    #excel = df.to_excel(r'output_kupol_so_to_excel.xlsx', engine='xlsxwriter')
    print('KUPOL выгружен успешно')
    #excel = df.to_excel(r'output_kupol_so_to_excel.xlsx', engine='xlsxwriter')
    return df
    #return excel

def merge():
    df1 = pd.DataFrame(get_1c_regist(), columns=columns1c)
    df2 = pd.DataFrame(get_kupol_so(), columns=columnsKupol)
    merges = df1.merge(df2, left_on = ['Seria', 'SO_Number','registration_number', 'date_doc'], right_on = ['elt_bn', 'idsof_','registrationnumber', 'SOFdate_'], how = 'outer')
    df3 = merges[merges['elt_bn'].notnull()] #оставляю только где заполнен elt_bn
    df3 = df3[df3['Registrator'].isnull()] #убираю нулевые значения из регистра 1С
    df3 = pd.DataFrame(df3, columns=columnsKupol)
    merges2 = merges.merge(df3,left_on = ['Seria', 'registration_number', 'date_doc'], right_on=['elt_bn', 'registrationnumber', 'SOFdate_'], how='left')
    merges2 = merges2.fillna({'name_store_x': merges2['name_store_y'], 'elt_bn_x': merges2['elt_bn_y'], 'elt_id_x': merges2['elt_id_y'], 
                            'pn_x': merges2['pn_y'], 'qty_released_x': merges2['qty_released_y'], 'qty_restocked_x': merges2['qty_restocked_y'],
                            'idsof__x': merges2['idsof__y'], 'SOFdate__x': merges2['SOFdate__y'], 'registrationnumber_x': merges2['registrationnumber_y'],
                            'statusSO_x': merges2['statusSO_y'], 'StatusLog_x': merges2['StatusLog_y'], 'KUPoLErrorText_x': merges2['KUPoLErrorText_y']}) #делаю замену данных, что если пусто, то бери справа, если нет, то оставляй значение
    merges2 = merges2.rename(columns={'name_store_x':'name_store', 'elt_bn_x':'elt_bn', 'elt_id_x':'elt_id', 'pn_x':'pn', 'qty_released_x':'qty_released',
                                      'qty_restocked_x':'qty_restocked', 'idsof__x':'idsof_', 'SOFdate__x':'SOFdate_', 'registrationnumber_x':'registrationnumber',
                                      'statusSO_x':'statusSO', 'StatusLog_x':'StatusLog', 'KUPoLErrorText_x':'KUPoLErrorText'}) #делаю ренэйм столбцов
    merges2 = pd.DataFrame(merges2, columns=columns_all) #отрезаю лишние столбцы
    df4 = merges2[merges2['elt_bn'].notnull()] #оставляю только где заполнен elt_bn
    df4 = df4[df4['Registrator'].notnull()] #оставляю только где заполнен Registrator
    df4 = pd.DataFrame(df4, columns=columnsKupol)
    df4 = df4.rename(columns={'name_store':'name_store_x', 'elt_bn':'elt_bn_x',	'elt_id':'elt_id_x', 'pn':'pn_x', 'qty_released':'qty_released_x',
                              'qty_restocked':'qty_restocked_x', 'idsof_':'idsof__x', 'SOFdate_':'SOFdate__x', 'registrationnumber':'registrationnumber_x',	
                              'statusSO':'statusSO_x', 'StatusLog':'StatusLog_x', 'KUPoLErrorText':'KUPoLErrorText_x'})
    merges3 = merges2.merge(df4, left_on = ['elt_bn', 'pn', 'idsof_','registrationnumber', 'SOFdate_'], 
                            right_on = ['elt_bn_x', 'pn_x', 'idsof__x','registrationnumber_x', 'SOFdate__x'], how = 'left')
    df5 = merges3[(merges3['elt_bn_x'].isnull())&(merges3['Registrator'].isnull())]
    df5 = pd.DataFrame(df5, columns=columns_all)
    df6 = merges3[merges3['Registrator'].notnull()]
    df6 = pd.DataFrame(df6, columns=columns_all)
    df7_concat = pd.concat([df6,df5]) #набор данных после второй стыковки
    df7_concat_sostikov = df7_concat[(df7_concat['Registrator'].notnull())&(df7_concat['elt_bn'].notnull())] #Набор данных состыкованных только после второй стыковки
    df8 = df7_concat[(df7_concat['Registrator'].notnull())&(df7_concat['elt_bn'].isnull())]
    df8 = pd.DataFrame(df8, columns=columns1c)
    df8_group = df8.groupby(["Registrator", "date_doc", "Seria", "PN", "order_", "Analitika_rashodov", "registration_number", "users"], as_index=False).sum()
    df9 = df7_concat[(df7_concat['Registrator'].isnull())&(df7_concat['elt_bn'].notnull())]
    df9 = pd.DataFrame(df9, columns=columnsKupol)
    df9_group = df9.groupby(["name_store","elt_bn","pn","SOFdate_","registrationnumber","statusSO","StatusLog"], as_index=False).sum()
    merges4 = df8_group.merge(df9_group, left_on = ['date_doc', 'PN', 'registration_number'], right_on= ['SOFdate_', 'pn', 'registrationnumber'], how = 'outer') #набор обработанных данных после второй стыковки
    df10_concat = pd.concat([df7_concat_sostikov, merges4])
    #ебейшие преобразования
    df10_concat['qty_restocked'] = df10_concat['qty_restocked'].fillna(0)
    df10_concat['qty_released'] = df10_concat['qty_released'].fillna(0)
    df10_concat['qty'] = df10_concat['qty'].fillna(0)
    df10_concat['Proverka'] = df10_concat.apply(lambda x: x['qty_released']-x['qty_restocked']-x['qty'], axis=1)
    df10_concat = df10_concat.fillna({'date_doc':df10_concat['SOFdate_']})
    df10_concat['date_doc'] = pd.to_datetime(df10_concat['date_doc'])
    df10_concat['PN_all'] = df10_concat['PN'].fillna(df10_concat['pn'])
    df10_concat = df10_concat.sort_values(by=['date_doc','PN','Seria'], ascending=True)
    #вывод в файл
    excel = df10_concat.to_excel(f'C:\Dev\compare_reports_KUPOL_1C\compare_reports_KUPOL_1C\save\so_report_{DT.now():%Y-%m-%d_%H-%M}.xlsx', engine='xlsxwriter')
    return excel


#def getlog_kupol():
#    df = pd.read_sql_query(SqlQueries.get_kupol_log_from_test(), con=conn)
#    excel = df.to_excel(r'output_kupol_log_test_to_excel.xlsx', engine='xlsxwriter')
#    #return df
#    return excel


print(merge())
#print(get_1c_regist())
#print(get_kupol_so())
time.sleep(5)