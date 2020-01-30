//testing
import bs4 as bs
import requests
import pandas as pd
import datetime
from datetime import datetime
import mysql.connector
from sqlalchemy import create_engine
import time
import random

pd.set_option('display.max_columns', 100)

# 2016 to 2017 Season is 10/25/16 to 06/12/17
# 2017 to 2018 Season is 10/17/17 to 6/8/18
# Edit the start and end dates to scrape below, dates are inclusive. (i.e. 06/26/2016 to 06/28/2016, includes the 26th, 27th, 28th)
startDate = '10/18/2018'
endDate = '10/19/2018'


dates = pd.date_range(startDate,endDate)
print(dates)

for date in dates:
    # Iterate through each page
    link = requests.get('https://www.basketball-reference.com/boxscores/?month={}&day={}&year={}'.format(date.month, date.day, date.year))
    soup = bs.BeautifulSoup(link.text,'html.parser')

    # Find all game summaries or each box that represents a game on the webpage
    gameSummaries = soup.find_all('div', {'class': 'game_summary expanded nohover'})
    allGameQuarters = []
    allGamePoints = []
    allTeams = []

    ## GET DATA POINTS 
    # Loop through each summary, and obtain data for Points and Teams
    for summary in gameSummaries:
        games = summary.find_all('table', {'class': None})

        # Get team names
        teams = summary.find_all('table', {'class': 'teams'})
        for team in teams:
            teamName = team.find_all('td', {'class': None})
            [allTeams.append(name.text) for name in teamName]

        # Get points per quarter for each team
        for game in games:
            quarterPoints = game.find_all('td', {'class': 'center'})
            print(len(quarterPoints))
            x = []
            for points in quarterPoints:
                x.append(points.text)
                if len(quarterPoints) == len(x):
                    allGamePoints.append(x)


    print(allTeams)
    print(allGamePoints)

    numberGames = len(allGamePoints)
    pointsTable = pd.DataFrame() # Create a table to insert data 

    ## ARRANGE DATA INTO TABULAR FORMAT
    for game in range(numberGames): # Loop through each game
        numPoints = int(len(allGamePoints[game]))
        print("numPoints", numPoints)
        numQuarters = int(numPoints / 2)
        awayTeam = allTeams[game*2]
        homeTeam = allTeams[game*2 + 1]
        for point in range(numPoints):
            points = allGamePoints[game][point]
            if point < numQuarters:
                team = allTeams[game * 2]
                quarter = point + 1
                homeAway = 'A'
            else:
                team = allTeams[game * 2 + 1]
                quarter = (point + 1) - numQuarters
                homeAway = 'H'

            gameId = int(game + 1)
            pointsEntry = [gameId, team, quarter, points, homeAway]
            pointsTable = pointsTable.append(pd.Series(pointsEntry), ignore_index=True)

    # Add column names and amend data types of table
    
    if not pointsTable.empty:
        pointsColumns = ['game_id', 'team', 'quarter', 'points', 'homeAway']
        pointsTable.columns = pointsColumns
        pointsTable.insert(0,'date',date)
        pointsTable = pointsTable.astype({'game_id': int, 'quarter': int,'points': int})
        print(pointsTable)
    
        engine = create_engine('mysql+mysqlconnector://root:<PASSWORD>@localhost:3306/nba', echo=False)  #This line should be declared up top.
        pointsTable.to_sql(name='points', con=engine, if_exists ='append', index=False)
        print(date, "Appended to table successfully")

    # Sleep between 5 and 15 seconds
    t = random.uniform(5.0, 15.0)
    print("Sleeping for {} seconds, next page to scrape for {}...".format(t, date))
    time.sleep(t)






