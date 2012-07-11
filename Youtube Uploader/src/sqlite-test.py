# -*- coding: utf-8 -*-
"""
Created on Wed Feb 01 08:59:57 2012

@author: wkentler
"""

import sqlite3
import time
 
connection = sqlite3.connect('test.db')

cursor = connection.cursor()

#cursor.execute('CREATE TABLE mytable (Id INTEGER PRIMARY KEY, Date TEXT, Entry TEXT)')
#connection.commit()

#today=time.strftime("%A, %B %d, %Y")
#today
#cursor.execute('INSERT INTO mytable VALUES(null, ?, ?)', (today, "This entry could be the first item on a To-Do List, or it could be a journal entry, or whatever you want."))
#cursor.execute('INSERT INTO mytable VALUES(null, ?, ?)', (today, "To-Do: Write an SQLite3 tutorial!"))
#connection.commit()

cursor.execute('SELECT * FROM mytable')
allentries=cursor.fetchall()
allentries
for x in allentries:
  print "Item number: " + str(x[0]) + "  Date: " + x[1] + "  Entry: " + x[2]

cursor.close()