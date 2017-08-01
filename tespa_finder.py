import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

def find_players(match_link, option):
    link = urlopen(match_link)
    soup = BeautifulSoup(link.read(), "html.parser")
    print("Page accessed...")
    
    if option == 0: 
        #Parsing html for player IDs from match page
        rows = soup.find(id ='content').find_all('p')
        del rows[0]
               
    else:
        #Parsing html for player IDs from team page
        rows = soup.find(id = 'content').find_all("td", {"class" : "text-break"})
        
    #Cleaning up the names. I could probably have used regex when finding them but was too lazy
    for i in range(len(rows)):
        rows[i] = rows[i].get_text().replace('#', '-').strip() 
    
    return(rows)






def find_sr (rows):    
    #Setting up links to profiles
    profile = 'https://playoverwatch.com/en-us/career/pc/us/{}'
    links = [profile.format(tags)
             for tags in rows]  

    players = []

    #Open links to profiles and extract SRs
    for i, link in enumerate(links):
        try:
            players.append(1)
            players[i] = urlopen(link)
            soup = BeautifulSoup(players[i].read(), "html.parser")
            sr = soup.find("div", {"class" : "u-align-center h6"})
            sr = str(sr)    
            sr = sr.replace('<div class="u-align-center h6">', '').replace('</div>', '')
            print(rows[i], ':' , sr)
        except:
            sys.stdout.write(rows[i])
            sys.stdout.write('\'s name has weird characters. Look it up here:\n')
            sys.stdout.write('https://playoverwatch.com/en-us/career/pc/us/')
            sys.stdout.write(rows[i])
            print()

link_type = input("0 if match page, 1 if team page: ")
link = input("Paste match link below:\n")
players = find_players(link, link_type)
find_sr(players)
