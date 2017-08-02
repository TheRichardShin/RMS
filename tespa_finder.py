import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

def find_players(link, option):
    link = urlopen(link)
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

    #Open links to profiles and extract SRs:
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
    
 
            

option = int(input("0 if match page, 1 if team page, 2 if tag: "))
if option <2:
    link = input("Paste link below:\n")
    players = find_players(link = link, option = option)
    for player in players:
        sr = find_sr(player)
        mains = find_mains(player)
        print(player, ':', sr, '. Mains: ' , mains)
else:
    print("Paste tag below, make sure caps are accounted for.")
    tag = input("Make sure it follows the format @@@@@@@@-#####\n")
    sr = find_sr(tag)
    mains = find_mains(tag)
    print('SR :', sr, '. Mains: ', mains)
