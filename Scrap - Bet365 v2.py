import requests
import lxml
import sys
import traceback
import time
from random import choice
from bs4 import BeautifulSoup
from bs4 import NavigableString
from urlparse import urljoin
import csv
from multiprocessing import Pool
import multiprocessing
import copy
import re
import os
import time
from threading import Timer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime

from selenium.common.exceptions import TimeoutException
import smtplib
import email
import ConfigParser


reload(sys)  
sys.setdefaultencoding('utf8')

LIMIT_TIME = 90
GAP = 0
DELAY = 1

Gmail_User = ""
Gmail_Pwd = ""
ToEmail1 = "" 
ToEmail2 = "" 

RT_NONE = 0
RT_SUCCESS = 1
RT_SUSPEND = 2
RT_EXISTHALT = 3
 
def SendEmailWithGmail(TEXT):

    print "Sending Ready --------------------- "
    SUBJECT = "Report match"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(Gmail_User, Gmail_Pwd)
    BODY = '\r\n'.join(['To: %s' % ToEmail1,
        'From: %s' % Gmail_User,
        'Subject: %s' % SUBJECT,
        '', TEXT])

    server.sendmail(Gmail_User, [ToEmail1], BODY)

    BODY = '\r\n'.join(['To: %s' % ToEmail2,
        'From: %s' % Gmail_User,
        'Subject: %s' % SUBJECT,
        '', TEXT])

    server.sendmail(Gmail_User, [ToEmail2], BODY)

    print "----    Successfully Sent Email    ---------"


def checkhalf(INDEX):
    result = RT_NONE

    try:

        games = driver.find_elements_by_xpath("//div[@class='ipo-Fixture_ScoreDisplay ipo-ScoreDisplayStandard ']")
        games[INDEX].click()

        nCount = 0
        bLoop = True
        while bLoop:
            time.sleep(1)
        
            nCount += 1
            if nCount == 5:
                bLoop = False

            src = driver.page_source
            soup = BeautifulSoup(src,"lxml")
            MarketGroups = soup.find_all("div", class_="gl-MarketGroup ")
            if len(MarketGroups) == 0:
                continue

            if soup.find("span", class_="gl-MarketGroupButton_CurrentlySuspended"):
                result = RT_SUSPEND
                break;

            for MarketGroup in MarketGroups:
                ButtonText = MarketGroup.find("span", class_="gl-MarketGroupButton_Text")
                if ButtonText.text == "Half Time Result":
                    result = RT_EXISTHALT
#                    print "                 ---------- exist half time " 
                    bLoop = False
                    break

                if ButtonText.text == "Match Goals":
                    bLoop = False
#                    print "                 ---------- send "
                    result = RT_SUCCESS
                    break
    
    except:
        print(" ")

    while True:
        driver.find_element_by_xpath("//div[@class='ip-ControlBar_BBarItem ']").click()
        time.sleep(1)

        src = driver.page_source
        soup = BeautifulSoup(src,"lxml")

        title = soup.find("div", class_="ip-ControlBar ")
        sel_button = title.find("div", class_="ip-ControlBar_BBarItem wl-ButtonBar_Selected ")

        if sel_button.text == "Overview":
            break

    return result

#gl-MarketGroup 
#    gl-MarketGroupButton gl-MarketGroup_HasFavouriteButton gl-MarketGroup_Open 


def crawl ():

    SoccorDict = {}
    SentList = {}

    driver.get("https://www.bet365.com/en/")
    driver.add_cookie({'name':'aps03', 'value':'oty=1&cg=0&cst=119&tzi=27&hd=N&lng=1&cf=N&ct=42'})
    driver.add_cookie({'name':'rmbs', 'value':'3'})
    driver.get("https://www.bet365.com/#/IP/")

    driver1.get("https://www.bet365.com/en/")
    driver1.add_cookie({'name':'aps03', 'value':'oty=1&cg=0&cst=119&tzi=27&hd=N&lng=1&cf=N&ct=42'})
    driver1.add_cookie({'name':'rmbs', 'value':'3'})
    driver1.get("https://www.bet365.com/#/IP/")

    while True:
        src = driver.page_source 
        soup = BeautifulSoup(src,"lxml") 

        ToolBar_Labels = soup.find_all("div", class_="ipo-ClassificationBarButtonBase_Label ")
        if ToolBar_Labels:
            break
           
        time.sleep(1)

    while True:
        src = driver1.page_source 
        soup = BeautifulSoup(src,"lxml") 

        ToolBar_Labels = soup.find_all("div", class_="ipo-ClassificationBarButtonBase_Label ")
        if ToolBar_Labels:
            break
           
        time.sleep(1)

    while True:
        
        try:
            src = driver.page_source
            soup = BeautifulSoup(src,"lxml")

            SoccerTitle = soup.find("div", class_="ipo-ClassificationHeader_HeaderLabel ")
            if SoccerTitle.text != "Soccer":
                ToolBar_Labels = soup.find_all("div", class_="ipo-ClassificationBarButtonBase_Label ")
                if ToolBar_Labels[1].text == "Soccer":
                    ToolBarItems = driver.find_elements_by_xpath("//div[@class='ipo-ClassificationBarButtonBase_Label ']")
                    ToolBarItems[1].click()
                    time.sleep(1.2)
                else:
                    time.sleep(30)
                continue

            Menu = soup.find("div", class_="ip-DropDownContainer_Button ipo-InPlayClassificationMarketSelectorDropDown_Button ipo-InPlayClassificationMarketSelectorDropDown_Button-1 ")
            if Menu.text == "Main Markets":
                driver.find_element_by_xpath("//div[@class='ip-DropDownContainer_Button ipo-InPlayClassificationMarketSelectorDropDown_Button ipo-InPlayClassificationMarketSelectorDropDown_Button-1 ']").click()
                time.sleep(1.2)

                DropDownItems = driver.find_elements_by_xpath("//div[@class='ipo-InPlayClassificationMarketSelectorDropDown_DropDownItem ipo-MarketSelectorDropDownItem wl-DropDownItem ']")
                DropDownItems[1].click()           
                time.sleep(3)
                continue

            Menu = soup.find_all("span", class_="hm-DropDownSelections_Highlight ")
            if Menu[1].text == "Fractional":
                driver.find_element_by_xpath("//div[@class='hm-OddsDropDownSelections hm-DropDownSelections ']").click()
                time.sleep(1.2)

                DropDownItems = driver.find_element_by_xpath("//a[@class='hm-DropDownSelections_Item ']").click() 
                time.sleep(1)
                continue

            src = driver1.page_source
            soup1 = BeautifulSoup(src,"lxml")

            SoccerTitle = soup1.find("div", class_="ipo-ClassificationHeader_HeaderLabel ")
            if SoccerTitle.text != "Soccer":
                ToolBar_Labels = soup1.find_all("div", class_="ipo-ClassificationBarButtonBase_Label ")
                if ToolBar_Labels[1].text == "Soccer":
                    ToolBarItems = driver1.find_elements_by_xpath("//div[@class='ipo-ClassificationBarButtonBase_Label ']")
                    ToolBarItems[1].click()
                    time.sleep(1.2)
                else:
                    time.sleep(30)
                continue

            Menu = soup1.find_all("span", class_="hm-DropDownSelections_Highlight ")
            if Menu[1].text == "Fractional":
                driver1.find_element_by_xpath("//div[@class='hm-OddsDropDownSelections hm-DropDownSelections ']").click()
                time.sleep(1.2)

                DropDownItems = driver1.find_element_by_xpath("//a[@class='hm-DropDownSelections_Item ']").click() 
                time.sleep(1)
                continue

       
            NewDict = {}

            Leagues = soup.find_all("div", class_="ipo-Competition ipo-Competition-open ")
            Matches = soup.find_all("div", class_="ipo-Fixture_TableRow ")
            print "\nCount:", len(Matches)

            Matches1 = soup1.find_all("div", class_="ipo-Fixture_TableRow ")

            n = -1

            for League in Leagues: 
                
                try:

                    Matches = League.find_all("div", class_="ipo-Fixture_TableRow ")

                    for Match in Matches:

                        n += 1

                        SoccerTime = Match.find("div", class_="ipo-InPlayTimer ")
                        TeamWrapper = Match.find_all("span", class_="ipo-TeamStack_TeamWrapper")
                    
                        if SoccerTime.text[3] == ":":
                            SoccerTime_Min = int(SoccerTime.text[:3])
                            SoccerTime_Sec = int(SoccerTime.text[4:6])
                        else:
                            SoccerTime_Min = int(SoccerTime.text[:2])
                            SoccerTime_Sec = int(SoccerTime.text[3:5])
                        SoccerTime_Sum = SoccerTime_Min * 60 + SoccerTime_Sec

                        if SoccerTime.text[3] == ":":
                            print "time", SoccerTime_Sum, " limit ----------", SoccerTime.text, TeamWrapper[0].text
                            continue
                    
                        if SoccerTime_Min < LIMIT_TIME:
                            Team_Point1 = Match.find("div", class_="ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamone ")
                            Team_Point2 = Match.find("div", class_="ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamtwo ")

                            if Team_Point1.text != '0' or Team_Point2.text != '0':
                                 print "score(", Team_Point1.text, ':', Team_Point2.text, ") ------------", SoccerTime.text, TeamWrapper[0].text
                                 continue

                            '''
                            BlankLen = len(Match.find_all("div", class_="ipo-MainMarketRenderer_BlankParticipant "))
                            if BlankLen != 9:
                                BlankLen += len(Match.find_all("div", class_="gl-ParticipantCentered ipo-AllMarketsParticipant gl-ParticipantCentered_BlankName gl-ParticipantCentered_Suspended "))
                                BlankLen += len(Match.find_all("div", class_="gl-ParticipantCentered gl-ParticipantCentered_NoHandicap ipo-AllMarketsParticipant gl-ParticipantCentered_BlankName gl-ParticipantCentered_Suspended "))
                                if BlankLen != 9:
                                    print "blank (", BlankLen , ") limit ----------", SoccerTime.text, TeamWrapper[0].text
                                    continue
                            '''

                            MainMarketRenderer = Match.find("div", class_="ipo-MainMarketRenderer ").find_all('div')
                            ht0 = MainMarketRenderer[0].find("span", class_="gl-ParticipantCentered_Odds")
                            if ht0:
                                ht0_value = float(ht0.text)
                            else:
                                ht0_value = 0
                            ht1 = MainMarketRenderer[1].find("span", class_="gl-ParticipantCentered_Odds")
                            if ht1:
                                ht1_value = float(ht1.text)
                            else:
                                ht1_value = 0

                            MainMarketRenderer = Matches1[n].find("div", class_="ipo-MainMarketRenderer ").find_all('div')
                            ft0 = MainMarketRenderer[0].find("span", class_="gl-ParticipantCentered_Odds")
                            if ft0:
                                ft0_value = float(ft0.text)
                            else:
                                ft0_value = 0
                            ft1 = MainMarketRenderer[1].find("span", class_="gl-ParticipantCentered_Odds")
                            if ft1:
                                ft1_value = float(ft1.text)
                            else:
                                ft1_value = 0

                            diff0 = ft0_value - ht0_value
                            diff1 = ft1_value - ht1_value
                            if diff0 < 0 and diff1 < 0:
                                print "diffs (", diff0, "," , diff1, ") ------", SoccerTime.text, TeamWrapper[0].text
                                continue


                            if SoccorDict.get(TeamWrapper[0].text) != None:
                                ret = RT_NONE
                                if SoccerTime_Sum - SoccorDict[TeamWrapper[0].text] > GAP:
                                    if SentList.get(TeamWrapper[0].text) != None:
                                        continue

                                    ret = checkhalf(n)

                                    if ret == RT_SUCCESS:
                                        LeagueName = League.find("div", class_="ipo-CompetitionButton_NameLabel ipo-CompetitionButton_NameLabelHasMarketHeading ")
                                        Team1 = TeamWrapper[0].text + " : " +Match.find("div", class_="ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamone ").text
                                        Team2 = TeamWrapper[1].text + " : " +Match.find("div", class_="ipo-TeamPoints_TeamScore ipo-TeamPoints_TeamScore-teamtwo ").text

                                        message = '\r\n'.join(['%s\r\n' % LeagueName.text,
                                                               '%s  %s' % (SoccerTime.text, Team1),
                                                               '       %s' % Team2])

                                        SendEmailWithGmail(message)
                                        SentList[TeamWrapper[0].text] = TeamWrapper[1].text
                                        continue

                                print "Check Old Soccer ----------", SoccerTime.text, TeamWrapper[0].text, SoccerTime_Sum, SoccorDict[TeamWrapper[0].text], SoccerTime_Sum - SoccorDict[TeamWrapper[0].text]                     
                                
                                if ret == RT_SUSPEND:
                                    print "                 ---------- suspended "
                                    continue
                                elif ret == RT_EXISTHALT:
                                    print "                 ---------- exist half time "
                                    continue

                                NewDict[TeamWrapper[0].text] = SoccorDict[TeamWrapper[0].text]
                                continue

                            print "Start New Soccer ----------", SoccerTime.text, TeamWrapper[0].text, SoccerTime_Sum
                            NewDict[TeamWrapper[0].text] = SoccerTime_Sum 
                          
                        else:
                            print "time", SoccerTime_Sum, " limit ----------", SoccerTime.text, TeamWrapper[0].text
                except:
                    print("Unexpected error:", sys.exc_info()[0])

            SoccorDict = NewDict.copy()
            time.sleep(DELAY)
        except:
            print("Re Loading.....")
#            raise
    return

def init():
    global LIMIT_TIME
    global GAP
    global Gmail_User
    global Gmail_Pwd
    global ToEmail1
    global ToEmail2

    config = ConfigParser.ConfigParser()
    config.read('Setting.ini')

    LIMIT_TIME = int(config.get('Setting', 'Limit', 30))
    GAP = int(config.get('Setting', 'Gap', 2))

    Gmail_User = config.get('Email', 'From_Email', "")
    Gmail_Pwd = config.get('Email', 'From_EmailPwd', "")
    ToEmail1 = config.get('Email', 'ToEmail1', "")
    ToEmail2 = config.get('Email', 'ToEmail2', "")

if __name__ == '__main__':
    init()
    print "Loading....."
    driver = webdriver.Firefox()
    driver1 = webdriver.Firefox()
    crawl()
    driver.quit()
    driver1.quit()
    