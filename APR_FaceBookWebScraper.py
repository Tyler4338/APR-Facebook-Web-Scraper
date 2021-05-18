import requests
import os.path
import pyodbc 
import time
import urllib3
from tkinter import *
import tkinter.font as tkfont
from PIL import ImageTk, Image
from tkinter import messagebox
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
#=====================================================================UTIL FUNCTIONS=================================================================#
def safe_is_element_xpath_available(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True 
    except NoSuchElementException:
        return False

def safe_find_elements_by_xpath(driver, xpath):
    try:
        return driver.find_elements_by_xpath(xpath)
    except NoSuchElementException:
        return None
def safe_find_element_by_xpath(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return None

def safe_countChildNodes(driver, xpath):
    try:
        x = safe_find_element_by_xpath(driver,xpath).get_attribute('childElementCount')
        return int(x)
    except Exception as e:
        print(e)
        return 1

def safe_FB_loginSequence(driver,FBemail,FBpass,implicityWaitTime=10):
    try:
        UN = FBemail
        PASS = FBpass
        masterLinkFacebookLogin = "https://mbasic.facebook.com/login"
        driver.get(masterLinkFacebookLogin)
        driver.implicitly_wait(implicityWaitTime) # Driver will wait 10 seconds when a specific element within the DOM is not readily visable
        #Xpath Elements associated with the login screen 
        #login element username
        username = safe_find_element_by_xpath(driver,"//*[@name = 'email']")
        #login element password
        password = safe_find_element_by_xpath(driver,"//*[@name = 'pass']")
        #login element login
        login = safe_find_element_by_xpath(driver,"//*[@name = 'login']")

        username.clear()
        password.clear()
        username.send_keys(UN)
        password.send_keys(PASS) 
        login.submit()
    except Exception as e:
        print(e)
#===================================================================SEARCHERS==============================================================#
def safe_Find_Places_Lived(driver,placesLivedTuple, placesLivedTupleTitle, waitTimes=5):
    try:
        if(safe_is_element_xpath_available(driver,"//*[text()='Places Lived']")): # checks to see if the catagory is visable to be scraped 
            depConst = safe_countChildNodes(driver, "//*[@id='living']/div/div") # retruns the number of subcatagories which exist in the visable places lived catagory
            for i in range(1,(depConst+1)):
                time.sleep(waitTimes)

                #Finds the address associated with the place being refered to, ie "Maryland", usually stored in a tags
                XpAtH_FS_placesLived= "//*[@id='living']/div/div/div["+ str(i) +"]/div/table/tbody/tr/td[2]/div/a" 

                #Finds the address associated with the title of the place being refered to, ie x place is the "hometown"
                XpAtH_FS_placesLived_Title= "//*[@id='living']/div/div/div["+ str(i) +"]/div/table/tbody/tr/td[1]/div/span"

                #the variable below is not needed but it makes the program easier to follow
                textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_placesLived).text
                time.sleep(waitTimes)
                placesLivedTuple.append(textualAttriubteConversion)
                #The place that is scraped is added to the places lived list of strings
                textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_placesLived_Title).text
                time.sleep(waitTimes)
                placesLivedTupleTitle.append(textualAttriubteConversion)
        else:
            pass #Nothing
    except Exception as e:
        print(e)

def safe_Find_Basic_Info(driver,basicTuple, basicTupleTitle, waitTimes=5):
    try:
        if(safe_is_element_xpath_available(driver,"//*[text()='Basic Info']")): # checks to see if the catagory is visable to be scraped 
            depConst = safe_countChildNodes(driver, "//*[@id='basic-info']/div/div") # retruns the number of subcatagories which exist in the visable places lived catagory
            for i in range(1,(depConst+1)):
                time.sleep(waitTimes)

                #Finds the address associated with the place being refered to, ie "Maryland", usually stored in a tags
                XpAtH_FS_BasicInfo= "//*[@id='basic-info']/div/div/div["+ str(i) +"]/table/tbody/tr/td[2]/div" 

                #Finds the address associated with the title of the place being refered to, ie x place is the "hometown"
                XpAtH_FS_BasicInfo_Title= "//*[@id='basic-info']/div/div/div["+ str(i) +"]/table/tbody/tr/td[1]/div/span"

                #the variable below is not needed but it makes the program easier to follow
                textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_BasicInfo).text
                time.sleep(waitTimes)
                basicTuple.append(textualAttriubteConversion)
                #The place that is scraped is added to the basic info list of strings
                textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_BasicInfo_Title).text
                time.sleep(waitTimes)
                basicTupleTitle.append(textualAttriubteConversion)
        else:
            pass #Nothing
    except Exception as e:
        print(e)

def safe_Find_Contact_Info(driver,contactTuple, contactTupleTitle, waitTimes=5):
    try:
        print(safe_is_element_xpath_available(driver,"//*[text()='Contact Info']"))
        if(safe_is_element_xpath_available(driver,"//*[text()='Contact Info']")): # checks to see if the catagory is visable to be scraped 
            depConst = safe_countChildNodes(driver, "//*[@id='contact-info']/div/div") # retruns the number of subcatagories which exist in the visable places lived catagory
            for i in range(1,(depConst+1)):
                time.sleep(waitTimes)

                #Finds the address associated with the contact info
                XpAtH_FS_BasicInfo= "//*[@id='contact-info']/div/div/div["+ str(i) +"]/table/tbody/tr/td[2]/div" 

                #Finds the address associated with the title of the place being refered to, ie x place is the "hometown"
                XpAtH_FS_BasicInfo_Title= "//*[@id='contact-info']/div/div/div["+ str(i) +"]/table/tbody/tr/td[1]/div/span"

                #the variable below is not needed but it makes the program easier to follow
                textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_BasicInfo).text
                time.sleep(waitTimes)
                contactTuple.append(textualAttriubteConversion)
                #The place that is scraped is added to the contact info list of strings
                textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_BasicInfo_Title).text
                time.sleep(waitTimes)
                contactTupleTitle.append(textualAttriubteConversion)
        else:
            print("not found")
    except Exception as e:
        print(e)

#===================================================================SPECIAL SEARCHERS==============================================================#
def safe_Find_Full_Name(driver,waitTime=5):
    try:
        textualAttriubteConversion = "n/a"
        if(safe_is_element_xpath_available(driver,"//*[@id='root']")):
            Xpath_NameFull = "//*[@id='root']/div/div/div[2]/div/span/div/span/strong"
            textualAttriubteConversion = safe_find_element_by_xpath(driver, Xpath_NameFull).text
            time.sleep(waitTime)
        return textualAttriubteConversion
    except Exception as e:
        print(e)
def safe_Find_FamilyMembers(driver,familyTuple,familyRelationTuple, waitTimes=5):
    try:
        if(safe_is_element_xpath_available(driver,"//*[text()='Family Members']")): # checks to see if the catagory is visable to be scraped 
            depConst = safe_countChildNodes(driver, "//*[@id='family']/div/div")
            for i in range(1,(depConst+1)):
                time.sleep(waitTimes)
                
                XpAtH_FS_FamilyH3 = "//*[@id='family']/div/div/div["+ str(i) +"]/header/h3[1]"
                XpAtH_FS_FamilyA = "//*[@id='family']/div/div/div["+ str(i) +"]/header/h3[1]/a"
                XpAtH_FS_Relation = "//*[@id='family']/div/div/div["+ str(i) +"]/header/h3[2]"

                
                #Checks the elements present at the previously defined Xpaths, the place of work can 
                #either be stored in a tags or span tags, so the if statemnets are meant to detect this

                if(safe_is_element_xpath_available(driver, XpAtH_FS_FamilyA)):
                    textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_FamilyA).text
                    time.sleep(waitTimes)
                else:
                    textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_FamilyH3).text
                familyTuple.append(textualAttriubteConversion)
                if(safe_is_element_xpath_available(driver, XpAtH_FS_Relation)):       
                    textualAttriubteConversion  =  safe_find_element_by_xpath(driver, XpAtH_FS_Relation).text
                    familyRelationTuple.append(textualAttriubteConversion)
                    time.sleep(waitTimes)
                elif((safe_is_element_xpath_available(driver, XpAtH_FS_FamilyA) or safe_is_element_xpath_available(driver, XpAtH_FS_FamilyH3))
                      and not safe_is_element_xpath_available(driver, XpAtH_FS_Relation)):
                    familyRelationTuple.append("n/a")
        else:
            print("not found")
    except Exception as e:
        print(e)

def safe_Find_Work(driver,workTuple,occupationTuple,timeFrameTuple, waitTimes=5):
    try:
        if(safe_is_element_xpath_available(driver,"//*[text()='Work']")): # checks to see if the catagory is visable to be scraped 
            depConst = safe_countChildNodes(driver, "//*[@id='work']/div/div")
            for i in range(1,(depConst+1)):
                time.sleep(waitTimes)
                
                XpAtH_FS_WorkSpan = "//*[@id='work']/div/div/div["+ str(i) +"]/div/div/div[1]/span"
                XpAtH_FS_WorkA = "//*[@id='work']/div/div/div["+ str(i) +"]/div/div/div[1]/span/a"
                XpAtH_FS_WorkProfession = "//*[@id='work']/div/div/div["+ str(i) +"]/div/div/div[2]/span"
                XpAtH_FS_WorkTimeFrame = "//*[@id='work']/div/div/div["+ str(i) +"]/div/div/div[3]/span"

                
                #Checks the elements present at the previously defined Xpaths, the place of work can 
                #either be stored in a tags or span tags, so the if statemnets are meant to detect this

                if(safe_is_element_xpath_available(driver, XpAtH_FS_WorkA)):
                    textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_WorkA).text
                    time.sleep(waitTimes)
                else:
                    textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_WorkSpan).text
                workTuple.append(textualAttriubteConversion)
                if(safe_is_element_xpath_available(driver, XpAtH_FS_WorkProfession)):       
                    textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_WorkProfession).text
                    occupationTuple.append(textualAttriubteConversion)
                    time.sleep(waitTimes)
                    if(safe_is_element_xpath_available(driver, XpAtH_FS_WorkTimeFrame)):       
                        textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_WorkTimeFrame).text
                        timeFrameTuple.append(textualAttriubteConversion)
                        time.sleep(waitTimes)
                    else:
                        timeFrameTuple.append("n/a")
                elif((safe_is_element_xpath_available(driver, XpAtH_FS_WorkA) or safe_is_element_xpath_available(driver, XpAtH_FS_WorkSpan))
                      and not safe_is_element_xpath_available(driver, XpAtH_FS_WorkProfession)):
                    timeFrameTuple.append("n/a")
                    occupationTuple.append("n/a")

        else:
            print("not found")
    except Exception as e:
        print(e)

def safe_Find_Education(driver,educationTuple,educationTypeTuple,educationTimeFrame, waitTimes=5):
    try:
        if(safe_is_element_xpath_available(driver,"//*[text()='Education']")): # checks to see if the catagory is visable to be scraped 
            depConst = safe_countChildNodes(driver, "//*[@id='education']/div/div")
            for i in range(1,(depConst+1)):
                time.sleep(waitTimes)
                
                XpAtH_FS_EducationSpan = "//*[@id='education']/div/div/div["+ str(i) +"]/div/div/div[1]/div/span"
                XpAtH_FS_EducationA = "//*[@id='education']/div/div/div["+ str(i) +"]/div/div/div[1]/div/span/a"
                XpAtH_FS_EducationType = "//*[@id='education']/div/div/div["+ str(i) +"]/div/div/div[2]/span"
                XpAtH_FS_EducationClass = "//*[@id='education']/div/div/div["+ str(i) +"]/div/div/div[3]/span"

                
                #Checks the elements present at the previously defined Xpaths, the place of work can 
                #either be stored in a tags or span tags, so the if statemnets are meant to detect this
                #print(safe_is_element_xpath_available(driver, XpAtH_FS_EducationA))
                #print(safe_is_element_xpath_available(driver, XpAtH_FS_EducationSpan))

                if(safe_is_element_xpath_available(driver, XpAtH_FS_EducationA)):
                    textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_EducationA).text
                    time.sleep(waitTimes)
                else:
                    textualAttriubteConversion = safe_find_element_by_xpath(driver, XpAtH_FS_EducationSpan).text
                educationTuple.append(textualAttriubteConversion)

                if(safe_is_element_xpath_available(driver, XpAtH_FS_EducationType)):       
                    textualAttriubteConversion  =  safe_find_element_by_xpath(driver, XpAtH_FS_EducationType).text
                    educationTypeTuple.append(textualAttriubteConversion)
                    time.sleep(waitTimes)
                    if(safe_is_element_xpath_available(driver, XpAtH_FS_EducationClass)):       
                        textualAttriubteConversion  =  safe_find_element_by_xpath(driver, XpAtH_FS_EducationClass).text
                        educationTimeFrame.append(textualAttriubteConversion)
                        time.sleep(waitTimes)
                    else:
                        educationTimeFrame.append("n/a")

                elif( (safe_is_element_xpath_available(driver, XpAtH_FS_EducationA) or safe_is_element_xpath_available(driver, XpAtH_FS_EducationSpan))
                       and not safe_is_element_xpath_available(driver, XpAtH_FS_EducationType)):
                    educationTypeTuple.append("n/a")
                    educationTimeFrame.append("n/a")
        else:
            print("not found")
    except Exception as e:
        print(e)

#=================================================================== SQL Export ==============================================================

def SqlDatabaseExport(serverName,username,chosenDatabase, scrapedInformation, name):
    userID = 0
    try:
        #=======================================
        conn = pyodbc.connect('Driver={SQL Server};Server='+serverName+';Database='+chosenDatabase+';UID='+username+';Trusted_Connection=yes;')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as CountED FROM dbo.ScrapedMainDT')
        for row in cursor:
            thing = str(row)
            thing = thing.strip('(), ')
        userID = str((int(thing) + 1))
        #SqlDatabaseInitalization(conn,cursor)
        # NEVER RUN THIS AFTER YOU HAVE GATHERED OR 
        # ARE GATHERING USER PROFILES AS IT WILL WIPE 
        # YOUR TABLES CLEAN
        #=======================================
        print(scrapedInformation[0])
        print(scrapedInformation[1])
        print(scrapedInformation[2])
        print(scrapedInformation[3])
        print(scrapedInformation[4])
        print(scrapedInformation[5])
        print(scrapedInformation[6])
        print(scrapedInformation[7])
        print(scrapedInformation[8])
        print(scrapedInformation[9])
        print(scrapedInformation[10])
        print(scrapedInformation[11])
        print(scrapedInformation[12])
        print(scrapedInformation[13])
        

        print("Main record start")
        SqlMainRecordExport(conn, cursor, userID, name)
        print("Places Lived start")
        SqlPlacesLivedExport(conn, cursor, userID, scrapedInformation[0], scrapedInformation[1])
        print("contact info start")
        SqlContactInfoExport(conn, cursor, userID, scrapedInformation[2], scrapedInformation[3])
        print("basic info start")
        SqlBasicInfoExport(conn, cursor, userID, scrapedInformation[4], scrapedInformation[5])
        print("work info start")
        SqlWorkInfoExport(conn, cursor, userID, scrapedInformation[6], scrapedInformation[7],scrapedInformation[8])
        print("family info start")
        SqlFamilyExport(conn, cursor, userID, scrapedInformation[9], scrapedInformation[10])
        print("education info")
        SqlEducationInfoExport(conn, cursor, userID, scrapedInformation[11], scrapedInformation[12],scrapedInformation[13])
    except(Exception) as e:
        print(e)
def SqlDatabaseInitalization(conn, cursor):
    try:
        cursor.execute('''
        
        IF OBJECT_ID('dbo.ScrapedMainDT', 'U') IS NOT NULL
        DROP TABLE dbo.ScrapedMainDT
        -- Create the table in the specified schema
        CREATE TABLE dbo.ScrapedMainDT(
        UserId int NOT NULL, 
        Name  varchar(255) NOT NULL,
        Date  varchar(255) default getutcdate(),
        RetrievalTime varchar(255) default sysdatetime()
        );

        IF OBJECT_ID('dbo.PlacesLived', 'U') IS NOT NULL
        DROP TABLE dbo.PlacesLived
        CREATE TABLE dbo.PlacesLived(
        UserId int NOT NULL,
        Place varchar(255) default NULL,
        Hometown  varchar(255) default NULL,
        CurrentCity  varchar(255) default NULL,
        Other varchar(255) default NULL
        );

        IF OBJECT_ID('dbo.BasicInfo', 'U') IS NOT NULL
        DROP TABLE dbo.BasicInfo
        CREATE TABLE dbo.BasicInfo(
        UserId int NOT NULL,
        Gender varchar(255) default NULL,
        InterestedIn  varchar(255) default NULL,
        Languages  varchar(255) default NULL,
        Other varchar(255) default NULL
        );

        IF OBJECT_ID('dbo.ContactInfo', 'U') IS NOT NULL
        DROP TABLE dbo.ContactInfo
        CREATE TABLE dbo.ContactInfo(
        UserId int NOT NULL,
        Facebook varchar(255) default NULL,
        Email  varchar(255) default NULL,
        Other varchar(255) default NULL
        );

        IF OBJECT_ID('dbo.WorkInfo', 'U') IS NOT NULL
        DROP TABLE dbo.WorkInfo
        CREATE TABLE dbo.WorkInfo(
        UserId int NOT NULL,
        WorkPlace varchar(255) default NULL,
        Occupation  varchar(255) default NULL,
        Timeframe varchar(255) default NULL,
        Other varchar(255) default NULL
        );

        IF OBJECT_ID('dbo.EducationInfo', 'U') IS NOT NULL
        DROP TABLE dbo.EducationInfo
        CREATE TABLE dbo.EducationInfo(
        UserId int NOT NULL,
        School varchar(255) default NULL,
        College  varchar(255) default NULL,
        Highschool  varchar(255) default NULL,
        Timeframe varchar(255) default NULL,
        Other varchar(255) default NULL
        );

        IF OBJECT_ID('dbo.FamilyInfo', 'U') IS NOT NULL
        DROP TABLE dbo.FamilyInfo
        CREATE TABLE dbo.FamilyInfo(
        UserId int NOT NULL,
        PersonName varchar(255) default NULL,
        Relation  varchar(255) default NULL,
        );
        ''')
        conn.commit()
    except(Exception) as e:
        print(e)
def SqlMainRecordExport(conn, cursor, userID, name):
    name = "'" + name + "'"
    cursor.execute('''INSERT INTO ScrapedMainDT ([UserId],[Name])
                      VALUES 
                      (''' + userID + ',' + name + ')')
    conn.commit()

def SqlPlacesLivedExport(conn, cursor, userID, placesLivedTitles, placesLived):

    placeholder = ''
    #For a given value in the list, the loop modifies the sql query that commits to the database
    for count, i in enumerate(placesLivedTitles):
        if i.lower() == 'hometown':
            placeholder = "'" + placesLived[count] + "'"+''','yes','no', NULL'''
        elif i.lower() == 'current city':
            placeholder = "'" + placesLived[count] + "'"+''','no','yes', NULL'''
        else:
            placeholder = "'" + placesLived[count] + "'"+''','no','no',''' + "'"+ i +"'"

        cursor.execute('''INSERT INTO dbo.PlacesLived ([UserId],[Place],[Hometown],[CurrentCity], [Other])
                        VALUES 
                        (''' + userID + ',' + placeholder + ')')
        conn.commit()
        time.sleep(0.2)

def SqlBasicInfoExport(conn, cursor, userID, basic_titles, basic_info):
    placeholderGender =  "'n/a'"
    placeholderLanguages = "'n/a'" 
    placeholderPreference = "'n/a'"
    placeholderOther = []
    #For a given value in the list, the loop modifies the sql query that commits to the database
    if len(basic_titles) > 0 and len(basic_info) > 0:
        for count, i in enumerate(basic_titles):
            if i.lower() == 'gender':
                placeholderGender = "'" + basic_info[count] + "'"
            elif i.lower() == 'interested in':
                placeholderPreference = "'" + basic_info[count] + "'"
            elif i.lower() == 'languages':
                placeholderLanguages = "'" + basic_info[count] + "'"
            else:
                placeholderOther.append("'"+ i + ': ' + basic_info[count] + "'")  
        cursor.execute('''INSERT INTO dbo.BasicInfo ([UserId],[Gender],[InterestedIn],[Languages], [Other])
                        VALUES 
                        (''' + userID + ',' + placeholderGender + ',' + placeholderPreference + ',' + placeholderLanguages + ',NULL)')
        conn.commit()
        if len(placeholderOther) > 0:
            for x in placeholderOther:
                time.sleep(0.2)
                cursor.execute('''INSERT INTO dbo.BasicInfo ([UserId],[Gender],[InterestedIn],[Languages], [Other])
                                    VALUES 
                                    (''' + userID + ',NULL,NULL,NULL,' + x + ')')
                conn.commit()
    
def SqlContactInfoExport(conn, cursor, userID, contact_titles, contact_info):
    placeholderFB = "'n/a'"
    placeholderEMAIL = "'n/a'"
    placeholderOther = []
    #For a given value in the list, the loop modifies the sql query that commits to the database
    if len(contact_titles) > 0 and len(contact_info) > 0:
        for count, i in enumerate(contact_titles):
            if i.lower() == 'facebook':
                placeholderFB = "'" + contact_info[count] + "'"
            elif i.lower() == 'email':
                placeholderEMAIL = "'" + contact_info[count] + "'"
            else:
                placeholderOther.append("'"+ i + ': ' + contact_info[count] + "'")  
        cursor.execute('''INSERT INTO dbo.ContactInfo ([UserId],[Facebook],[Email],[Other])
                        VALUES 
                        (''' + userID + ',' + placeholderFB + ',' + placeholderEMAIL + ',NULL)')
        conn.commit()
        if len(placeholderOther) > 0:
            for x in placeholderOther:
                time.sleep(0.2)
                cursor.execute('''INSERT INTO dbo.ContactInfo ([UserId],[Facebook],[Email],[Other])
                                    VALUES 
                                    (''' + userID + ',NULL,NULL,' + x + ')')
                conn.commit()

def SqlWorkInfoExport(conn, cursor, userID, work_info,occupationTuple,timeFrameTuple):
    placeholderTimeFrame = "'n/a'"
    placeholderOccupation = "'n/a'"
    #For a given value in the list, the loop modifies the sql query that commits to the database
    for count, i in enumerate(work_info):
        placeholderPlaceOfWork = "'" + work_info[count] + "'"
        placeholderOccupation = "'" + occupationTuple[count] + "'"
        placeholderTimeFrame = "'" +timeFrameTuple[count] + "'"
    
        cursor.execute('''INSERT INTO dbo.WorkINFO ([UserId],[WorkPlace],[Occupation],[Timeframe], [Other])
                        VALUES 
                        (''' + userID + ',' + placeholderPlaceOfWork + ',' + placeholderOccupation + ',' + placeholderTimeFrame + ',NULL)')
        conn.commit()
        placeholderTimeFrame = "'n/a'"
        placeholderOccupation = "'n/a'"
        time.sleep(0.2)

def SqlEducationInfoExport(conn, cursor, userID, education_info,education_titles,educationTimeFrame): #TO BE EDITED TO ACCOUNT FOR EXTRA VAR
    placeholder = ''
    #For a given value in the list, the loop modifies the sql query that commits to the database
    if len(education_titles) > 0 and len(education_info) > 0:
        for count, i in enumerate(education_titles):
            if (i.lower() == 'college' or i.lower() == 'graduate school') or ("college" in (education_info[count]).lower()) or ("university" in (education_info[count]).lower()) :
                placeholder = "'" + education_info[count] + "'"+ ",'yes','no'," + "'" + educationTimeFrame[count] + "'" + ''' ,'n/a' '''
            elif i.lower() == 'high school' or i.lower() == 'highschool':
                placeholder = "'" + education_info[count] + "'" + ",'no','yes'," + "'" + educationTimeFrame[count] + "'" + ''' ,'n/a' '''
            else:
                placeholder = "'" + education_info[count] + "'" + ",'no','no'," + "'" + educationTimeFrame[count] + "'" + "," + "'" + i + "'"
           
            cursor.execute('''INSERT INTO dbo.EducationInfo ([UserId],[School],[College],[Highschool],[Timeframe], [Other])
                            VALUES 
                            (''' + userID + ',' + placeholder + ')')
            conn.commit()
            time.sleep(0.2)
def SqlFamilyExport(conn, cursor, userID, family_names, family_relation):
    placeholder = ''
    #For a given value in the list, the loop modifies the sql query that commits to the database
    if len(family_relation) > 0 and len(family_names) > 0:
        for count, i in enumerate(family_names):
            try:
                placeholder = "'" + family_names[count] + "'" + ',' + "'" + family_relation[count] + "'"
            except Exception:
                placeholder = "'" + family_names[count] + "'" + ',' + "'n/a'"
            cursor.execute('''INSERT INTO dbo.FamilyInfo ([UserId],[PersonName],[Relation])
                            VALUES 
                            (''' + userID + ',' + placeholder + ')')
            conn.commit()
            time.sleep(0.2)

#=================================================================== GUI ==============================================================#

class FB_retriver_GUI():
    SqlServerNamelabel = None
    SqlServerName = None
    SqlDatbaseLabel= None
    SqlDatbaseName = None
    inputBOX_ForUrl = None
    SQLusernameLabel = None
    SQLusername = None
    FBusernameLabel = None
    FBusername = None
    FBpassLabel = None
    FBpass = None
    def __init__(self):
        try:
            root = Tk()
            root.title("Facebook Demographic Prototype Scraper V1.0")
            self.ny = BooleanVar()
            self.ny.set(False)
            frame_all = LabelFrame(root)
            #initalize the widgets
            itfont = tkfont.Font(family="Comic Sans MS", size = 10,slant=tkfont.ITALIC)
            itlefont = tkfont.Font(family="Comic Sans MS", size = 10)
            title_label = LabelFrame(frame_all, text="Place the Url for the Facebook Profile you Want to Scrape Here", font=itlefont,padx= 20, pady =10)
            self.inputBOX_ForUrl = Entry(title_label, width=78, borderwidth= 5)

            self.FBusernameLabel = LabelFrame(frame_all, text="What is your FB username/email?", font=itlefont,padx= 20, pady =10)
            self.FBusername = Entry(self.FBusernameLabel, width=78, borderwidth= 5)

            self.FBpassLabel = LabelFrame(frame_all, text="What is your FB password?", font=itlefont,padx= 20, pady =10)
            self.FBpass = Entry(self.FBpassLabel, width=78, borderwidth= 5)
             
            #Sql Export
            sub_frame = LabelFrame(frame_all)

            self.SqlServerNamelabel = Label(sub_frame, text = "What is your SQL server name?", font=itlefont)
            self.SqlServerName = Entry(sub_frame, width=80, borderwidth= 5)

            self.SqlDatbaseLabel = Label(sub_frame, text= "What is your chosen database for exporting the scraped information into?", font=itlefont)
            self.SqlDatbaseName = Entry(sub_frame,width=80, borderwidth= 5)

            self.SQLusernameLabel = Label(sub_frame, text="What is your username associated with your server?" + "\n" + "(note: password isn't taken as it is assumed that you are an authenticated user)", font=itlefont)
            self.SQLusername = Entry(sub_frame,width=80, borderwidth= 5)

            #Stort
            start_button = Button(root,text = "Press to Start", command=self.startSequence, font=itlefont) 
            #filepath + Icon
            dir_path = os.path.dirname(os.path.realpath(__file__))
            root.iconbitmap(dir_path+"\\YOIT2.ico")
            #Images + funny label ting
            IMG_frame = LabelFrame(root) 
            canvas = Canvas(IMG_frame, width= 400, height =126)
            #Label
            message_caption = Label(root, text= "\"The mitochondria is the powerhouse of the cell.\"", font=itfont)
            innovationimg = ImageTk.PhotoImage(Image.open(dir_path + "\\innovation.jpg"))
            #Pack the widgets 
            IMG_frame.pack(padx=10, pady=10)
            canvas.pack(pady=5,padx=5, anchor=CENTER)
            canvas.create_image(200,-130,anchor=CENTER, image=innovationimg)
            message_caption.pack()

            frame_all.pack(padx=10, pady=10)
            title_label.pack(padx=10, pady=10)
            self.inputBOX_ForUrl.pack()
            
            self.FBusernameLabel.pack(padx=10, pady=10)
            self.FBusername.pack()
            
            self.FBpassLabel.pack(padx=10, pady=10)
            self.FBpass.pack()
            
            sub_frame.pack(padx=10, pady=10)
            self.SqlServerNamelabel.pack(padx=10, pady=10)
            self.SqlServerName.pack()

            self.SQLusernameLabel.pack(padx=10, pady=10)
            self.SQLusername.pack()

            self.SqlDatbaseLabel.pack(padx=10, pady=10)
            self.SqlDatbaseName.pack()
            
            start_button.pack(pady=10)

            #mainloop
            root.mainloop() 
        except Exception as e:
            messagebox.showerror(title="Something Went Wrong, you should fix it! ",message= e)
            #print("Something Went Wrong, you should fix it! ",e)
    
    def startSequence(self):
        b = self.inputBOX_ForUrl.get()
        r = self.FBusername.get() 
        u = self.FBpass.get()
        h = self.SqlServerName.get()
        e = self.SQLusername.get()
        d = self.SqlDatbaseName.get()
        FBScraperProto1 = xPathSearcher_GENERAL(b,r,u,h,e,d)

#=================================================================== Scraper MAIN ==============================================================#

class xPathSearcher_GENERAL():
    #There are a total of 11 catagories which could be revealed on one's about section, 
    # and the # subsections of these catagories vary depending on the indvidual, so I'm  usually using
    # 2 lists for each catagory type to mangage the content (work and education are execptions)
    places_lived = []
    places_lived_titles = []
    contact_info = []
    contact_titles = []
    basic_info = []
    basic_titles = []
    work_info = []
    work_occupation = []
    work_timeframes = []
    family_info = []
    family_relations = []
    education_info = []
    education_type = []
    education_timeframe = []

    
    def __init__(self, desired_account_url,FBemail,FBpass, serverName, SQLusername, chosenDatabase):
        try:
            #chromium initalization, opens browser in a non-borderless mode
            myDriver = webdriver.Chrome()
            safe_FB_loginSequence(myDriver,FBemail,FBpass)
            time.sleep(5)
            myDriver.get(desired_account_url)
            time.sleep(5)
            self.listReset() #in case the user has run the program more than once in a single instance
            #requests the desired url
            name = safe_Find_Full_Name(myDriver,2)
            print("places scrape start")
            safe_Find_Places_Lived(myDriver,self.places_lived, self.places_lived_titles, 2)
            print("basic scrape start")
            safe_Find_Basic_Info(myDriver,self.basic_info,self.basic_titles, 2)
            print("contact scrape start")
            safe_Find_Contact_Info(myDriver,self.contact_info,self.contact_titles, 2)
            print("family scrape start")
            safe_Find_FamilyMembers(myDriver,self.family_info,self.family_relations, 2)
            print("work scrape start")
            safe_Find_Work(myDriver,self.work_info,self.work_occupation,self.work_timeframes, 2)
            print("education scrape start")
            safe_Find_Education(myDriver,self.education_info, self.education_type,self.education_timeframe, 2)
            #places lived related information
            scrapedInformation = [self.places_lived_titles,self.places_lived,self.contact_titles,self.contact_info,
                                  self.basic_titles,self.basic_info,self.work_info,self.work_occupation, self.work_timeframes,
                                  self.family_info, self.family_relations,self.education_info, self.education_type,self.education_timeframe]
            SqlDatabaseExport(serverName,SQLusername,chosenDatabase,scrapedInformation,name)

        except Exception as e:
            print(e)
    def listReset(self):
        self.places_lived = []
        self.places_lived_titles = []
        self.contact_info = []
        self.contact_titles = []
        self.basic_info = []
        self.basic_titles = []
        self.work_info = []
        self.work_occupation = []
        self.work_timeframes = []
        self.family_info = []
        self.family_relations = []
        self.education_info = []
        self.education_type = []
        self.education_timeframe = []
#=================================================================== Execution ==============================================================#
xTestProto1 = FB_retriver_GUI() # this calls the scraper when the start button is pressed
