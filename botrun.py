import time
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt
try:
    from bot.YaSync import sync_main_files  # Синхронизация с я.диском
    sync_main_files()
except Exception as e:
    print(
        'can not sync\n %s' % e
    )
    pass

from bot.settings import *
from bot.bd.models import Dozor, Harbour, Energy
from bot.main import Brow


def log_in_file(text):
    with open('logfile.txt', 'a') as f:
        f.write(str(dt.now().strftime("%Y-%m-%d %H.%M.%S ")) + text + '\n')
        print(text + str(dt.now().time().strftime("%H:%M:%S")))


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

timer_battle = 0
timer_harbour = 0
harb_i = 0
timer_present = 0


b = Brow()

log_in_file('start')

mnts = [randint(1, 12), randint(16, 27), randint(31, 42), randint(46, 55)]

log_in_file('mnts = ' + ' '.join(str(mnt) for mnt in mnts))


while True:

    if dt.now().hour < 1 and dt.now().minute < 2:
        dozornyi = False
        harb_i = 0
        b_energy = False

    if time.time() > timer_battle:
        b.start()
        b.login(email, password)
        b.news_close()
        
        on_farm = b.time_on_farm()
        if on_farm:
            timer_battle = time.time() + on_farm
            b.end_session()
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
            timer_battle = time.time() + h_farm * 3600 + randint(5, 200)

            log_in_file('b stat farm ')

    for mnt in mnts:
        if dt.now().minute == mnt:  # and randint(1, 2) == 1:
            time.sleep(randint(1, 120))
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
            log_in_file('resurs')

    if b.icelight_timer < time.time():  # Новогодняя акция
        b.start()
        b.login(email, password)
        b.news_close()
        b.end_session()

    time.sleep(50)

