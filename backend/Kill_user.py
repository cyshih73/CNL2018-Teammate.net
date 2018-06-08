from filelock import Timeout, FileLock
import sqlite3
import datetime, time

while 1:
    dblock = FileLock("db.lock", timeout=1)
    dblock.acquire()
    try:
        db = sqlite3.connect("./user_gamedata.db3")
        cursor = db.cursor()

        # DELETE timeout
        count = 0
        cursor.execute("SELECT * FROM lineupPool")
        results = cursor.fetchall()
        for record in results:
            if round(time.time()) - round(record[1]) > 15:
                count += 1
                cursor.execute("DELETE FROM lineupPool WHERE uid='" + str(record[0]) + "'")
                db.commit()
        db.close()
        # Print message
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ": " + str(count) + " user(s) has/have deleted")
    
    except:
        print("ERROR occured, please check")

    finally:
        dblock.release()
        time.sleep(10)
