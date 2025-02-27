from dotenv import load_dotenv
import os
import json
import requests
import time
import datetime
import pygsheets

load_dotenv()
api_key = os.environ.get('api_key')
headers = {"X-Riot-Token": api_key}
client = pygsheets.authorize(service_account_file='JSONs\\riot-spreadsheet-938829989662.json')


def get_mastery_sheet(sheet):
    wks = sheet.sheet1
    mastery = {}
    for row in wks:
        mastery[row[0]] = {row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20]}
    return mastery

def update_mastery_sheet(users, sheet, remaining):
    wks = sheet.sheet1
    wks.link()
    mastery = get_mastery_sheet(sheet)
    new_mastery = {}
    maxwait = 0
    for user in users:
        puuid = user['puuid']
        if puuid not in mastery:
            if maxwait == 5:
                #time.sleep(115)
                #maxwait = 0
                break
            elif remaining == 0:
                time.sleep(1)
                remaining = 20
                maxwait += 1
            else:
                request = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}'
                response = requests.get(request, headers=headers).json()
                new_mastery[puuid] = []
                for champion in response:
                    if champion['championPoints'] >= 50000 and len(new_mastery[puuid]) < 20:
                        new_mastery[puuid].append(champion['championId'])
                    else:
                        break
                remaining -= 1
    for user in new_mastery.keys():
        row = [user]
        row.extend(new_mastery[user])
        wks.append_table(row)
    
    wks.unlink()
    return
    
    
def get_users():
    users = []
    #ranks = ['EMERALD','DIAMOND']
    apex = ['MASTER','GRANDMASTER','CHALLENGER']
    #division = ['IV','III','II','I']
    '''for rank in ranks:
        for num in division:
            request = f'https://na1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{rank}/{num}?page=1'
            users.extend(requests.get(request, headers=headers).json())'''
    for rank in apex:
        request = f'https://na1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{rank}/I?page=1'
        users.extend(requests.get(request, headers=headers).json())
    return users
    
def get_matches(remaining, users):
    maxwait = 0
    matches = {}
    index = 0
    while(index < len(users)):
        if remaining > 0:
            puuid = users[index]['puuid']
            request = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime=116208000&type=ranked&start=0&count=100'
            matches[puuid] = requests.get(request, headers=headers).json()
            remaining -= 1
            index += 1
        elif maxwait < 5:
            time.sleep(1)
            remaining = 20
            maxwait += 1
        else:
            time.sleep(115)
            maxwait = 0
def main():
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1XVmIqilXdGTqx5Ha-wdyI0MpQy2IMsFn6E_MKAwG7rU/edit?usp=sharing')
    users = get_users()
    remaining = 20
    if len(users) > 0:
        remaining = 17
    #matches = get_matches(remaining, users)
    update_mastery_sheet(users,sheet,remaining)
            
            
if __name__ == "__main__":
    print(datetime.datetime.now().strftime("%H:%M:%S"))
    main()
            
            