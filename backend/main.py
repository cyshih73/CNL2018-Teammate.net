from flask import Flask, jsonify, request
from filelock import Timeout, FileLock
import subprocess
import sqlite3
import time

app = Flask(__name__)

# Check uid2room table to find if paired or not
def pair_up(uid):
    dblock = FileLock("db.lock", timeout=1)
    dblock.acquire()
    try:
        db = sqlite3.connect("./user_gamedata.db3")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM uid2room WHERE uid='" + str(uid) + "'")
        results = cursor.fetchall()
        db.close()
    finally:
        dblock.release()

    roomcode = ""
    if len(results) > 0:
        for record in results:
            roomcode = record[1]
        return roomcode
    else:
        return ""
    
@app.route('/')
def Nothing():
    return "This is Teammate.net\'s backend"

@app.route('/lineup/<uid>', methods=['GET'])
def Lineup(uid):
    try:
        roomcode = pair_up(uid)
        if roomcode == "":
            # Lineup the user
            dblock = FileLock("db.lock", timeout=1)
            dblock.acquire()
            try:
                db = sqlite3.connect("./user_gamedata.db3")
                cursor = db.cursor()
                cursor.execute("REPLACE INTO lineupPool values ('" + uid + "'," + str(time.time()) + ")")
                db.commit()
                db.close()
            finally:
                dblock.release()

            #TODO: Pairup algorithm
            proc = subprocess.Popen(['python3', 'Pairing.py'], stdout=subprocess.PIPE)
            proc.wait()
            roomcode = pair_up(uid)
            
        if roomcode != "":
            output = { 'result': 'success', 'room': str(roomcode) }
        else: 
            output = { 'result': 'fail' }
    except:
        print("ERROR occured, please check")
        output = { 'result': 'fail' }

    return jsonify(output)

@app.route('/record/<uid>', methods=['POST'])
def game_report(uid):
    dblock = FileLock("db.lock", timeout=1)
    dblock.acquire()
    try:
        db = sqlite3.connect("./user_gamedata.db3")
        cursor = db.cursor()
        cursor.execute("INSERT INTO gameData (uid, record) values ('" + uid + "','" + str(request.get_json(force=True)['record']) + "')")
        
        # Delete user from table uid2room
        cursor.execute("DELETE FROM uid2room WHERE uid='" + uid + "'")
        db.commit()
        db.close()

        output = { 'result': 'success' }

    except:
        output = { 'result': 'fail' }
        
    finally:
        dblock.release()

    return jsonify(output)

app.run(debug=True, host='0.0.0.0', port=5566)

# IGNORE THESE
"""
Things to remember:
    cursor.execute("SELECT * FROM uid2room WHERE uid=" + uid)
    results = cursor.fetchall()
    output = 0
    if len(results) > 0:
        for record in results:
            output = int(record[1])
"""