#! python3

import requests, re, os, sys

import smtplib, ssl
from email.message import EmailMessage

port = 465  # For SSL
smtp_server = "smtp.seznam.cz"
sender_email = "hyneknahorach@seznam.cz"  # Enter your address
receiver_email = "jakub.venglar@seznam.cz"  # Enter receiver address
password = input("Napiš heslo a zmáčkni enter: ")

msg = EmailMessage()
msg.set_content("Úspěšný pokus")
msg['Subject'] = "Testování"
msg['From'] = sender_email
msg['To'] = receiver_email


try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
    print('Email úspěšně odeslán')

except Exception as e:
    print('Něco se nepovedlo a email jsem neodeslal. Jsi připojen k internetu?')
    print(e)

#make sure working directory is set the same as file directory
#os.chdir(os.path.dirname(sys.argv[0]))
#
#page = requests.get('https://portal.permit.pcta.org/availability/mexican-border.php', headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
#print(page.text)

#make regex for getting only dict
#eval dict
#for loop for finding proper dict key

# bezi kontinualne
# posli email