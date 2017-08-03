import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np


# the _1 refers to the option chosen, not players on team 1
def find_players_1(link):
    link = urlopen(link)
    soup = BeautifulSoup(link.read(), "html.parser")
    
    #Parsing html for player IDs from team page
    rows = soup.find(id = 'content').find_all("td", {"class" : "text-break"})
        
    #Cleaning up the names. I could probably have used regex when finding them but was too lazy
    for i in range(len(rows)):
        rows[i] = rows[i].get_text().replace('#', '-').strip() 
    
    return(rows)

def find_team_1(link):
    #find team name on page
    link = urlopen(link)
    soup = BeautifulSoup(link.read(), "html.parser")
    name = soup.find("span", {"class" : "hgd-em"})    
    name = name.get_text().strip()
    return(name)

def find_players_0a(link):
    link = urlopen(link)
    soup = BeautifulSoup(link.read(), "html.parser")
    
    #Parsing html for player IDs from match page
    rows = soup.find(id ='content').find("div", {"class" : "col-xs-5 match-players"}).find_all('p')
    for i in range(len(rows)):
        rows[i] = rows[i].get_text().replace('#', '-').strip() 
    return(rows)    

def find_players_0b(link):    
    link = urlopen(link)
    soup = BeautifulSoup(link.read(), "html.parser")
    
    #Parsing html for player IDs from match page
    rows = soup.find(id ='content').find("div", {"class" : "col-xs-5 col-xs-offset-2 match-players text-right"}).find_all('p')
    for i in range(len(rows)):
        rows[i] = rows[i].get_text().replace('#', '-').strip() 
    return(rows)    


def find_team_0(link):
    #find team names from match page
    names = ["", ""]
    link = urlopen(link)
    soup = BeautifulSoup(link.read(), "html.parser")
    names[0] = soup.find(id="player1Container").get_text().strip()
    names[1] = soup.find(id="player2Container").get_text().strip()
    return(names)


def find_sr (tag):    
    #Setting up links to profiles
    profile = 'https://playoverwatch.com/en-us/career/pc/us/{}'
    link = profile.format(tag)

    #Open links to profiles and extract SRs
    try:
        site = urlopen(link)
        soup = BeautifulSoup(site.read(), "html.parser")
        sr = soup.find("div", {"class" : "u-align-center h6"})
        sr = str(sr)    
        sr = sr.replace('<div class="u-align-center h6">', '').replace('</div>', '')
    except:
        sr = ""
    return(sr)

def find_mains(tag):
    #Setting up links to profiles
    profile = 'https://playoverwatch.com/en-us/career/pc/us/{}'
    link = profile.format(tag)

    #Open links to profiles and extract mains:
    try:
        site = urlopen(link)
        soup = BeautifulSoup(site.read(), "html.parser")
        soup = soup.find(id = "competitive")
        main_list = soup.find_all("div", {"class" : "title"})
        main_list[0] = main_list[0].text.strip()
        main_list[1] = main_list[1].text.strip()
        main_list[2] = main_list[2].text.strip()
        mains = main_list[0:3]
        
    except:
        mains = link
        mains +=' Check it yourself, \'cuz I can\'t'
    return(mains)
    
#public static void main(String args[]){
option = int(input("0 if match page, 1 if team page, 2 if tag: "))
if option == 0:
    link = input("Paste link below:\n")
    teams = find_team_0(link)
    team1 = find_players_0a(link)
    team2 = find_players_0b(link)
    print(teams[0])
    srs1 = []
    srs2 = []
    for idx, player in enumerate(team1):
        sr = find_sr(player)
        srs1.append(1)
        srs1[idx] = sr
        mains = find_mains(player)
        print(player, ':', sr, '. Mains: ' , mains)
    #replace unranked people with 2500
    srs1 = [sr.replace('None', '2500') for sr in srs1]
    srs1 = list(map(int,srs1))
    print("Average sr: " , np.mean(srs1))

    print('\n', teams[1])
    for idx, player in enumerate(team2):
        sr = find_sr(player)
        srs2.append(1)
        srs2[idx] = sr
        mains = find_mains(player)
        print(player, ':', sr, '. Mains: ' , mains)
    srs1 = [sr.replace('None', '2500') for sr in srs2]
    srs2 = list(map(int,srs1))
    print("Average sr: ",np.mean(srs2))
elif option == 1:
    link = input("Paste link below:\n")
    team = find_team_1(link)
    print(team)
    players = find_players_1(link = link)
    srs = []
    for player in players:
        sr = find_sr(player)
        srs.append(1)
        srs[player] = sr
        mains = find_mains(player)
        print(player, ':', sr, '. Mains: ' , mains)
    map(lambda x:0 if x=="None" else x,srs)
    print(np.mean(srs))
        
elif option == 2:
    print("Paste tag below, make sure caps are accounted for.")
    tag = input("Make sure it follows the format @@@@@@@@-#####\n")
    tag = tag.replace('#', '-')
    sr = find_sr(tag)
    mains = find_mains(tag)
    print('SR :', sr, '. Mains: ', mains)
else:
    print("How could you mess that up?")
#}
