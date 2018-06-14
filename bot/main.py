import time
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime as dt
from bot.bd.models import IceTownUpgrades, Dozor, Harbour, Energy, Log
try:
    from bot.YaSync import WdavForBd
except:
    pass

from bot.settings import max_instrument_cost, max_stone_cost, min_glory_points_to_buy

        
class Brow:
    """login (email, password)
    news_close
    energy - [0]now, [1]max
    stats_gold
    gold_now
    train(stat) - stat = id of stat
    battle - make 1 fight
    b_t_s - do battle and train while energy > 0
    mine 
    dozor - wear head and dozor
    tikets - go to s and b tikets
    farm(hours) - go to farm for N hours
    conflict_resurses - take all resurses from map
    chest - take reward from map
    """



    def add_to_base(self, action, number=0):
        """doz, harb, energy"""

        engine = create_engine('sqlite:///bot/bd/base.bd', echo=False)

        Session = sessionmaker(bind=engine)
        session = Session()
        if action == 'doz':
            session.add(Dozor())
            session.add(Log('Dozor'))
        elif action == 'harb':
            session.add(Harbour())
            session.add(Log('Harb'))
            session.commit()
            self.wd.upload_as()
            # self._upload_base()
        elif action == 'energy':
            session.add(Energy(number))
            session.add(Log('energy'))
            self.wd.upload_as()
        else:
            print('session error')

        session.commit()

    def __init__(self):

        global min_glory_points_to_buy
        global max_stone_cost
        global max_instrument_cost
        self.max_instrument_cost = max_instrument_cost
        self.max_stone_cost = max_stone_cost
        self.min_glory_points_to_buy = min_glory_points_to_buy

        self.wd = WdavForBd()
        # self.wd.download()
        # self._download_base()

        self.stats_prices = []

        # self.octo_timer = 0
        self.b_gift_timer = 0
        # self.cloud_island_timer = 0
        self.ice_timer = 0
        self.ice_upd_timer = 0
        self.icelight_timer = 0
        self.valentine_timer = 0

    def start(self):
        self.brow = webdriver.Chrome()
        # self.brow.implicitly_wait(2)
        self.brow.get('http://avatar.botva.ru/')
        assert 'Ботва' in self.brow.title
        # self.octo_gifts = 0

    def headless_start(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.brow = webdriver.Chrome(chrome_options=options)
        self.brow.implicitly_wait(2)
        self.brow.get('http://avatar.botva.ru/')

    def login(self, email, password):
        # if self.cookies:
        while True:
            try:
                element = WebDriverWait(self.brow, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'sign_in'))
                )
                sign = self.brow.find_element_by_class_name('sign_in')
                sign.click()

                em = self.brow.find_element_by_name('email')
                em.send_keys(email)
                psw = self.brow.find_element_by_name('password')
                psw.send_keys(password + Keys.ENTER)
                time.sleep(4)
                wait = WebDriverWait(self.brow, 10).until(
                    EC.element_to_be_clickable((By.ID, 'm1'))
                )
                break
            except:
                self.brow.refresh()

    def news_close(self):
        try:
            if self.brow.find_element_by_id('news_box'):
                news_close = self.brow.find_element_by_id('close')
                news_close.click()
        except:
            pass

        if self.npc():
            pass
            # self.contraband_click()
        #     self.birthday_gift()
        #     self.b_gift_timer = time.time() + 2 * 3602
        #     print('gift as npc {}:{}:{}'.format(str(dt.now().hour), 
        #         str(dt.now().minute), str(dt.now().second)))
            # self.octogame()
            # self.octo_timer = time.time() + 1 * 3602
            # print('octo as npc {}:{}:{}, gifts: {}'.format(str(dt.now().hour), 
            #     str(dt.now().minute), str(dt.now().second), str(self.octo_gifts - 1)))

        # if (self.valentine_timer - 15) < time.time():
        #     sleep_time = self.valentine_timer - time.time()
        #     if sleep_time > 0:
        #         print(self.valentine_timer)
        #         time.sleep(sleep_time + 3)
        #     self.st_valentine()

        
        self.stats_prices = self.stats_gold()
        # self.cloud_island()
        # self.ice_upgrade()
        # self.ice_mine()
        # self.ice_light()

    def end_session(self):
        self.click_valentain = False
        self.brow.close()
        self.brow.quit()

    def energy(self):
        # energy_now
        # energy_max
        en_now = self.brow.find_element_by_class_name('energy_now').text
        en_max = self.brow.find_element_by_class_name('energy_max').text
        return int(en_now), int(en_max)

    def buy_energy(self):
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'avatar_buy_energy_top'))
        )
        self.brow.find_element_by_id('avatar_buy_energy_top').click()
        wait = WebDriverWait(self.brow, 60).until(
            EC.presence_of_element_located((By.ID, 'avatar_buy_energy_popup'))
        )
        el = self.brow.find_elements_by_css_selector('div#avatar_buy_energy_popup > div.pt5 > b')
        buyed = int(el[1].text.split('/')[0])
        maxy_buy = int(el[1].text.split('/')[1])
        count = maxy_buy - buyed

        buts = self.brow.find_elements_by_css_selector('div#avatar_buy_energy_popup > div.mt10 > div')
        if count:
            buts[2].click()

            for _ in range(count - 1):
                while True:
                    try:
                        wait = WebDriverWait(self.brow, 60).until(
                            EC.element_to_be_clickable((By.ID, 'm9'))
                        )
                        self.brow.find_element_by_id('m9').click()
                        wait = WebDriverWait(self.brow, 60).until(
                            EC.element_to_be_clickable((By.ID, 'avatar_buy_energy_top'))
                        )
                        self.brow.find_element_by_id('avatar_buy_energy_top').click()
                        wait = WebDriverWait(self.brow, 60).until(
                            EC.presence_of_element_located((By.ID, 'avatar_buy_energy_popup'))
                        )
                        buts = self.brow.find_elements_by_css_selector('div#avatar_buy_energy_popup > div.mt10 > div')
                        buts[2].click()
                        time.sleep(2)
                        break
                    except:
                        self.brow.refresh()
        else:
            buts[0].click()
        self.add_to_base('energy', count)

    def stats_gold(self):
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm1'))
        )
        pers = self.brow.find_element_by_id('m1')
        pers.click()
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm1'))
        )
        s_g = self.brow.find_elements_by_css_selector(
            'div > div.tab > div.p10 > div.w40p > div.mb1 > span')
        g_list = []
        for gold in s_g[:5]:
            g_list.append(self.remove_dot(gold.text))
        return g_list

    def gold_now(self):
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'gold_data'))
        )
        
        return self.remove_dot(self.brow.find_element_by_class_name('gold_data').text)

    def train(self, stat):
        """stat = i of stat
        3 = endurance """

        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm1'))
        )
        pers = self.brow.find_element_by_id('m1')
        pers.click()
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm1'))
        )
        buttons = self.brow.find_elements_by_css_selector('div > div.tab > div.p10 > div.w40p > div.mb1 > div.inlineb')
        buttons[stat].click()

    def battle(self):
        wait = WebDriverWait(self.brow, 10).until(
            EC.element_to_be_clickable((By.ID, 'm8'))
        )
        dozor = self.brow.find_element_by_id('m8')
        dozor.click()
        wait = WebDriverWait(self.brow, 10).until(
            EC.element_to_be_clickable((By.ID, 'watch_find'))
        )
        find_target = self.brow.find_element_by_id('watch_find')
        find_target.click()
        try:
            wait = WebDriverWait(self.brow, 10).until(
                EC.element_to_be_clickable((By.ID, 'attack_form'))
            )
            self.brow.find_element_by_id('attack_form').click()
        except:
            pass
        # time.sleep(randint(1, 2))

    def b_t_s(self):
        battle_count = 0
        e_n = self.energy()[0] // 10
        bat_for_def = e_n * 0.8
        for bat in range(e_n):
            gold = self.gold_now()
            for i, s in enumerate(self.stats_prices):
                if bat < int(bat_for_def):
                    if (gold > s) and (i != 3) and (i != 2):
                        self.train(i)
                        self.stats_prices = self.stats_gold()
                else:
                    if (gold > s) and (i != 3):
                        self.train(i)
                        self.stats_prices = self.stats_gold()
            if battle_count < 230:
                self.battle()
                battle_count += 1
            else:
                self.mine_rage()
                battle_count = 0

    def m_b_t(self):
        e_n = self.energy()[0] // 15

        for mines in range(e_n):
            self.mine()

        # self.battle_rage()

    def battle_rage(self):
        wait = WebDriverWait(self.brow, 10).until(
            EC.element_to_be_clickable((By.ID, 'm8'))
        )
        dozor = self.brow.find_element_by_id('m8')
        dozor.click()
        try:
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'rage_amount'))
            )
            battle_rage = self.brow.find_element_by_class_name('rage_amount').text
        except:
            return False
        for _ in range(int(battle_rage)):
            gold = self.gold_now()
            for i, s in enumerate(self.stats_prices):
                if (gold > s) and (i != 3):
                    self.train(i)
                    self.stats_prices = self.stats_gold()
            self.battle()

    def mine_rage(self):
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm6'))
        )
        miner = self.brow.find_element_by_id('m6')
        miner.click()
        try:
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'rage_amount'))
            )
            mine_rage = self.brow.find_element_by_class_name('rage_amount').text
        except:
            return False
        for _ in range(int(mine_rage)):
            self.mine()
        # self.tikets()

    def mine(self):
        if self.brow.current_url != r'http://avatar.botva.ru/mine.php':
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm6'))
            )
            miner = self.brow.find_element_by_id('m6')
            miner.click()

        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#work_in_mine > div.p10 > div.h60 > div.button_new'))
        )
        self.brow.find_element_by_css_selector('div#work_in_mine > div.p10 > div.h60 > div.button_new').click()
        time.sleep(4)
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div#work_in_mine > div.p10 > div.p5 > div.pt5 > div.button_new'))
        )
        self.brow.find_element_by_css_selector(
            'div#work_in_mine > div.p10 > div.p5 > div.pt5 > div.button_new').click()
        time.sleep(randint(1, 2))

    def dozor(self):

        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm1'))
        )
        pers = self.brow.find_element_by_id('m1')
        pers.click()

        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'selector_weapons'))
        )
        self.brow.find_element_by_id('selector_weapons').click()
        WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'home_item_1668'))
        )
        head = self.brow.find_element_by_id('home_item_1668')
        head.click()
        
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm8'))
        )
        dozor = self.brow.find_element_by_id('m8')
        dozor.click()

        wait = WebDriverWait(self.brow, 15).until(
            EC.element_to_be_clickable((By.ID, 'watch_watch'))
        )
        doz_time = self.brow.find_elements_by_css_selector('div#watch_watch_time_left > b')[1].text
        while int(doz_time) > 0:
            try:
                self.brow.find_element_by_id('watch_watch').click()
                time.sleep(9)
                # in_doz = self.brow.find_element_by_class_name('h65')
                # while in_doz:
                #     try:
                #         in_doz = self.brow.find_element_by_class_name('h65')
                #     except:
                #         in_doz = False
                #         break
                wait = WebDriverWait(self.brow, 15).until(
                    EC.element_to_be_clickable((By.ID, 'watch_watch'))
                )
                doz_time = self.brow.find_elements_by_css_selector('div#watch_watch_time_left > b')[1].text
                self.add_to_base('doz')
            except:
                continue


        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm1'))
        )
        pers = self.brow.find_element_by_id('m1')
        pers.click()
        WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'selector_weapons'))
        )
        self.brow.find_element_by_id('selector_weapons').click()
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'home_item_1729'))
        )
        head = self.brow.find_element_by_id('home_item_1729')
        head.click()

    def tikets(self):
        def tik(i):
            for _ in range(int(i)):
                wait = WebDriverWait(self.brow, 6).until(
                    EC.presence_of_element_located(
                        (By.ID, 'counter_1'))
                )
                self.brow.find_elements_by_css_selector('div.mt5 > a')[1].click()
                time.sleep(1.5)
                wait = WebDriverWait(self.brow, 6).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'div.mt5 > a'))
                )
                self.brow.find_element_by_css_selector('div.mt5 > a').click()
                time.sleep(1.5)
        try:
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm6'))
            )
            miner = self.brow.find_element_by_id('m6')
            miner.click()

            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm6'))
            )
            count_tikets = self.brow.find_elements_by_class_name('mt4')

            big_tik = count_tikets[1].text.split('/')[0]
            self.brow.find_elements_by_css_selector('td > div.button_new')[1].click()
            tik(big_tik)

            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm6'))
            )
            miner = self.brow.find_element_by_id('m6')
            miner.click()
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm6'))
            )
            count_tikets = self.brow.find_elements_by_class_name('mt4')
            small_tik = count_tikets[0].text.split('/')[0]
            self.brow.find_elements_by_css_selector('td > div.button_new')[0].click()
            tik(small_tik)
        except:
            wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm8'))
            )
            try:
                dozor = self.brow.find_element_by_id('m8').click()
                self.brow.find_element_by_css_selector('div.mt5 > a').click()
            except:
                pass

    def farm(self, value):

        """value = hours of farm"""

        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm3'))
        )
        vil = self.brow.find_element_by_id('m3')
        vil.click()
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'village_image5'))
        )
        farm = self.brow.find_element_by_class_name('village_image5')
        farm.click()
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.NAME, 'work'))
        )
        hours_farm = Select(self.brow.find_element_by_name('work'))
        hours_farm.select_by_value(str(value))
        # hours_farm.click()

        self.brow.find_element_by_class_name('work_on_farm').click()

    def time_on_farm(self):
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm8'))
        )
        dozor = self.brow.find_element_by_id('m8')
        dozor.click()
        try:
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm8'))
            )
            h_m_s = self.brow.find_element_by_css_selector('div#avatar_farm_work_bar > div.text > span').text
            timer = int(h_m_s.split(':')[0]) * 3600 + int(h_m_s.split(':')[1]) * 60 + int(h_m_s.split(':')[2])
            return int(timer)
        except:
            return False

    def harbour(self):

        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm7'))
        )
        harb = self.brow.find_element_by_id('m7')
        harb.click()
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'harbour_image2'))
        )
        pier = self.brow.find_element_by_class_name('harbour_image2')
        pier.click()
        self.brow.find_element_by_class_name('send_ship').click()

        self.add_to_base('harb')

    def conflict_resurses(self):

        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm44'))
        )
        elem = self.brow.find_element_by_id('m44')
        elem.click()

        try:
            element = WebDriverWait(self.brow, 60).until(
                EC.title_contains('Битва за земли')
            )
        except:
            pass
        time.sleep(randint(3, 5))

        r1 = self.brow.find_elements_by_class_name('submit_by_ajax_completed')
        for i in range(len(r1)):
            res = self.brow.find_elements_by_class_name('submit_by_ajax_completed')
            try:
                res[i].click()
                time.sleep(randint(1, 2))
            except:
                pass

        try:
            element = WebDriverWait(self.brow, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'btn_craft'))
            )
            self.brow.find_element_by_class_name('btn_craft').click()  # enter in craft
            element = WebDriverWait(self.brow, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'btn_craft'))
            )

            def my_glory():
                glory_points_str = self.brow.find_element_by_css_selector('div.p5 > b')
                nums = glory_points_str.text.split('.')
                for i1, g2 in enumerate(nums):
                    if i1 == 0:
                        n = str(g2)
                    else:
                        n += str(g2)
                return int(n)
            glory_points = my_glory()
            glory_points_cost = int(self.brow.find_elements_by_css_selector('div.pt3 > b')[0].text)

            while glory_points_cost < self.max_stone_cost and glory_points > self.min_glory_points_to_buy:
                self.brow.find_elements_by_css_selector('div.pb5 > form')[0].click()
                glory_points -= glory_points_cost
                glory_points_cost = int(self.brow.find_elements_by_css_selector('div.pt3 > b')[0].text)
                instruments_bag_cost = int(self.brow.find_elements_by_css_selector('div.pt3 > b')[1].text)
                if instruments_bag_cost < self.max_instrument_cost:
                    self.brow.find_elements_by_css_selector('div.pb5 > form')[1].click()
                time.sleep(0.5)
        except:
            pass

    def chest(self):
        # has_chest - сундук
        elem = self.brow.find_element_by_id('m44')
        elem.click()
        try:
            element = WebDriverWait(self.brow, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'has_chest'))
            )
        except:
            return False
        butt = self.brow.find_element_by_class_name('has_chest')
        butt.click()
        # get_reward
        time.sleep(2)
        element = WebDriverWait(self.brow, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'get_reward'))
        )
        butt2 = self.brow.find_element_by_class_name('get_reward')
        butt2.click()

    def present(self):
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm1'))
        )

        self.brow.find_element_by_css_selector('span.h75 > div#uptime_get_prize > div.p2').click()
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div > span.w80'))
        )
        self.brow.find_elements_by_css_selector('div > span.w80')[0].click()

    def time_to_present(self):
        wait = WebDriverWait(self.brow, 60).until(
            EC.element_to_be_clickable((By.ID, 'm1'))
        )
        try:
            h_m_s = self.brow.find_element_by_css_selector(
                'div#uptime_prize_timer > div.h20  > div.borderred_text > b > span').text
            timer = int(h_m_s.split(':')[0]) * 3600 + int(h_m_s.split(':')[1]) * 60 + int(h_m_s.split(':')[2])
            return int(timer)
        except:
            return False

    def npc(self):
        try:
            wait = WebDriverWait(self.brow, 5).until(
                EC.element_to_be_clickable((By.ID, 'm1'))
            )
            self.brow.find_element_by_id('annoying_npc').click()
            wait = WebDriverWait(self.brow, 3).until(
                EC.element_to_be_clickable((By.ID, 'm1'))
            )
            return True
        except:
            return False

    def remove_dot(self, str_summ):
        # if '.' in str_summ:
        nums = str_summ.split('.')
        for i, number in enumerate(nums):
            if i == 0:
                n = str(number)
            else:
                n += str(number)
        return int(n)

    ##### Акции #####

    def octogame(self):
        self.brow.get('http://avatar.botva.ru/event.php?a=weekofauthority')
        # wait = WebDriverWait(self.brow, 60).until(
        #     EC.element_to_be_clickable((By.ID, 'm1'))
        # )
        # self.brow.find_element_by_css_selector('div.top_menu > a.logo').click()
        while True:
            try:
                wait = WebDriverWait(self.brow, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.p10 > div.mt10 > form > div.button_new'))
                )
                self.brow.find_elements_by_css_selector('div.p10 > div.mt10 > form > div.button_new')[0].click()
            except:
                pass
            if EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.dflex > div > div.dflex > div.active')):
                break
            

        # wait = WebDriverWait(self.brow, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.dflex > div > div.dflex > div.active'))
        # )

        # for line in range(7):
            # if line == 6:
        tryes = 0
        while True:
            try:
                boxes = self.brow.find_elements_by_css_selector('div.dflex > div > div.dflex > div.active')
                # print(boxes)
                boxes[randint(0, 2)].click()
                time.sleep(2)
                tryes = 0
                self.octo_gifts += 1
            except:
                try:
                    wait = WebDriverWait(self.brow, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.dflex > div > div.dflex > div.active'))
                    )
                    box = self.brow.find_element_by_css_selector('div.dflex > div > div.dflex > div.active')
                    box.click()
                    time.sleep(2)
                    self.octo_gifts += 1
                    
                except:
                    tryes += 1
                    if tryes == 3:
                        break
        wait = WebDriverWait(self.brow, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.box_body > div > div.box_controls > div.button'))
        )
        self.brow.find_element_by_css_selector('div.box_body > div > div.box_controls > div.button').click()
        time.sleep(1)

    def octogame_timer(self):
        self.brow.get('http://avatar.botva.ru/event.php?a=weekofauthority')
        # wait = WebDriverWait(self.brow, 60).until(
        #     EC.element_to_be_clickable((By.ID, 'm1'))
        # )
        # self.brow.find_element_by_css_selector('div.top_menu > a.logo').click()
        wait = WebDriverWait(self.brow, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.p10 > div.mt10 > form > div.button_new'))
        )
        try:
            time = self.brow.find_element_by_css_selector('div.p10 > div.mt10 > form > div.button_new > span > span').text
            parts = time.split(':')
            timer = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            return int(timer)
        except:
            return False

    def full_octo_game(self):
        if time.time() > self.octo_timer: 
            o_time = self.octogame_timer()
            if o_time:
                self.octo_timer = time.time() + o_time
            else:
                self.octogame()
                self.octo_timer = time.time() + 1 * 3602
                print('octo {}:{}:{}, gifts: {}'.format(str(dt.now().hour), 
                    str(dt.now().minute), str(dt.now().second), str(self.octo_gifts - 1)))

    def birthday_gift(self):
        self.brow.get('https://avatar.botva.ru/event.php?a=whereisshanni')
        wait = WebDriverWait(self.brow, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 
                'div.p10 > div.mt10 > div.button_new'))
        )
        self.brow.find_element_by_css_selector(
            'div.p10 > div.mt10 > div.button_new'
            ).click()
        wait = WebDriverWait(self.brow, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 
                'div.box_body > div > div.box_controls > div.button'))
        )
        self.brow.find_element_by_css_selector(
            'div.box_body > div > div.box_controls > div.button').click()
        time.sleep(1)

    def cloud_check_time(self):
        try:
            button_time = self.brow.find_element_by_css_selector(
                'div.tab > div.pr10 > form > div.button_new > span > span').text
            parts = button_time.split(':')
            timer = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            self.cloud_island_timer = time.time() + int(timer)
            return True
        except:
            return False

    def cloud_island(self):
        if self.cloud_island_timer < time.time():
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm1'))
            )
            elem = self.brow.find_element_by_id('m49')
            elem.click()
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm1'))
            )
            check_time = self.cloud_check_time()
            if not check_time:
                startbutton = self.brow.find_element_by_css_selector('div.tab > div.pr10 > form > div.button_new')
                startbutton.click()
                wait = WebDriverWait(self.brow, 60).until(
                    EC.element_to_be_clickable((By.ID, 'm1'))
                )
                self.cloud_check_time()

                print('dogs {}:{}:{}'.format(str(dt.now().hour),
                                            str(dt.now().minute), str(dt.now().second)))

    def ice_mine(self):
        if time.time() > self.ice_timer:
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm3'))
            )
            self.brow.find_element_by_id('m3').click()

            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'village_image12'))
            )
            self.brow.find_element_by_class_name('village_image12').click()

            wait = WebDriverWait(self.brow, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.icetown_place > div.icetown_area2'))
            )
            try:
                gift_keys = self.brow.find_elements_by_class_name('h100')
                for gift_key in range(len(gift_keys)):
                    self.brow.find_element_by_class_name('h100').click()
                    time.sleep(1)
            except:
                pass

            self.brow.find_element_by_css_selector('a.icetown_place > div.icetown_area2').click()

            if self.ice_repair():
                try:
                    wait = WebDriverWait(self.brow, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.lh30 > div.mr10 > div.button_new'))
                    )
                    self.brow.find_element_by_css_selector('div.lh30 > div.mr10 > div.button_new').click()
                    time.sleep(2)
                except:
                    pass

                time_text = self.brow.find_element_by_css_selector(
                    'div.dflex > b.timer > span').text
                parts = time_text.split(':')
                timer = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                self.ice_timer = time.time() + timer

    def ice_upgrade(self):

        def upgrade_timer_exist(building_number):
            css_selec = 'a.icetown_place > div.icetown_area{}'.format(building_number)
            self.brow.find_element_by_css_selector(css_selec).click()

            timer = 0
            try:
                time_text = self.brow.find_element_by_css_selector(
                    'div.pl10 > div > b.timer > span').text
                parts = time_text.split(':')
                timer = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                self.ice_upd_timer = time.time() + timer
                self.brow.find_element_by_class_name('navigation_back').click()
                # self.brow.execute_script("window.history.go(-1)")
                # self.brow.get('http://avatar.botva.ru/event.php?a=icetown')
                return True
                            
            except:
                self.brow.find_element_by_class_name('navigation_back').click()
                # self.brow.execute_script("window.history.go(-1)")
                # self.brow.get('http://avatar.botva.ru/event.php?a=icetown')
                return False

        def upgrade_building(building_number):
            css_selec = 'a.icetown_place > div.icetown_area{}'.format(building_number)
            self.brow.find_element_by_css_selector(css_selec).click()

            wait = WebDriverWait(self.brow, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.pl10 > div.button_new'))
                )
            self.brow.find_element_by_css_selector('div.pl10 > div.button_new').click()
 
                
        if time.time() > self.ice_upd_timer:

            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm3'))
            )
            self.brow.find_element_by_id('m3').click()

            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'village_image12'))
            )
            self.brow.find_element_by_class_name('village_image12').click()

            wait = WebDriverWait(self.brow, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.icetown_place > div.icetown_area3'))
            )
            self.curr_icecubes = self.remove_dot(self.brow.find_element_by_css_selector(
                                'div.icetown_info > div.mb2 > b').text)

            
                # tree, miner, tower, leprec, storage, firehouse
            lvls = {
                '3': 0,
                '5': 0,
                '2': 0,
                '1': 0,
                '6': 0,
                '4': 0,
            }

            # lvls = []
            for k in lvls.keys():
                selector = 'a.icetown_place > div.icetown_area{} > div.icetown_flag > span'.format(k)
                lvls[k] = int(self.brow.find_element_by_css_selector(selector).text)

            for idx, bld in lvls.items():
                if bld < 10:
                    timer_exst = upgrade_timer_exist(idx)
                    break
                else:
                    timer_exst = True

            if not timer_exst:
                engine = create_engine('sqlite:///bot/bd/base.bd', echo=False)
                Session = sessionmaker(bind=engine)
                session = Session()
                upd_posibility = {}
                prev_lvl = 10
                for idx, buildings_lvl in lvls.items():
                    idx = int(idx) - 1
                    if buildings_lvl < 10:
                        try:
                            upgrd_cost = session.query(IceTownUpgrades).filter_by(
                                building_id=idx, building_lvl=buildings_lvl + 1)[0].upgrade_cost
                        except:
                            
                            selector = 'a.icetown_place > div.icetown_area{}'.format(idx+1)
                            self.brow.find_element_by_css_selector(selector).click()
                            wait = WebDriverWait(self.brow, 5).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.pl10 > div > b'))
                            )
                            if self.ice_repair():
                                try:
                                    upgrd_cost = self.remove_dot(self.brow.find_element_by_css_selector(
                                        'div.pl10 > div > b').text)
                                    session.add(IceTownUpgrades(idx, buildings_lvl + 1, upgrd_cost))
                                    session.commit()
                                except:
                                    pass
                            else:
                                upgrd_cost = 99999999
                            self.brow.find_element_by_class_name('navigation_back').click()

                        if self.curr_icecubes > upgrd_cost and prev_lvl > buildings_lvl:
                            upd_posibility[str(idx+1)] = True  # .append(True)
                            prev_lvl = buildings_lvl
                        else:
                            upd_posibility[str(idx+1)] = False
                            prev_lvl = buildings_lvl
                    else:
                        upd_posibility[str(idx+1)] = False
                        prev_lvl = buildings_lvl

                # 2, 3, 5 in css - miner, tower, storage

                for i, u_pas in upd_posibility.items():
                    if u_pas:
                        #upgrade storage
                        upgrade_building(i)

                    # elif lvls[1] != lvls[2] and upd_posibility[1]:
                    #     #upgrade miner
                    #     upgrade_building(1)
                    # elif upd_posibility[2]:
                    #     #upgrade tower
                    #     upgrade_building(2)

    def ice_light(self):

        def findlight_timer_exist():
            css_selec = 'a.icetown_place > div.icetown_area6'
            self.brow.find_element_by_css_selector(css_selec).click()

            timer = 0
            try:
                
                wait = WebDriverWait(self.brow, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, 'navigation_back'))
                )
                time_text = self.brow.find_element_by_css_selector(
                    'div.lh30 > div > b.timer > span').text
                parts = time_text.split(':')
                timer = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                self.icelight_timer = time.time() + timer
                # self.brow.find_element_by_class_name('navigation_back').click()
                self.brow.find_element_by_id('navigation').click()
                return True

            except:
                self.brow.find_element_by_id('navigation').click()
                return False

        if self.icelight_timer < time.time():
            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.ID, 'm3'))
            )
            self.brow.find_element_by_id('m3').click()

            wait = WebDriverWait(self.brow, 60).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'village_image12'))
            )
            self.brow.find_element_by_class_name('village_image12').click()

            wait = WebDriverWait(self.brow, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.icetown_place > div.icetown_area6'))
            )
            self.brow.find_element_by_css_selector('a.icetown_place > div.icetown_area6').click()
            # if not findlight_timer_exist():
            try:
                wait = WebDriverWait(self.brow, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.lh30 > div.button_new'))
                )
                go_btns = self.brow.find_elements_by_css_selector('div.lh30 > div.button_new')

                for btn in go_btns:
                    if 'ОТПУСТИТЬ' in btn.text:
                        lights = self.brow.find_elements_by_css_selector('div.w130 > img')
                        if len(lights) == 3:
                            btn.click()
                            time.sleep(1)
            except:
                pass

            if self.ice_repair():
                try:
                    # start button!
                    wait = WebDriverWait(self.brow, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.icetown_result2 > div.button_new'))
                    )
                    self.brow.find_element_by_css_selector('div.icetown_result2 > div.button_new').click()
                except:
                    pass

                try:
                    wait = WebDriverWait(self.brow, 5).until(
                                EC.visibility_of_element_located(
                                    (By.CSS_SELECTOR, 'div.dflex > b.timer > span'))
                                )
                    time_text = self.brow.find_element_by_css_selector(
                                            'div.dflex > b.timer > span').text
                    parts = time_text.split(':')
                    timer = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                    self.icelight_timer = time.time() + timer
                except:
                    pass

    def ice_repair(self):
        btn_repair = False
        try:
            wait = WebDriverWait(self.brow, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.bgr_red > div.button_new'))
            )
            btn_repair = self.brow.find_element_by_css_selector('div.bgr_red > div.button_new')
        except:
            return True

        if btn_repair:
            repair_cost = self.remove_dot(self.brow.find_element_by_css_selector('div.pl10 > div > b').text)
            if self.curr_icecubes > repair_cost:
                btn_repair.click()
                return True
            else:
                return False

    def contraband_click(self):
        self.brow.find_element_by_id('contraband_sale_start').click()

    def st_valentine(self):
        self.brow.refresh()

        cur_url = self.brow.current_url

        shield = False

        wait = WebDriverWait(self.brow, 5).until(
                EC.element_to_be_clickable((By.ID, 'm8'))
            )
        try:
            shield = self.brow.find_element_by_id('valentine_2015_heart')
        except:
            pass

        if shield:  # EC.visibility_of_element_located((By.ID, 'valentine_2015_heart')):
            shield.click()

            wait = WebDriverWait(self.brow, 5).until(
                EC.element_to_be_clickable((By.ID, 'm8'))
            )
            self.brow.get(cur_url)
        else:
            self.brow.get('http://avatar.botva.ru/house.php?tab=4')
            wait = WebDriverWait(self.brow, 5).until(
                EC.element_to_be_clickable((By.ID, 'm8'))
            )
            h_m_s = self.brow.find_element_by_css_selector('div.mb10 > div.w100 > span').text
            self.valentine_timer = int(h_m_s.split(':')[0]) * 3600 + int(h_m_s.split(':')[1]) * 60 + int(h_m_s.split(':')[2]) + time.time()

        # except:
        #     time.sleep(1)

