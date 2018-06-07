from filelock import Timeout, FileLock
import sqlite3
import random
import sys

# Random a 8 chars roomcode
def random_pool():
    roomcode = ""
    for i in range(8):
        tmp = random.randrange(48, 84)
        if tmp > 57: 
            tmp += 7
        roomcode = roomcode + str(chr(tmp))
    return roomcode


# Pairup users
dblock = FileLock("db.lock", timeout=1)
dblock.acquire()
try:
    db = sqlite3.connect("./user_gamedata.db3")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM lineupPool")
    results = cursor.fetchall()
    for i in range(len(results)):
        if i+1 < len(results):
            roomcode = random_pool()
            cursor.execute("REPLACE INTO uid2room values ( " + str(results[i][0]) + ", \"" + str(roomcode) + "\")")
            cursor.execute("REPLACE INTO uid2room values ( " + str(results[i+1][0]) + ", \"" + str(roomcode) + "\")")
            cursor.execute("DELETE FROM lineupPool WHERE uid=" + str(results[i][0]))
            cursor.execute("DELETE FROM lineupPool WHERE uid=" + str(results[i+1][0]))
            db.commit()
    db.close()
    
finally:
    dblock.release()
