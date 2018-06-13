import time
from random import randint
import webdav3.client as wc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt
import os


def log_in_file(text):
    with open('logfile.txt', 'a') as f:
        f.write(str(dt.now().strftime("%Y-%m-%d %H.%M.%S ")) + text + '\n')


def wd_sync(client, remote_path, relative_local_path):
    try:
        local_path = os.path.join(os.getcwd() + relative_local_path)
        m_file_time = os.path.getmtime(local_path)
        m_wdfile_timestr = client.info(remote_path)['modified']
        m_wdfile_time = dt.strptime(m_wdfile_timestr, '%a, %d %b %Y %X %Z').timestamp()
        if float(m_file_time) < float(m_wdfile_time):
            client.download_file(remote_path, local_path)
        else:
            client.upload_file(remote_path, local_path)
    except:
        client.download_file(remote_path, local_path)

    

options = {
    'webdav_hostname': "https://webdav.yandex.ru",
    'webdav_login':    "mrkotee08@ya.ru",
    'webdav_password': "fiopegvjeoxwfehl"
    }
client = wc.Client(options)
# # client.sync('/bot/', 'bot')

wd_sync(client, '/bot/bd/base.bd', '/bot/bd/base.bd')
wd_sync(client, '/bot/main.py', '/bot/main.py')
wd_sync(client, '/bot/settings.py', '/bot/settings.py')


from bot.settings import *
from bot.main import Dozor, Harbour, Energy, Brow

###################################################
# try:
#     with open('e_pass.txt', 'r') as f:
#         email, password = f.readline().split(',')
# except:
#     email = input('Введите логин: ')
#     password = input('Введите пароль: ')
#     with open('e_pass.txt', 'w') as f:
#         f.write(email + ',' + password)

# h_farm = 3   #hours to farm
timer_battle = 0
timer_harbour = 0
harb_i = 0
# b_energy = False

timer_present = 0

b = Brow()

engine = create_engine('sqlite:///bot/bd/base.bd', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
for d in session.query(Harbour).order_by(Harbour.id)[::-1][0:17]:
    if d.date == dt.now().date():
        harb_i += 1

for d in session.query(Dozor).order_by(Dozor.id)[::-1][0:5]:
    if d.date == dt.now().date():
        dozornyi = True
        break
    else:
        dozornyi = False

for d in session.query(Energy).order_by(Energy.id)[::-1][0:5]:
    if d.date == dt.now().date():
        b_energy = True
        break
    else:
        b_energy = False
#####################################

# time.sleep(15*60)

#####################################
print('start ' + str(dt.now().time().strftime("%H:%M:%S")))
log_in_file('start')

mnts = [randint(1, 12), randint(16, 27), randint(31, 42), randint(46, 55)]
print('mnts = ', mnts)
log_in_file('mnts = ' + ' '.join(str(mnt) for mnt in mnts))


while True:

    if dt.now().hour < 1 and dt.now().minute < 2:
        dozornyi = False
        harb_i = 0
        b_energy = False

    
    if time.time() > timer_battle:
        # print('start b_f_s')
        # b = Brow('Chrome')
        b.start()
        # b.headless_start()
        b.login(email, password)
        b.news_close()
        
        on_farm = b.time_on_farm()
        if on_farm:
            timer_battle = time.time() + on_farm
            b.end_session()
            # b.brow.close()
            # b.brow.quit()
        else:
            while True:
                gold = b.gold_now()
                for i, s in enumerate(b.stats_prices):
                    if (gold > s) and (i != 3):
                        b.train(i)
                        b.stats_prices = b.stats_gold()
                if gold < b.stats_prices[2]:
                    break
            if not b_energy:
                b.buy_energy()
                b_energy = True

            if b.valentine_timer - 300 < time.time():
                if b.valentine_timer > 0:
                    time.sleep(b.valentine_timer + 5 - time.time())
                b.st_valentine()

            b.b_t_s()
            b.mine_rage()

            # b.m_b_t()
            # b.battle_rage()

            if not dozornyi:  # dt.now().hour < 8 and
                if b.valentine_timer - 300 < time.time():
                    if b.valentine_timer > 0:
                        time.sleep(b.valentine_timer + 5 - time.time())
                    b.st_valentine()
                
                b.dozor()
                dozornyi = True

                b.tikets()

                b.wd.upload_as()
    
            b.b_t_s()

            # b.m_b_t()

            on_farm = b.time_on_farm()
            while not on_farm:
                b.farm(h_farm)
                on_farm = b.time_on_farm()
                timer_battle = time.time() + on_farm
            
            b.end_session()
            # b.brow.close()
            # b.brow.quit()
            timer_battle = time.time() + h_farm * 3600 + randint(5, 200)
            print('b stat farm ' + str(dt.now().time().strftime("%H:%M:%S")))
            log_in_file('b stat farm ')


    for mnt in mnts:
        if dt.now().minute == mnt: # and randint(1, 2) == 1:
            # print('start resurs')
            time.sleep(randint(1, 120))
            # b = Brow('Chrome')
            b.start()
            b.login(email, password)
            b.news_close()

            b.conflict_resurses()
            try:
                b.chest()
            except:
                pass

            if timer_present < time.time():
                t_p_wait = b.time_to_present()
                if t_p_wait:
                    timer_present = time.time() + t_p_wait
                else:
                    b.present()
                    timer_present = time.time() + 12 * 3600

            if timer_harbour < time.time() and harb_i < 15:  #отправка корабля
                harb_i += 1
                try:
                    b.harbour()
                except:
                    pass
                timer_harbour = time.time() + 3700

            b.end_session()
            # b.brow.close()
            # b.brow.quit()
            print('resurs ' + str(dt.now().time().strftime("%H:%M:%S")))
            log_in_file('resurs')

    if b.icelight_timer < time.time():
        b.start()
        b.login(email, password)
        b.news_close()
        b.end_session()
        # b.brow.close()
        # b.brow.quit()

    time.sleep(50)

