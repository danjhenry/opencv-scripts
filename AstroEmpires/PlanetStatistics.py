import requests
import re
import time

#enter login Information before using.
email = ''
password = ''


testURL = input('Enter base url to test: ')
logUrl = 'https://kepler.astroempires.com/login.aspx?href='

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Connection' : 'keep-alive'
        }

def login(logUrl):
    payload = {
        'email' : email,
        'pass' : password,
        'navigator' : 'Netscape',
        'hostname' : 'kepler.astroempires.com',
        'javascript' : 'true',
        'post_back' : 'true'
        }
    sess = requests.Session()
    logReq = sess.post(logUrl, data=payload, headers=headers)
    return sess
    
def fleetData(planetUrl, sess):
    total = {}
    fleets = {}
    dataReq = sess.get(planetUrl, headers=headers)
    pageData = dataReq.text
    planetData = re.findall(r'map.aspx(.*?)Arriving size', pageData)
    loc = str(planetData)[7:19]
    fleetID = set(re.findall(r"fleet=(.*?)'>", str(planetData)))
    for ID in fleetID:
        ships = {}
        ID = ID.replace('\\', '')
        fleetUrl = 'http://kepler.astroempires.com/fleet.aspx?fleet={}'.format(ID)
        fleetPage = sess.get(fleetUrl, headers=headers)
        fleetData = re.findall(r".show()(.*?)<center>Fleet Size:", fleetPage.text)
        owner = re.findall(r"player=(.*?)]  ", str(fleetData))
        owner = re.findall(r'[A-Za-z]', str(owner))
        owner = ''.join(owner)
        name = re.findall(r"] (.*?)</a>", str(fleetData))
        if name:
            units = re.findall(r"Units(.*?)</table>", str(fleetData))
            units = str(units).replace('\\', '')
            types = re.findall(r"<b>(.*?)</b>", units)
            numbers = re.findall(r"'center'>(.*?)</td>", units)
            if name[0] not in fleets:
                fleets[name[0]] = {}
            for index, ship in enumerate(types):
                if ship in fleets[name[0]]:
                    fleets[name[0]][ship] += int(float(numbers[index].replace(',', '')))
                else:
                    fleets[name[0]][ship] = int(float(numbers[index].replace(',', '')))
            if owner not in total:
                total[owner] = {}
            fleets[name[0]]['Corp'] = owner
            
    for player in fleets:
        owner = fleets[player]['Corp']
        for ship in fleets[player]:
            if ship != 'Corp':
                if ship in total[owner]:
                    total[owner][ship] += fleets[player][ship]
                else:
                    total[owner][ship] = fleets[player][ship]
            
    return fleets, total, loc
        
def main():
    logSession = login(logUrl)
    data, total, loc = fleetData(testURL, logSession)
    order = ('Fighters', 'Bombers', 'Heavy Bombers', 'Ion Bombers',
             'Corvette', 'Destroyer', 'Frigate', 'Ion Frigate',
             'Recycler', 'Scout Ship', 'Outpost Ship', 'Cruiser',
             'Carrier', 'Heavy Cruiser', 'Battleship', 'Fleet Carrier',
             'Dreadnought')
    print('Location {}'.format(loc))
    for name in data:
        print('{} {}'.format(data[name]['Corp'], name), end=' [')
        for ship in order:
            if ship in data[name]:
                print('{}: {}'.format(ship, data[name][ship]), end=', ')
        print(']')
    for corp in total:
        print('Total {}'.format(corp), end=' [')
        for ship in order:
            if ship in total[corp]:
                print('{}: {}'.format(ship, total[corp][ship]), end=', ')
        print(']')
main()


