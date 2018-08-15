#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import requests, time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from selenium import webdriver
import os

# Set the MOZ_HEADLESS environment variable which casues Firefox to start in headless mode.
os.environ['MOZ_HEADLESS'] = '1'


blacklists = open('fileIPs.txt', 'r')
line = blacklists.readline()
for line in blacklists:

	url_site= 'https://mxtoolbox.com/SuperTool.aspx?action=blacklist:' + str(line)
	
	navegador= webdriver.Firefox()
	navegador.get(url_site)

	time.sleep(5)


	campo_verificacion = navegador.find_element_by_xpath("/html/body/form/div[3]/div/div[2]/div/div[3]/div[2]/span/div/div[3]/strong[3]")
	verificacion = campo_verificacion.text

	time.sleep(1)


	numero = random.randrange(0000, 9999)


	if verificacion == "0":
		#numero = random.randrange(0000, 9999)
		navegador.save_screenshot('Blacklist_not_' + str(numero) + '.png')
		time.sleep(1)

		navegador.quit()
	else:
		navegador.save_screenshot('Blacklist_yes.png')
		time.sleep(1)

		navegador.quit()


		#enviarCorreo():
		fromaddr = "remitente"
		recipients = "destinatario"
 
		msg = MIMEMultipart()
 
		msg['From'] = fromaddr
		msg['To'] = ", ".join(recipients)
		msg['Subject'] = "Listas Negras"
 
		body = "Alerta de Seguridad (Blacklists)" +'\r\n' + "La IP " + line + " fue listada."
 
		msg.attach(MIMEText(body, 'plain'))
 
		filename = "Blacklist_yes.png"
		attachment = open("Blacklist_yes.png", "rb")
 
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
 
		msg.attach(part)
 
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(fromaddr, "Su contraseña")
		text = msg.as_string()
		server.sendmail(fromaddr, recipients, text)
		server.quit()


blacklists.close()
