import sqlite3
import time
import datetime
import random
import random
import threading
import time
from functools import partial
from ophyd.status import MoveStatus, wait as status_wait
from ophyd.status import MoveStatus as MoveStatus
from ophyd.sim import SynAxis
from bluesky import RunEngine
from bluesky.plans import scan
from bluesky.callbacks.best_effort import BestEffortCallback
from ophyd.sim import SynGauss

from status import StatusAxis
import getpass
import pandas

class waitingHook():
    def __init__(self, motorName):
        self.conn = sqlite3.connect('statusDB.db')
        self.create_table(motorName)
        self.motorName = motorName

    def __call__(self, statuses):
        if statuses!=None:
            for stat in statuses:
                    if isinstance(stat, MoveStatus):
                        user = getpass.getuser()
                        stat.add_callback(partial(self.data_entry, status = stat, user = user))

    def data_entry(self, status, user):
        conn=self.conn
        c = conn.cursor()
        start = status.start_ts
        finish = status.finish_ts
        start_ts = datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
        finish_ts = datetime.datetime.fromtimestamp(finish).strftime('%Y-%m-%d %H:%M:%S')
        start_pos = status.start_pos
        finish_pos = status.finish_pos
        target = status.target
        user = user
        temp = status.success
        motorName = self.motorName
        if temp==0:
            success = "False"
        else:
            success = "True"

        c.execute("INSERT INTO '"+motorName+"' (start_ts, finish_ts, start_pos, finish_pos, target, success, user) VALUES(?, ?, ?, ?, ?, ?, ?)",
                  (start_ts, finish_ts, start_pos, finish_pos, target, success, user)),

        conn.commit()



    def create_table(self, motorName):
        conn=self.conn
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS '"+motorName+"'(start_ts TEXT, finish_ts TEXT, start_pos INTEGER, finish_pos INTEGER, target INTEGER, success TEXT, user TEXT)")
        conn.commit()
        c.close()


    def get_data(self, motor, start_time, stop_time):
        conn=self.conn
        c = conn.cursor()
        query = "SELECT start_ts, finish_ts, ROUND(start_pos), ROUND(finish_pos), ROUND(target), success, user FROM '"+motor+"' WHERE DATETIME(start_ts) >= '"+start_time+"' AND DATETIME(start_ts) <= '"+stop_time+"'"
        df = pandas.read_sql_query(query, conn)

        conn.commit()
        c.close()
        return df
