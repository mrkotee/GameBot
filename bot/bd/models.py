from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os



Base = declarative_base()


class IceTownUpgrades(Base):
    __tablename__ = 'icetownupgrades'
    id = Column(Integer, primary_key=True)
    building_id = Column(Integer)
    building_lvl = Column(Integer)
    upgrade_cost = Column(Integer)

    def __init__(self, building_id, building_lvl, upgrade_cost):
        self.building_id = building_id
        self.building_lvl = building_lvl
        self.upgrade_cost = upgrade_cost

    def __str__(self):
        building_names = ['Tree', 'Miner', 'Tower', 'Leprecon', 'Storage', 'FireHouse']

        return "{}, lvl {} - {} icecubes".format(
            building_names[self.building_id], self.building_lvl, self.upgrade_cost)


class Dozor(Base):
    __tablename__ = 'dozor'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    gold = Column(Integer)

    def __init__(self, gold=1):
        self.date_time = dt.now()
        self.gold = gold

    def __repr__(self):
        return "{}, gold = {}" .format(self.date_time, self.gold)

    @property
    def date(self):
        # return dt.strptime(str(self.date_time), "%Y-%m-%d %H:%M:%S.%f").date()
        return self.date_time.date()

    @property
    def time(self):
        return self.date_time.strftime('%H:%M:%S')


class Harbour(Base):
    __tablename__ = 'harbour'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)

    def __init__(self):
        self.date_time = dt.now()

    def __repr__(self):
        return "{}" .format(self.date_time)

    @property
    def date(self):
        # return dt.strptime(str(self.date_time), "%Y-%m-%d %H:%M:%S.%f").date()
        return self.date_time.date()

    @property
    def time(self):
        return self.date_time.strftime('%H:%M:%S')


class Energy(Base):
    __tablename__ = 'energy'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    hundreds = Column(Integer)

    def __init__(self, hundreds):
        self.date_time = dt.now()
        self.hundreds = hundreds

    def __repr__(self):
        return "{}, {} сотни".format(self.date_time, self.hundreds)

    @property
    def date(self):
        # return dt.strptime(str(self.date_time), "%Y-%m-%d %H:%M:%S.%f").date()
        return self.date_time.date()

    @property
    def time(self):
        return self.date_time.strftime('%H:%M:%S')


class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    action = Column(String)

    def __init__(self, action):
        self.date_time = dt.now()
        self.action = action

    def __repr__(self):
        return "{} {}, {}".format(self.date, self.time, self.action)

    @property
    def date(self):
        # return dt.strptime(str(self.date_time), "%Y-%m-%d %H:%M:%S.%f").date()
        return self.date_time.date()

    @property
    def time(self):
        return self.date_time.strftime('%H:%M:%S')


if __name__ == '__main__':
    path = 'base.bd'

else:
    path = 'bot/bd/base.bd'

if not os.path.exists(path):
    engine = create_engine('sqlite:///%s' % path, echo=False)
    Base.metadata.create_all(bind=engine)

    
