import pytz
import socket
import datetime
import time
import smtplib
import email.message
from ipaddress import IPv4Address
from ping3 import ping

def enviar_email():
    corpo_email = ('''<p>O servidor do site {} não está respondendo<p>
    <p>Data e hora da verificação : {} </p>
    <p>Este é o {}º e-mail de falha no servidor.</p>'''.format(ip, datastr,falha))

    msg = email.message.Message()
    msg['Subject'] = "AVISO - Servidor Offline"
    msg['From'] = 'prmassoni@gmail.com'
    msg['To'] = 'prmassoni@gmail.com'
    password = 'fxoaialcjwtdvnzo'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email de constatação do erro enviado.')

def esta_funcionando(ip):
    IPv4Address(ip)
    t = ping(ip, timeout=5)
    status = 'OFFLINE' if t is None else 'ONLINE'
    if status == 'ONLINE':
        return True
    else:
        return False

if __name__ == "__main__":
    falha = 0
    ip = input('IP (000.000.000.XXX) : ')
    ipinicial = 0
    ipfinal = int(input('IP Final (0/254) : '))
    while True:
        if ipinicial <= (ipfinal-1):
            ipinicial = ipinicial+1
            ip = ip[0:9]+'.'+ format(ipinicial)
            if esta_funcionando(ip):
                maquina = socket.gethostname()
                data = datetime.datetime.now(pytz.timezone('America/Cuiaba'))
                datastr = data.strftime("%d/%m/%y %H:%M")
                print('\nO IP : {} está online. '.format(ip))
                print('Horario : {} '.format(datastr))
            else:
                maquina = socket.gethostname()
                data = datetime.datetime.now(pytz.timezone('America/Cuiaba'))
                datastr = data.strftime("%d/%m/%y %H:%M")
                print('\nO IP : {} está offline. '.format(ip))
                print('Horario : {} '.format(datastr))
                falha = falha + 1
                enviar_email()
        else:
            ipinicial = 0
            time.sleep(540)
