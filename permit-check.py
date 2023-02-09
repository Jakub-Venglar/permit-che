#! python3

import requests, re, time, getpass, time, os, json, datetime

import smtplib, ssl
from email.message import EmailMessage


port = 465  # For SSL

#nejdrive zkus nacist data ze souboru

try:   
    with open('data.json', 'r', encoding='utf-8') as file:
        data =  json.loads(file.read())

except FileNotFoundError:
    print('Zeptám se tě na pár úvodních nastavení. Ta se uloží do souboru "data.json". Pokud bys je chtěl změnit, uprav je v soboru nebo ho smaž a spusť znovu program.')
    smtp_server = input("smtp server, např. smtp.seznam.cz:")
    sender_email = input("Z jakého emailu to budeme posílat:")  
    receiver_email = input("A kam:") 
    initial_date = input("Napiš první datum, které mám otestovat. \nNapříklad 2023-04-01 (dodrž formát):")
    end_date = input("Napiš poslední datum, které mám otestovat. \nNapříklad 2023-05-31 (dodrž formát), ale můžeš použít 2023-07-01 nebo vyšší pro testovací účely:")

    data = {'smtp_server':smtp_server,'sender_email':sender_email,'receiver_email':receiver_email,'initial_date':initial_date,'end_date':end_date}

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent = 4) 


password = getpass.getpass("Napiš heslo k ODESÍLACÍMU emailu a zmáčkni enter: ")

#make sure working directory is set the same as file directory




# hlavni smycka

def convert_date(self, string):
    dateobj = datetime.datetime.strptime(string, '%Y-%m-%d')

    return dateobj

while True:
    #stahni stranku

    page = requests.get('https://portal.permit.pcta.org/availability/mexican-border.php', headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    all = page.text
    start = '{"limit":50,"calendar":'
    end= '};var canadaStart'

    # vyber si relevantni cast, konvertuj do objektu a prober ho

    result = re.search(f'{start}(.*){end}', all)
    dateList = eval(result.group(1))

    for item in dateList:

        if convert_date(item['start_date']) >= convert_date(data['initial_date']):

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
                msg['From'] = data['sender_email']
                msg['To'] = data['receiver_email']


                try:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL(data['smtp_server'], port, context=context) as server:
                        server.login(data['sender_email'], password)
                        server.send_message(msg, from_addr=data['sender_email'], to_addrs=data['receiver_email'])
                    print('Email úspěšně odeslán')

                except Exception as e:
                    print('Něco se nepovedlo a email jsem neodeslal. Jsi připojen k internetu?')
                    print(e)
        
        if item['start_date'] == end_date:
            break # po kontrole tohoto data skoncime

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print('Kontrola ukončena:')
    print(current_time)
    print('Čekám minutku na novou kontrolu')
    time.sleep(60) # pockame si


