from flask import Flask, jsonify, request
import sqlite3
import time

app = Flask(__name__)
 
@app.route('/')
def Nothing():
    return "This is Teammate.net\'s backend"

@app.route('/lineup/<uid>', methods=['GET'])
def Lineup(uid):
    db = sqlite3.connect("./user_gamedata.db3")    
    cursor = db.cursor()
    cursor.execute("INSERT INTO lineupPool values (" + uid + "," + str(time.time()) + ")")
    db.commit()

    success = False
    #TODO: Lineup algorithm
    
    if success:
        output = "{ 'result': success, 'room': " + str(roomcode) + "}"
    else: output = "{ 'result': fail }"
    db.close()
    return jsonify(output)

@app.route('/record/<uid>', methods=['POST'])
def report_post_game(uid):
    db = sqlite3.connect("./user_gamedata.db3")
    cursor = db.cursor()
    print("INSERT INTO gameData values (" + uid + ",\"" + str(request.get_json(force=True)['record']) + "\")")

    try:
        cursor.execute("INSERT INTO gameData (uid, record) values (" + uid + ",\"" + str(request.get_json(force=True)['record']) + "\")")
        db.commit()
        output = "{ 'result': success }"
    except:
        output = "{ 'result': fail }"
    db.close()
    return jsonify(output)

app.run(debug=True, host='0.0.0.0', port=5566)


"""
Things to remember:
    cursor.execute("SELECT * FROM uid2room WHERE uid=" + uid)
    results = cursor.fetchall()
    output = 0
    if len(results) > 0:
        for record in results:
            output = int(record[1])
"""