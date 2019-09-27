# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 00:13:12 2019

@author: giova
"""


from urllib.request import urlopen

from bs4 import BeautifulSoup

import pandas as pd

import numpy as np

from scipy import stats

import sys


# URL to Format

url_template = "https://www.pro-football-reference.com/years/2019/week_{week_num}.htm"



# Iterate Player Data Frame for Each Year Specified





for itorator in range(len(sys.argv)):

    week_num=sys.argv[itorator]

    url = url_template.format(week_num=week_num)  # get the url

    

    html = urlopen(url)



    soup = BeautifulSoup(html, 'html.parser')
    

    #getWinningTeamAndScore
    iteration=0;
    drawCount=0;
    gameCount=len(soup.findAll('table',{'class':'teams'}))
    winningTeamArr=[]
    winningTeamScoreArr=[]
    losingTeamArr=[]
    losingTeamScoreArr=[]
    drawTeam1TeamScoreArr=[]
    drawTeam1TeamArr=[]
    drawTeam2TeamArr=[]
    drawTeamScore2TeamScoreArr=[]
    gameDatArr=[]
    appended_data=[]
    while(gameCount>iteration): 
        winnerBlock=soup.findAll('table',{'class':'teams'})[iteration]
        
        #winningTeam=winnerBlock.find('tr',{'class':'winner'}).find('td',attrs={'class': 'right'}).get_text()
        
        try:
            losingTeam=winnerBlock.find('tr',{'class':'loser'}).find('td',attrs={'class': None}).find('a').getText()
            winningTeam=winnerBlock.find('tr',{'class':'winner'}).find('td',attrs={'class': None}).find('a').getText()
            losingTeamScore=winnerBlock.find('tr',{'class':'loser'}).find('td',attrs={'class': 'right'}).get_text()
            winningTeamScore=winnerBlock.find('tr',{'class':'winner'}).find('td',attrs={'class': 'right'}).get_text()
            gameDateBlock=winnerBlock.find('tr',{'class':'date'}).find('td').get_text()
            losingTeamScoreArr.append(losingTeamScore)
            losingTeamArr.append(losingTeam)
            winningTeamArr.append(winningTeam)
            winningTeamScoreArr.append(winningTeamScore)
            gameDatArr.append(gameDateBlock)
            print(losingTeam+":"+losingTeamScore+"|"+winningTeam+":"+winningTeamScore+" => "+gameDateBlock)
        except: 
            drawCount+=1
            drawTeam1=winnerBlock.findAll('tr',{'class':'draw'})[0].find('td',attrs={'class': None}).find('a').getText()
            drawTeamScore1=winnerBlock.findAll('tr',{'class':'draw'})[0].find('td',attrs={'class': 'right'}).get_text()           
            drawTeam2=winnerBlock.findAll('tr',{'class':'draw'})[1].find('td',attrs={'class': None}).find('a').getText()
            drawTeamScore2=winnerBlock.findAll('tr',{'class':'draw'})[1].find('td',attrs={'class': 'right'}).get_text() 
            gameDateBlock=winnerBlock.find('tr',{'class':'date'}).find('td').get_text()
            losingTeamScoreArr.append(drawTeamScore1)
            losingTeamArr.append(drawTeam1)
            winningTeamArr.append(drawTeam2)
            winningTeamScoreArr.append(drawTeamScore2)
            gameDatArr.append(gameDateBlock) 
            print(losingTeam+":"+losingTeamScore+"|"+winningTeam+":"+winningTeamScore+" => "+gameDateBlock)
        finally:
            print(gameCount)
            iteration+=1
       
    initial_data = {'Losing Team': losingTeamArr,  
                'Losing Team Score': losingTeamScoreArr,  
                'Winning Team': winningTeamArr,  
                'Winning Team Score': winningTeamScoreArr, 
                'Game Date':gameDatArr
               } 
    nfl_df = pd.DataFrame(initial_data,columns=['Losing Team',  'Losing Team Score','Winning Team',  'Winning Team Score','Game Date'])
    print(nfl_df)
    nfl_df.to_csv('myfile.csv')

   


