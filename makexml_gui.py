#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
GUI для makexml
'''
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QMessageBox, 
QCommandLinkButton, QLineEdit, QLabel, QCheckBox, QRadioButton, QFileDialog)
from PyQt5.QtCore import Qt
import sys, os
import makexml

def load_cfg():
    print("load_cfg")
    outf = None
    driver = None
    sqlserver = None
    port = None
    dbname = None
    username = None
    password = None
    batch_size = None
    try:
        config=open("makexml.cfg","r")
        for line in config:
            l = line.split("=")
            if l[0].strip() == "outf" and len(l[1].strip()) > 0:
                outf = l[1].strip()
            if l[0].strip() == "driver" and len(l[1].strip()) > 0:
                driver = l[1].strip()
            if l[0].strip() == "sqlserver" and len(l[1].strip()) > 0:
                sqlserver = l[1].strip()
            if l[0].strip() == "port" and len(l[1].strip()) > 0:
                port = l[1].strip()
            if l[0].strip() == "dbname" and len(l[1].strip()) > 0:
                dbname = l[1].strip()
            if l[0].strip() == "tbname" and len(l[1].strip()) > 0:
                tbname = l[1].strip()            
            if l[0].strip() == "username" and len(l[1].strip()) > 0:
                username = l[1].strip()
            if l[0].strip() == "password" and len(l[1].strip()) > 0:
                password = l[1].strip()
            if l[0].strip() == "batch_size" and len(l[1].strip()) > 0:
                batch_size = l[1].strip()    
                
        #fcsv = window.labelIn.text()
        #window.labelIn.setText(res)
        window.lineEdit_outf.setText(outf)
        window.lineEdit_driver.setText(driver)
        window.lineEdit_sqlserver.setText(sqlserver)
        window.lineEdit_port.setText(port)
        window.lineEdit_dbname.setText(dbname)
        window.lineEdit_table.setText(tbname)
        window.lineEdit_username.setText(username)
        window.lineEdit_password.setText(password)
        window.lineEdit_batch_size.setText(batch_size)
        config.close()
    except:
        pass
        

def check_empty_fields():
    if len(str(window.lineEdit_outf.text())) == 0:
        return False
    if len(str(window.lineEdit_driver.text())) == 0:
        return False    
    if len(str(window.lineEdit_sqlserver.text())) == 0:
        return False
    if len(str(window.lineEdit_port.text())) == 0:
        return False 
    if len(str(window.lineEdit_dbname.text())) == 0:
        return False
    if len(str(window.lineEdit_table.text())) == 0:
        return False    
    if len(str(window.lineEdit_username.text())) == 0:
        return False
    if len(str(window.lineEdit_password.text())) == 0:
        return False     
    if len(str(window.lineEdit_batch_size.text())) == 0:
        return False 
    return True

def save_cfg():
    print("save_cfg")
    
    r = "outf       = " + window.lineEdit_outf.text() + "\n"
    r = r + "driver     = " + window.lineEdit_driver.text() + "\n"
    r = r + "sqlserver  = " + window.lineEdit_sqlserver.text() + "\n"
    r = r + "port       = " + window.lineEdit_port.text() + "\n"
    r = r + "dbname     = " + window.lineEdit_dbname.text() + "\n"
    r = r + "tbname     = " + window.lineEdit_table.text() + "\n"
    r = r + "username   = " + window.lineEdit_username.text() + "\n"
    r = r + "password   = " + window.lineEdit_password.text() + "\n"
    r = r + "batch_size = " + window.lineEdit_batch_size.text() + "\n"
    
    print(check_empty_fields())
    window.textEdit_info.setText("")
    window.lineEdit_cur_xml.setText("")
    window.lineEdit_db_rows.setText("")
    QApplication.processEvents()#принудительный перезапуск GUI для отрисовки    
    if not check_empty_fields():
        reply = QMessageBox.question(window, "Есть пустые поля",
            "Всё равно сохранить?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No) 
        if reply == QMessageBox.Yes:
            config=open("makexml.cfg","w")
            config.write(r)
            config.close()
        else:
            return
        
    else:   
        config=open("makexml.cfg","w")
        config.write(r)
        config.close()
        window.textEdit_info.setText("")
    
def make_xml():
    print("make_xml")
    makexml.main_function(window)


app = QApplication(sys.argv)
window = QMainWindow()
window = uic.loadUi("makexml_gui.ui")
window.pushButton_save_cfg.clicked.connect(save_cfg)
window.pushButton_exec.clicked.connect(make_xml)
load_cfg()
window.show()
sys.exit(app.exec_())