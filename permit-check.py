#! python3

import requests, re, time, getpass

import smtplib, ssl
from email.message import EmailMessage

#nastav veci pro email

port = 465  # For SSL
smtp_server = "smtp.seznam.cz"
end_date = input("Napiš datum od kterého už nebudu hledat. \nNejspíše 2023-07-01 (dodrž formát), ale můžeš použít 2023-07-02 nebo vyšší pro testovací účely:")
sender_email = "hyneknahorach@seznam.cz"  # Enter your address
receiver_email = "jakub.venglar@seznam.cz"  # Enter receiver address
password = getpass.getpass("Napiš heslo a zmáčkni enter: ")


#make sure working directory is set the same as file directory

#stahni stranku

page = requests.get('https://portal.permit.pcta.org/availability/mexican-border.php', headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

all = page.text
start = '{"limit":50,"calendar":'
end= '};var canadaStart'

# vyber si relevantni cast, konvertuj do objektu a prober ho

result = re.search(f'{start}(.*){end}', all)
dateList = eval(result.group(1))

while True:

    for item in dateList:

        if item['start_date'] == '2023-07-02':
            break # tohle datum uz nas nezajima

        if int(item['num']) < 50:
            print('VOLNO')
            print(item['start_date'])


            # sestav a odesli zpravu - musi byt v loop, pokud by bylo vice mist (jeste lepe - )

            date = item['start_date']
            spots = 50 - int(item['num'])
            subject = f'Volné místo {date} na PCT'

            message = f"""Milý Hynečku
            
            Našel jsem pro tebe volné místo na tvé pouti.

            Toto místo je na den {date} a je jich právě {spots}.

            Tak rychle klikej, než ti ho vyfouknou.

            https://portal.permit.pcta.org/availability/mexican-border.php

            Tvůj věrný robotický otrok
                    
            """

            msg = EmailMessage()
            msg.set_content(message)
            msg['Subject'] = subject
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
    print('Čekám minutku na novou kontrolu')
    time.sleep(60) # pockame si


