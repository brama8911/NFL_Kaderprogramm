#access website

import urllib.request, urllib.parse, urllib.error
import re
from bs4 import BeautifulSoup
import os.path

#auf Tabellenseite gehen
myurl='https://www.ran.de/datenbank/us-sport/nfl/teams/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}

#request
req=urllib.request.Request(url=myurl, headers=headers)
with urllib.request.urlopen(req) as response:
    page_html=response.read().decode()

#eingrenzen auf Teams und Teams-dict erstellen
soup=BeautifulSoup(page_html, 'lxml')
table_total=soup.find('div', class_="hs-block hs-teams")
lst_teams_unsauber=table_total.find_all('td', class_="team-name team-name-")
teams = []
teams_dict = {}
#print(table_total)
for team in lst_teams_unsauber:
    teams.append(team.text)
    #print(team.text)
    team_link=team.find('a')
    team_link_str=str(team_link)
    team_id= team_link_str[31:35]
    teams_dict[team.text.lower()] = team_id
print('')

#ask for team
inp='x'
while inp.capitalize() != 'N': #for repetition after execution
    count = 0
    for team in teams:
        if count < 9:
            print(' ' + str(count+1) + '  ' + team)
        else:
            print(str(count+1) + '  ' + team)
        count += 1

    print('')
    while inp.lower() not in (team.lower() for team in teams):
        inp = input('Choose a team (Name or Number): ')
        try:
            x = int(inp)
            if x < 1:
                continue
            else:
                inp = teams[x-1]
                break
        except:
            for team in teams:
                if inp.lower() == team.lower():
                    inp = team
                    break
                else:
                    continue

        print('')

    #auf Kaderseite gehen
    myurl='https://www.ran.de/datenbank/us-sport/te' + teams_dict[inp.lower()] + '/kader/'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}

    #request
    req=urllib.request.Request(url=myurl, headers=headers)
    with urllib.request.urlopen(req) as response:
        page_html=response.read().decode()

    #eingrenzen auf Teams und Teams-dict erstellen
    soup=BeautifulSoup(page_html, 'lxml')
    table_players = soup.find('div', class_="hs-block hs-persons")
    lst_players = table_players.find_all('td', class_="person-name person-name-")

    # make and write to file
    path_name = os.getcwd()
    with open(os.path.join(path_name, 'Kader NFL', inp + ".txt"), 'w', encoding = 'ANSI') as f:
        f.write(inp + '\n')
        for player in lst_players:
            player = player.find('a').text
            #First and Last name
            namelst=player.split(' ')
            if len(namelst) == 2:
                f.write(player+'\n')
                f.write(namelst[1]+'\n')

            elif len(namelst) >= 3 and namelst[-1] in ['I', 'II', 'III', 'Jr.']:
                namelst.remove(namelst[-1])
                f.write(namelst[-2] + ' ' + namelst[-1]+'\n')
                f.write(namelst[-1]+'\n')
            else:
                f.write(namelst[-1]+'\n')
                f.write(namelst[-2] + ' ' + namelst[-1]+'\n')

    print('Mission accomplished! A file has been created...')
    print('')
    inp=input('Continue with another team? (Y/N): ')
