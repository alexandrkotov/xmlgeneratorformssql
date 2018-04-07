#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
генератор XML 
'''
import time
import datetime
import os, sys
import pyodbc
from PyQt5.QtWidgets import QApplication
from decimal import *

def main_function(window):
    tStart = time.time()
    
    window.textEdit_info.setText("")
    window.lineEdit_cur_xml.setText("")
    window.lineEdit_db_rows.setText("")    
    QApplication.processEvents()

    outf = None
    driver = None
    sqlserver = None
    port = None
    dbname = None
    tbname = None
    username = None
    password = None
    batch_size = None

    try:
        is_1 = False #outf
        is_2 = False #driver
        is_3 = False #sqlserver
        is_4 = False #port
        is_5 = False #dbname
        is_6 = False #username
        is_7 = False #password
        is_8 = False #batch_size
        is_9 = False #tbname
        config = open("makexml.cfg","r")
        for line in config:
            l = line.split("=")
            if l[0].strip() == "outf" and len(l[1].strip()) > 0:
                outf = l[1].strip()
                is_1 = True
            if l[0].strip() == "driver" and len(l[1].strip()) > 0:
                driver = l[1].strip()
                is_2 = True
            if l[0].strip() == "sqlserver" and len(l[1].strip()) > 0:
                sqlserver = l[1].strip()
                is_3 = True
            if l[0].strip() == "port" and len(l[1].strip()) > 0:
                port = l[1].strip()
                is_4 = True
            if l[0].strip() == "dbname" and len(l[1].strip()) > 0:
                dbname = l[1].strip()
                is_5 = True
            if l[0].strip() == "tbname" and len(l[1].strip()) > 0:
                tbname = l[1].strip()
                is_9 = True                               
            if l[0].strip() == "username" and len(l[1].strip()) > 0:
                username = l[1].strip()
                is_6 = True
            if l[0].strip() == "password" and len(l[1].strip()) > 0:
                password = l[1].strip()
                is_7 = True
            if l[0].strip() == "batch_size" and len(l[1].strip()) > 0:
                try:
                    batch_size = int(l[1].strip())
                    is_8 = True
                except:
                    batch_size = "{} - должно быть число!".format(l[1].strip())
        if is_9 == True and is_1 == True and is_2 == True and is_3 == True and is_4 == True and is_5 == True and is_6 == True and is_7 == True and is_8 == True:
            pass
        else:            
            rinfo = "Нет обязательного параметра в конфигурационном файле"
            try:
                q=int(batch_size)
            except:
                rinfo = rinfo + "\n" + batch_size
            window.textEdit_info.setText(rinfo)
            print(rinfo)
            print("outf       = {}".format(outf))
            print("driver     = {}".format(driver))
            print("sqlserver  = {}".format(sqlserver))
            print("port       = {}".format(port))
            print("dbname     = {}".format(dbname))
            print("tbname     = {}".format(tbname))
            print("username   = {}".format(username))
            print("password   = {}".format(password))
            print("batch_size = {}".format(batch_size))
            return
    except:
        rinfo = "Конфигурационный файл не найден"
        window.textEdit_info.setText(rinfo)
        print(rinfo)
        return
              
    if not os.path.exists(outf):  
        os.makedirs(outf)
    
    con_str = 'DRIVER={};PORT={};SERVER={};DATABASE={};UID={};PWD={}'.format(driver, port, sqlserver, dbname, username, password)    
    cnxn = None
    try:
        cnxn = pyodbc.connect(con_str)
    except:
        rinfo = "Ошибка подключения к базе {} сервера {}".format(dbname, sqlserver)
        print(rinfo)
        window.textEdit_info.setText(rinfo)        
        return
    
    cnxn.autocommit = True
    print("Сервер                            : {}".format(sqlserver))
    print("База данных                       : {}".format(dbname))
    print("Таблица                           : {}".format(tbname))
    cursor = cnxn.cursor()    
    sql = "select * from [{}]".format(tbname)
    try:
        rinfo = "\n---\nАнализ начался - определение количества XML и количества item для каждого XML"
        print(rinfo)
        window.textEdit_info.setText(rinfo)
        QApplication.processEvents()
        cursor.execute(sql)
    except Exception as e:
        rinfo = "Ошибка подключения к таблице {} базы {}".format(tbname, dbname)
        print(rinfo)
        window.textEdit_info.setText(rinfo)
        f=open("Exception_Ошибка_подключения_к_таблице","w")
        f.write(str(e))
        f.close()
        return
        
    def make_header(i0, i1):
        res = '<?xml version="1.0" encoding="WINDOWS-1251"?><ItemList xmlns:importDomain="http://www.gk-software.com/storeweaver/master_data/import_domain/2.2.0" xmlns="http://www.gk-software.com/storeweaver/master_data/item/3.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gk-software.com/storeweaver/master_data/item/3.0.0 D:/GK/Validation/XSD/masterData_Item_v3_1_0.xsd" NumberOfItems="{}" GlobalChangeType="{}">'.format(str(i0).strip(), str(i1).strip()).strip()
        return res
    
    def make_item(i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, 
                  i19, i20, i21, i22, i23, i24, i25, i26, i27, i28, i29, i30, i31, i32, i33, i34,
                  i35, i36, i37, i38, i39, i40):
        
        res = """<Item ChangeType="{}"><BusinessUnitAssignment>
    <BusinessUnitID>{}</BusinessUnitID></BusinessUnitAssignment><ItemID>{}</ItemID>
    <BonText>{}</BonText><Description>{}</Description><TaxGroupID>{}</TaxGroupID>
    <BaseUOMCode>{}</BaseUOMCode><ClassCode>{}</ClassCode>
    <ItemUsageTypeCode>{}</ItemUsageTypeCode>
    <ShelfLifeDayCountPercent>{}</ShelfLifeDayCountPercent><ItemTextList><ItemText>
    <TextClass>{}</TextClass><Text>{}</Text>
    <xx_custom_01>{}</xx_custom_01>
    <xx_custom_02>{}</xx_custom_02></ItemText></ItemTextList><SupplierItemList><SupplierItem>
    <SupplierID>{}</SupplierID><SupplierItemID>{}</SupplierItemID>
    <DefaultOrderUOMCode>{}</DefaultOrderUOMCode><OrderUOMChoosableFlag>{}</OrderUOMChoosableFlag>
    </SupplierItem></SupplierItemList><UOMItemList><UOMItem><UOMCode>{}</UOMCode>
    <MainPOSItemID>{}</MainPOSItemID><ListingEffectiveDate>{}</ListingEffectiveDate>
    <ListingExpirationDate>{}</ListingExpirationDate>
    <MainMerchandiseHierarchyGroupID>{}</MainMerchandiseHierarchyGroupID>
    <PriceList><Price><Price>{}</Price><EffectiveDate>{}</EffectiveDate>
    <ExpirationDate>{}</ExpirationDate><PriceTypeCode>{}</PriceTypeCode>
    <xx_custom_01>{}</xx_custom_01></Price></PriceList><EANList><EAN>
    <PosItemID>{}</PosItemID><PosIdentityTypeCode>{}</PosIdentityTypeCode>
    <PLCFlag>{}</PLCFlag><PLCPart>{}</PLCPart><PLCPosItemID>{}</PLCPosItemID></EAN></EANList>
    <UOMItemTextList><UOMItemText><TextNumber>{}</TextNumber><TextClass>{}</TextClass>
    <LanguageID>{}</LanguageID><Text>{}</Text></UOMItemText></UOMItemTextList><ItemMHGList>
    <ItemMHG><MerchandiseHierarchyGroupID>{}</MerchandiseHierarchyGroupID>
    <MerchandiseHierarchyGroupIDQualifier>{}</MerchandiseHierarchyGroupIDQualifier>
    </ItemMHG></ItemMHGList></UOMItem></UOMItemList><ItemCollectionList/>
    </Item>""".format(i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, 
                      i17, i18, i19, i20, i21, i22, i23, i24, i25, i26, i27, i28, i29, i30, 
                      i31, i32, i33, i34, i35, i36, i37, i38, i39, i40).replace("\n","").strip()        
        return res
    
    key_cur = "" 
    key_last = "" 
    batch_count = 1 
    count = 0 
    count_in_batch = 0 
    start_row = 1 
    arr_ref_xml_rows = [] 
    while 1:
        row = cursor.fetchone()
        if row:
            cur_key = str(row[0]).strip() + str(row[1]).strip() + str(row[2]).strip()
            count += 1 
            if count == 1:
                key_last = cur_key
                count_in_batch = count                
            if (count_in_batch%batch_size == 0 and count > 1) or (key_last != cur_key and count > 1): 
                res = None
                if key_last == cur_key: 
                    res = [batch_count, start_row, count]                   
                    start_row = count+1
                else:
                    res = [batch_count, start_row, count-1]
                    start_row = count  
                    key_last = cur_key
                count_in_batch = 1
                arr_ref_xml_rows.append(res)                 
                batch_count += 1                   
            else:
                count_in_batch += 1           
        else:
            res = [batch_count, start_row, count]
            arr_ref_xml_rows.append(res)
            break
    rinfo = "Анализ завершился - количества item расчитаны для планируемых {} XML файлов".format(batch_count)
    window.textEdit_info.setText(rinfo)
    QApplication.processEvents()
    print(rinfo)

    dic_blocks = {}      
    dic_items_count = {} 
    for i in range(len(arr_ref_xml_rows)):
        block = arr_ref_xml_rows[i][0]
        row_start = arr_ref_xml_rows[i][1]
        row_end = arr_ref_xml_rows[i][2]
        if row_start not in dic_blocks:
            dic_blocks[row_start] = block
        if block not in dic_items_count:
            dic_items_count[block] = row_end-row_start+1
    q=dic_blocks
       
    window.lineEdit_db_rows.setText(str(count))    
    QApplication.processEvents()

    rinfo = "Генерация {} XML файлов началась".format(batch_count)
    window.textEdit_info.setText(rinfo)
    QApplication.processEvents()  
    print(rinfo)    
    cursor.execute(sql)
    count = 0
    cur_block = 0
    cf = None
    while 1:
        row = cursor.fetchone()
        if row:
            count += 1
            if count == 1:
                cur_block = dic_blocks[count]
                cf = open(os.path.join(outf, "_xml_{}.xml".format(cur_block)),"w")
                window.lineEdit_cur_xml.setText("_xml_{}.xml".format(cur_block))
                QApplication.processEvents()
                header = make_header(str(dic_items_count[cur_block]), row[0])
                cf.write(header)                
                item = make_item(row[1], row[2], row[3], row[4], str(row[5]).replace("&", "&amp;"), row[6], row[7], row[8], row[9], 
                                     row[10], row[11], row[12], str(row[13]).replace("&", "&amp;"), row[14], row[15], row[16], row[17], 
                                     row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], 
                                     row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], 
                                     row[34], row[35], row[36], row[37], row[38], row[39])
                cf.write(item)                
                
            if count in dic_blocks and count > 1:
                cf.write("</ItemList>")
                cf.close()
                cur_block = dic_blocks[count]
                cf = open(os.path.join(outf, "_xml_{}.xml".format(cur_block)),"w")
                window.lineEdit_cur_xml.setText("_xml_{}.xml".format(cur_block))
                QApplication.processEvents()
                header = make_header(str(dic_items_count[cur_block]), row[0])
                cf.write(header)                                 
                item = make_item(row[1], row[2], row[3], row[4], str(row[5]).replace("&", "&amp;"), row[6], row[7], row[8], row[9], 
                                     row[10], row[11], row[12], str(row[13]).replace("&", "&amp;"), row[14], row[15], row[16], row[17], 
                                     row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], 
                                     row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], 
                                     row[34], row[35], row[36], row[37], row[38], row[39])
                cf.write(item)  
            else:
                item = make_item(row[1], row[2], row[3], row[4], str(row[5]).replace("&", "&amp;"), row[6], row[7], row[8], row[9], 
                                     row[10], row[11], row[12], str(row[13]).replace("&", "&amp;"), row[14], row[15], row[16], row[17], 
                                     row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], 
                                     row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], 
                                     row[34], row[35], row[36], row[37], row[38], row[39])
                cf.write(item)                               
        else:
            cf.write("</ItemList>")
            cf.close()     
            rinfo = "Генерация {} XML файлов завершилась\n---\n".format(batch_count)
            window.textEdit_info.setText(rinfo)
            QApplication.processEvents()            
            print(rinfo)             
            break    

    st1 = "Обработанно строк в базе данных   : {}".format(count)
    st2 = "Количество строк на один XML файл : {}".format(batch_size)
    st3 = "Создано XML файлов                : {}".format(batch_count)
    st4 = "Путь к XML файлам                 : {}".format(os.path.join(os.path.abspath(os.curdir),outf))
    st5 = "Время выполнения                  : {0:.1f} сек.".format((time.time()-tStart))
    
    print(st1)
    print(st2)
    print(st3)
    print(st4)
    print(st5)
    
    flog=open("makexml.log","a")
    rs = str(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))+"\n"
    rs = rs + st1 + "\n"
    rs = rs + st2 + "\n"    
    rs = rs + st3 + "\n"
    rs = rs + st4 + "\n"
    rs = rs + st5 + "\n----------------------------------------------------------------------\n"
    window.textEdit_info.setText(rs)
    QApplication.processEvents()   
    flog.write(rs)
    flog.close()
