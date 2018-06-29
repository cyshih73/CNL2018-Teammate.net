import sqlite3
from IPython import embed
u = {
        'Tab':'X',
        'Meta':'O',
        'Alt':'O',
        'Shift':'O',
        'Control':'O',
        'Enter':'O',
        'Unidentified':'O',
        'Escape':'O',
        'ArrowUP':'O',
        'ArrowDown':'O',
        'ArrowLeft':'O',
        'ArrowRight':'O'}
u2 = {
        'w':'x',
        's':'x',
        'd':'x',
        'a':'x',
        'W':'x',
        'S':'x',
        'D':'x',
        'A':'x',
        '1':'x',
        '2':'x',
        '3':'x',
        '4':'x',
        '5':'x',
        '6':'x',
        ' ':'x',
        'r':'x',
        'e':'x',
        'm':'x',
        'R':'x',
        'E':'x',
        'M':'x'}


def get_meta_data(cursor, uid):
    cursor.execute("SELECT * FROM gameData where uid == '%s'" % uid)    
    data = cursor.fetchall()
    rate, l, mouse = [], [], []
    
    if len(data) == 0:
        return 0.1,0.1,1
    
    for n, id, record in data:
        record = record.split('|')[0]
        if len(record) < 10: continue
        for k, v in u.items():
            record = record.replace(k, v)
        for k, v in u2.items():
            record = record.replace(k, v)
        rate.append((record.count('x') + record.count('X')) / len(record))
        mouse.append((record.count('X')) / len(record))
        l.append(len(record))
        #print(record)
    
    return sum(rate) / len(rate), sum(mouse) / len(mouse), sum(l) / len(l)

if __name__ == "__main__":
    db = sqlite3.connect("./user_gamedata.db3")
    cursor = db.cursor()
    from Pairing import *
    s1=get_meta_data(cursor, "4REsHw2bCENPWxF8Ld0MEjCXJUO2")
    s2=get_meta_data(cursor, "m54F1Vk5McTbEe6WXTg85aoqG1J3")
    print(match_criteria(s1,s2))
    print(match_criteria(s2,s1))
