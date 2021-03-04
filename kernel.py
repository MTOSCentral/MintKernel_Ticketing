# MintTicketing - Fork Of Mint Kernel v1.1_PRERELEASE BY THE ORIGINAL DEVELOPER
"""
This file is part of Yau Yau Ticketing System v3.

Yau Yau Ticketing System v3
Copyright (C) 2021  Meow Tech Open Source

Yau Yau Ticketing System is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3 as published by
the Free Software Foundation.

Yau Yau Ticketing System is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this Yau Yau Ticketing System.  If not, see <https://www.gnu.org/licenses/>.
"""
from hashing import Hashing
from datetime import datetime
import sqlite3
import json
VERSION="0.0.5_engine"
class Kernel:
    def __init__(self):
        #print("Mint Engine")
        self.conn =sqlite3.connect('database\\database.sql', check_same_thread=False)
        self.cursor = self.conn.cursor()
    def version(self):
        global VERSION
        return VERSION
    def checkuser(self,username,password):
        hasher=Hashing()
        sqlstr='select * from user'
        self.cur=self.conn.execute(sqlstr)
        rows=self.cur.fetchall()
        cor=False
        for row in rows:
            if hasher.check(password,row[1]) and username == row[0]:
                cor=True
                return [True,row]
            #else:
                #pass
        if not cor:
            return [False]
    def checkuserexists(self,username):
        hasher=Hashing()
        sqlstr='select * from users'
        self.cur=self.conn.execute(sqlstr)
        rows=self.cur.fetchall()
        cor=False
        for row in rows:
            if username == row[0]:
                cor=True
                return True
            #else:
                #pass
        if not cor:
            return False
    def getvalue(self):
        with open("config\\ticketing.cfg.json","r+") as file1:
            return json.load(file1)["TicketNo"]
    def writevalue(self):
        reader=self.getvalue()
        with open("config\\ticketing.cfg.json","w+") as file:
            org={
                "TicketNo":str(int(reader)+1)
                }
            print("+1")
            towrite=json.dumps(org)
            file.write(towrite)
    def addconsumer(self,username,password,fullname):
        hasher=Hashing()
        sqlstr='select * from users'
        self.cur=self.conn.execute(sqlstr)
        rows=self.cur.fetchall()
        for row in rows:
            if username == row[0]:
                exist=True
                return "Exist"
            else:
                sqlstr=f'insert into users values("{username}","{hasher.hash(password)}","Consumer","{fullname}")'
                self.conn.execute(sqlstr)
                self.conn.commit()
                return "OK"
    def orderticket(self,type1,orderer):
        hasher=Hashing()
        sqlstr='select * from tickets'
        self.cur=self.conn.execute(sqlstr)
        rows=self.cur.fetchall()
        cor=False
        for row in rows:
            if type1 == row[0]:
                cor=True
        if cor:
            #Correct Type
            exists=self.checkuserexists(orderer)
            if exists:
                date="0000-00-00"
                value=int(self.getvalue())
                sqlstr=f'insert into ticket values("{type1}","{str(value+1)}","{orderer}","{date}")'
                self.conn.execute(sqlstr)
                self.conn.commit()
                self.writevalue()
            else:
                return "ERR"
        else:
            return 'ERR'

    def getavalibleticket(self):
        hasher=Hashing()
        sqlstr='select * from tickets'
        self.cur=self.conn.execute(sqlstr)
        rows=self.cur.fetchall()
        alls=[]
        for row in rows:
            alls.append({"Price":row[1],"TypeName":row[2],"Type":row[0]})
        return alls
    def chkrole(self,user,role):
        hasher=Hashing()
        sqlstr='select * from users'
        self.cur=self.conn.execute(sqlstr)
        rows=self.cur.fetchall()
        cor=False
        for row in rows:
            if user == row[0] and role == row[2]:
                cor=True
                return True
        if not cor:
            return False

"""
Meow Tech MintTicketing - Kernel For The Central Series Ticketing System
Central System Use The MintTicketing.
"""