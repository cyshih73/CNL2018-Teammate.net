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

def match_criteria(m1,m2):
    s1 = m1[0] * 1 + m1[1] * 0.5 + m1[2] * 0.5
    s2 = m2[0] * 1 + m2[1] * 0.5 + m2[2] * 0.5 + 1e-10
    return (s1 / s2) < (3 / 2) and (s1 / s2) > (2 / 3)
    

def pairing(uid, meta_data):
    # Pairup users
    dblock = FileLock("db.lock", timeout=1)
    dblock.acquire()
    
    db = sqlite3.connect("./user_gamedata.db3")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM lineupPool where uid != '%s'" % uid)
    results = cursor.fetchall()
    i = 0
    try:
        # uid | timestamp | v1 | v2 | v3
        for result in results: 
            if match_criteria(meta_data, result[2:]):
                roomcode = random_pool()
                cursor.execute("REPLACE INTO uid2room values ( '" + str(result[0]) + "', '" + str(roomcode) + "')")
                
                cursor.execute("REPLACE INTO uid2room values (?,?)", (result[0], roomcode))
                cursor.execute("REPLACE INTO uid2room values (?,?)", (uid, roomcode))
                cursor.execute("DELETE FROM lineupPool WHERE uid='%s'" % uid)
                cursor.execute("DELETE FROM lineupPool WHERE uid='%s'" % result[0])
                db.commit()
                break
            
        db.close()
        
    finally:
        dblock.release()

if __name__ == "__main__":
    pairing("4REsHw2bCENPWxF8Ld0MEjCXJUO2121231231",[1,2,3])
