#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import Select
import imaplib
import email
import os
import random
import urllib2
from fake_useragent import UserAgent
from ConfigParser import ConfigParser

start_time = time.time()

config = ConfigParser()
config.read('user.ini')

user_num = config.get("USER", "num")

user_num = int(user_num)

for num in range(1+user_num):
    num += 1


config.set("USER", "num", num)

with open('user.ini', 'wb') as configfile:
    config.write(configfile)


with open("cuentas.txt", "r") as f:
    lines = f.readlines()
    correo = lines[user_num-1]

direccion_web = "https://www.tunnelbear.com/account/signup"
contrasena = "tunnelbear.pass#1"


options = Options()
ua = UserAgent()
userAgent = ua.random

options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument("user-agent={userAgent}")
options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=options, executable_path="chromedriver.exe",
                          desired_capabilities=options.to_capabilities())

driver.get(direccion_web)

WebDriverWait(driver, 5).until(EC.presence_of_element_located(
    (By.ID, "email")))  # Id inicio de sesion
placa1 = driver.find_element_by_id("email")
placa1.send_keys(correo)

placa2 = driver.find_element_by_id("password")  # Contrasena
placa2.send_keys(contrasena)

time.sleep(1)
driver.find_element_by_css_selector(
    ".btn.btn-lg.full-width.submit-btn").click()  # Click

time.sleep(3)


f.close()

time.sleep(25)

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('tunnelbearacc02@gmail.com', 'tunnelbear.pass#1') #Login
mail.list()
mail.select()

string_busqueda = "TunnelBear"

find = False

typ, resBusq = mail.search(None, '(ALL SUBJECT "' + string_busqueda + '")')

if resBusq[0] == '':
    print "Reintentando busqueda... \n"
    find = False
    time.sleep(2)
else:
    resBusq = resBusq[0].split(' ')
    find = True


typ, data = mail.fetch(resBusq[-1], '(RFC822)')

msg = email.message_from_string(data[0][1])
body = ""

if msg.is_multipart():
    for part in msg.walk():
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))

        if ctype == 'text/plain' and 'attachment' not in cdispo:
            body = part.get_payload(decode=True)
            break

else:
    body = msg.get_payload(decode=True)

file_ = open('page.html', 'w')
file_.write(body)
file_.close()

f = open('page.html', 'r')
datos = f.read()

datos = datos[190:274]

driver.get(datos)

# Delete imbox

mail.select("Inbox")

typ1, data1 = mail.search(None, 'ALL')

for num in data1[0].split():
    mail.store(num, '+FLAGS', '\\Deleted')

mail.expunge()
mail.close()
mail.logout()

driver.close()
driver.quit()

elapsed_time = time.time() - start_time

print "\n"
print "Credentials: "
print "User/Pass: " + correo + " : " + contrasena
print "\n"
print "Elapsed time: %.10f seconds." %elapsed_time