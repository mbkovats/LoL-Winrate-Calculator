from dotenv import load_dotenv
import os
import pygsheets
import json
import requests
import time

load_dotenv()
api_key = os.environ.get('api_key')

def main():
    ranks = ['IRON','BRONZE','SILVER','GOLD','PLATINUM','EMERALD','DIAMOND']
    apex = ['MASTER','GRANDMASTER']
    division = ['IV','III','II','I']
    headers = {"X-Riot-Token": api_key}
    response = requests.get(f'https://na1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/CHALLENGER/I?page=1', headers=headers)
    for rank in ranks:
        if rank == 'PLATINUM':
            time.sleep(1)
        for num in division:
            request = f'https://na1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{rank}/{num}?page=1'
            response.update(requests.get(request, headers=headers))
    for rank in apex:
        request = f'https://na1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{rank}/I?page=1'
        response.update(requests.get(request, headers=headers))
    
    print(response.loads())
            
            