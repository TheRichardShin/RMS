import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

def open_and_read(link):
    link = urlopen(link)
    soup = BeautifulSoup(link.read(),"html.parser")
    return(soup)
    
# the _1 refers to the option chosen, not players on team 1
def find_players_1(soup):
    
    #Parsing html for player IDs from team page
    rows = soup.find(id = 'content').find_all("td", {"class" : "text-break"})
        
    #Cleaning up the names. I could probably have used regex when finding them but was too lazy
    for i in range(len(rows)):
        rows[i] = rows[i].get_text().replace('#', '-').strip() 
    
    return(rows)

def find_team_1(soup):
    #find team name on page
    name = soup.find("span", {"class" : "hgd-em"})    
    name = name.get_text().strip()
    return(name)

def find_players_0(soup, team):
    if team == 0:
        #Parsing html for player IDs from match page
        rows = soup.find(id ='content').find("div", {"class" : "col-xs-5 match-players"}).find_all('p')
    elif team == 1:
        rows = soup.find(id ='content').find("div", {"class" : "col-xs-5 col-xs-offset-2 match-players text-right"}).find_all('p')
    
    for i in range(len(rows)):
        rows[i] = rows[i].get_text().replace('#', '-').strip() 
    
    return(rows)    


def find_team_0(soup):
    #find team names from match page
    names = ["", ""]
    names[0] = soup.find(id="player1Container").get_text().strip()
    names[1] = soup.find(id="player2Container").get_text().strip()
    return(names)


def find_sr_main (tag):    
    #Setting up links to profiles
    profile = 'https://playoverwatch.com/en-us/career/pc/us/{}'
    link = profile.format(tag)

    #Open links to profiles and extract SRs
    try:
        link = open_and_read(link)
        sr = link.find("div", {"class" : "u-align-center h6"})
        sr = str(sr)    
        sr = sr.replace('<div class="u-align-center h6">', '').replace('</div>', '')
        soup = link.find(id = "competitive")
        main_list = soup.find_all("div", {"class" : "title"})
        #find top 3 most played
        main_list[0] = main_list[0].text.strip()
        main_list[1] = main_list[1].text.strip()
        main_list[2] = main_list[2].text.strip()
        mains = main_list[0:3]        
    except:
        sr = "None"
        mains = []
    return(sr, mains)


def display(soup, team_no):
    team_name = find_team_0(soup)
    team = find_players_0(link, team_no)
    print(team_name[team_no])
    srs= []
    for idx, player in enumerate(team):
        sr = find_sr_main(player)
        srs.append(1)
        srs[idx] = sr[0]
        print(player, ':', sr[0], '. Mains: ' , sr[1])
    #Sub unplaced people with imputation
    srs = [sr.replace('None', '0') for sr in srs]
    srs = list(map(int,srs))    
    avg = find_imp_avg(srs)
    srs = [avg if x == 0 else x for x in srs]
    print("Placeholder sr: ", avg)
    print("Effective sr: " , srs)
    print("Average sr: " , avg , " (should be same as placeholder)")
    return()

def find_imp_avg(srs):
    count = 0
    total = 0
    for i in srs:
        if i != 0:
            count += 1
            total += i
        else:
            count = count
    avg = total/count    
    
    return(avg)

def find_hero_pool(team):
    return(0)


def find_winner(soup):
    try:
        team1 = int(soup.find(id="team1_score")['value'])
        team2 = int(soup.find(id="team2_score")['value'])
        if (team1 + team2) > 0:
            return(team1>team2)
    except:
        return("forfeit")
    
    
#public static void main(String args[]){
option = int(input("0 if match page, 1 if team page, 2 if tag: "))

if option == 0:
    paste = input("Paste link below:\n")
    link = open_and_read(paste)
    display(link, 0)
    display(link,1)
    result = find_winner(link)
    try:
        print("The winner was ", find_team_0(link)[1- result])
    except:
        print("This was a", result)
        
        
        
elif option == 1:
    link = input("Paste link below:\n")
    team = find_team_1(link)
    print(team)
    players = find_players_1(link = link)
    srs = []
    for player in players:
        sr = find_sr_main(player)
        srs.append(1)
        srs[player] = sr[0]
        print(player, ':', sr[0], '. Mains: ' , sr[1])
        
elif option == 2:
    print("Paste tag below, make sure caps are accounted for.")
    tag = input("Make sure it follows the format @@@@@@@@-#####\n")
    tag = tag.replace('#', '-')
    sr = find_sr_main(tag)
    print('SR :', sr[0], '. Mains: ', sr[1])
    
else:
    print("How could you mess that up?")
#}
