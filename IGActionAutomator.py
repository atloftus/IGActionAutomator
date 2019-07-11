import time
import sys
import random
import datetime
import os.path
import numpy as np

from explicit import waiter, XPATH, NAME, CSS
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui

class IGActionAutomator :
    #region INITIALIZATION
    def __init__ (self, username, password, actionsString, numberOfActions, actionVariance, sourceType, sourceParams, comments) :
        self.username = str(username)
        self.password = str(password)
        self.actionsString = str(actionsString).lower()
        self.numberOfActions = int(numberOfActions)
        self.actionVariance = int(actionVariance)
        self.sourceType = str(sourceType)
        sourceParamsFull = str(sourceParams)
        self.sourceParams = sourceParamsFull.split('|', 30)
        commentsFull = str(comments)
        self.comments = commentsFull.split('|', 30)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"')
        self.driver = webdriver.Chrome(executable_path="C:\\Users\\AlexanderLoftus\\PycharmProjects\\IGAccountCurator\\venv\\Lib\\chromedriver_win32\\chromedriver.exe", options=chrome_options)
        self.driver.delete_all_cookies()


    errorFile = open(os.path.join(os.path.dirname(__file__) + '/Logs/Error', datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '.txt'), 'a+')
    runFile = open(os.path.join(os.path.dirname(__file__) + '/Logs/Run',
                                  datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '.txt'), 'a+')
    userleadsFile = open(os.path.join(os.path.dirname(__file__) + '/Logs/UserLeads',
                                datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '.txt'), 'a+')
    uploadFolder = os.path.join(os.path.dirname(__file__) + '/Upload')
    #endregion



    #region UTILITY METHODS
    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        time.sleep(random.randint(1,2))
        usernameElement = driver.find_element_by_xpath("//input[@name='username']")
        usernameElement.clear()
        usernameElement.send_keys(self.username)
        time.sleep(random.randint(1,3))
        passwordElement = driver.find_element_by_xpath("//input[@name='password']")
        passwordElement.clear()
        passwordElement.send_keys(self.password)
        time.sleep(random.randint(2,3))
        passwordElement.send_keys(Keys.ENTER)
        time.sleep(random.randint(4,6))
        self.setupLogFiles(self.username)


    def logout(self) :
        self.driver.get('https://www.instagram.com/' + self.username + '/')
        time.sleep(3)
        settingsButton = self.driver.find_element_by_xpath('//*[@id ="react-root"]/section/nav[1]/div/header/div/div[1]/button').click()
        time.sleep(3)
        logOutButton = self.driver.find_element_by_xpath(
            '//*[@ id ="react-root"]/section/nav[1]/div/section/div[3] / div / div[4] / div / div / a').click()
        time.sleep(3)
        logOutPopUpButton = self.driver.find_element_by_xpath(
            '/ html / body / div[3] / div / div / div[2] / button[1]').click()
        time.sleep(3)
        self.driver.close()
        self.closeLogFiles()


    def resolveDataSource(self):
        if (self.sourceType == '1'):
            self.hashtagMethod()
        elif (self.sourceType == '2'):
            self.locationMethod()
        elif (self.sourceType == '3'):
            self.fileMethod()


    def setupLogFiles(self, username) :
        self.errorFile.write('Error Log:\n')
        self.errorFile.write('Date: ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '\n')

        self.runFile.write('Run Log:\n')
        self.runFile.write('Date: ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '\n')

        if (username  == ''):
            self.errorFile.write('User: coppenmor' + '\n\n')
            self.runFile.write('User: coppenmor' + '\n\n')
        else:
            self.errorFile.write('User: ' + username + '\n\n')
            self.runFile.write('User: ' + username + '\n\n')


    def closeLogFiles(self) :
        self.runFile.write('\nCompleted On: ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y"))
        self.errorFile.write('\nCompleted On: ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y"))
        self.errorFile.close()
        self.runFile.close()


    def resolveLocations(self, locations):
        resolvedLocations = []
        for location in locations:
            location = self.resolveLocation(location)
            resolvedLocations.append(location)
        return resolvedLocations


    def resolveLocation(self, location):
        location = location.strip()
        if (location == 'Chicago' or location == 'CHI' or location == 'chicago' or location == 'chi'):
            return '204517928/chicago-illinois'
        elif (location == 'New York City' or location == 'NYC' or location == 'nyc' or location == 'new york city'):
            return '212988663/new-york-new-york'
        elif (location == 'Los Angeles' or location == 'LA' or location == 'la' or location == 'los angeles'):
            return '212999109/los-angeles-california/'
        elif (location == 'Houston'):
            return '212962809/houston-texas'
        elif (location == 'Twin Cities'):
            return '237906866/twin-cities-mn'
        elif (location == 'Boston'):
            return '206698624/boston-massachusetts'
        elif (location == 'Seattle'):
            return '213941548/seattle-washington'
        elif (location == 'San Francisco'):
            return '44961364/san-francisco-california'
        elif (location == 'Philladelphia'):
            return '263256136/philladelphia-pa'
        elif (location == 'Miami'):
            return '212941492/miami-florida'
        elif (location == 'New Orleans'):
            return 'new-orleans-louisiana'
        elif (location == 'Denver'):
            return '4599325/denver-colorado'


    def debugMethod(self):
        self.hashtagMethod()
    #endregion



    #region LEVEL ONE
    def hashtagMethod(self):
        self.runFile.write('HASHTAG SOURCE:')
        random.shuffle(self.sourceParams)
        self.runFile.write('These are the hashtags used:')
        for tag in self.sourceParams:
            self.runFile.write(tag)

        maxNumberOfActionsPerHour = 100
        numberOfActioned = 0

        for hashtag in self.sourceParams:
            if (random.randint(0, 1)):
                numToAct = self.numberOfActions + random.randint(0, self.actionVariance)
            else:
                numToAct = self.numberOfActions - random.randint(0, self.actionVariance)

            if (numberOfActioned + numToAct >= maxNumberOfActionsPerHour):
                break
            else:
                numberOfActioned += numToAct
                self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
                time.sleep(random.randint(3,5))
                picHrefs = []
                hrefsScraped = 0
                while (hrefsScraped <= numToAct):
                    try:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(random.randint(4,5))
                        allHrefs = self.driver.find_elements_by_tag_name('a')
                        allHrefs = [elem.get_attribute('href') for elem in allHrefs if
                                    '.com/p/' in elem.get_attribute('href')]
                        [picHrefs.append(href) for href in allHrefs if href not in picHrefs]
                        hrefsScraped = picHrefs.__len__()
                    except Exception:
                        self.errorFile.write('Exception thrown when getting hrefs for #' + hashtag)
                        continue

                href = []
                counter = 0
                for h in allHrefs:
                    if counter < numToAct:
                        if (href.__contains__(h) == False):
                            href.append(h)
                            counter += 1
                    else:
                        break

                if(self.actionsString[0] == 'y'):
                    self.likePics(href)
                if(self.actionsString[1] == 'y'):
                    self.commentPics(href, self.comments)
                if(self.actionsString[2] == 'y'):
                    self.followUsers(href)


    def locationMethod(self):
        self.runFile.write('LOCATION SOURCE: ')
        self.sourceParams = self.resolveLocations(self.sourceParams)
        random.shuffle(self.sourceParams)
        self.runFile.write('These are the locations used:')
        for tag in self.sourceParams:
            self.runFile.write(tag)
        maxNumberOfActionsPerHour = 100
        numberOfActioned = 0

        for location in self.sourceParams:
            if (random.randint(0, 1)):
                numToAct = self.numberOfActions + random.randint(0, self.actionVariance)
            else:
                numToAct = self.numberOfActions - random.randint(0, self.actionVariance)

            if (numberOfActioned + numToAct >= maxNumberOfActionsPerHour):
                break
            else:
                numberOfActioned += numToAct
                self.driver.get("https://www.instagram.com/explore/locations/" + location + "/")

                time.sleep(random.randint(4,6))
                picHrefs = []
                hrefsScraped = 0
                while (hrefsScraped <= numToAct):
                    try:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(random.randint(2,6))
                        allHrefs = self.driver.find_elements_by_tag_name('a')
                        allHrefs = [elem.get_attribute('href') for elem in allHrefs if
                                    '.com/p/' in elem.get_attribute('href')]
                        [picHrefs.append(href) for href in allHrefs if href not in picHrefs]
                        hrefsScraped = picHrefs.__len__()
                    except Exception:
                        self.errorFile.write('Exception thrown when getting hrefs for location:' + location)
                        continue

                href = []
                counter = 0
                for h in allHrefs:
                    if counter < numToAct:
                        if (href.__contains__(h) == False):
                            href.append(h)
                            counter += 1
                    else:
                        break

                if(self.actionsString[0]):
                    self.likePics(href)
                if(self.actionsString[1]):
                    self.commentPics(href, self.comments)
                if(self.actionsString[2]):
                    self.followUsers(href)


    def fileMethod(self):
        self.runFile.write('FILE SOURCE: \n')
        self.runFile.write('The users that have been followed from the upload docs: \n')
        href = []
        for filename in os.listdir(self.uploadFolder):
            tempFile = open(self.uploadFolder + filename, 'r')
            for line in tempFile :
                href.append("https://www.instagram.com/" + line + "/")
            tempFile.close()

        #TODO: I currently pass in the url to the profile, i need to pass in the url to a photo from this profile
        if (self.actionString[0] == 'y'):
            self.likePics(href)
        if (self.actionString[1] == 'y'):
            self.commentPics(href, self.comments)
        if (self.actionString[2] == 'y'):
            self.followUsers(href)
        if (self.actionString[3] == 'y'):
            recentFollowers = self.checkForFollowing()
            hrefsToUnfollow = []
            for h in href:
                if (recentFollowers.__contains__(h) == False):
                    hrefsToUnfollow.append(h)
            self.unfollowUsers(hrefsToUnfollow)


    def checkForFollowing(self):
        driver = self.driver
        time.sleep(5)
        driver.get('https://www.instagram.com/' + self.username + '/')
        followersString = "//a[@href='/" + self.username + "/followers/']"
        waiter.find_element(driver, followersString, by=XPATH).click()
        time.sleep(random.randint(2,4))
        userHrefs = []
        hrefsScraped = 0
        counter = 0
        while (counter < 4):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randint(4, 5))
                allHrefs = driver.find_elements_by_tag_name('a')
                allHrefs = [elem.get_attribute('href') for elem in allHrefs if
                            '.com/' in elem.get_attribute('href')]
                allUserHrefs = []
                for ref in allHrefs[19:]:
                    u = list(ref.split("/"))
                    if u.__len__() == 5:
                        if ((u[3] != 'explore') or (u[3] != self.username)):
                            allUserHrefs.append(u)
                [userHrefs.append(href) for href in allUserHrefs if href not in userHrefs]
                hrefsScraped = userHrefs.__len__()
            except Exception:
                self.errorFile.write('Exception thrown when getting hrefs for people that follow you')
                continue
            counter += 1
        href = []
        counter = 0
        for h in allHrefs:
            if counter < 100:
                if (href.__contains__(h) == False):
                    href.append(h)
                    counter += 1
            else:
                break
        return href
    #endregion



    #region LEVEL TWO
    def likePics(self, hrefs):
        for picHref in hrefs:
            self.driver.get(picHref)
            time.sleep(random.randint(2,8))
            try:
                time.sleep(random.randint(3,6))
                likeButton = self.driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
            except Exception:
                self.errorFile.write('Error: There was a problem liking this pic: ' + picHref)
            time.sleep(random.randint(3,6))
        self.runFile.write('Completed.')


    def commentPics(self, hrefs, comments):
        numOfComments = comments.__len__() - 1
        for picHref in hrefs:
            time.sleep(random.randint(2, 4))
            self.driver.get(picHref)
            time.sleep(random.randint(4, 6))
            commentSection = ui.WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", commentSection)
            while(1 == 1):
                try:
                    commentSection = ui.WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
                    comment = comments[random.randint(0,numOfComments)]
                    commentSection.send_keys(comment)
                    commentSection.send_keys(Keys.ENTER)
                    time.sleep(random.randint(3,4))
                    break
                except Exception:
                    time.sleep(random.randint(5,6))
        self.runFile.write('Completed.')


    def followUsers(self, hrefs):
        badFollowButtons = []
        invalidUsername = []
        alreadyFollowing = []
        for picHref in hrefs:
            self.driver.get(picHref)
            time.sleep(random.randint(2, 10))
            #TODO: Need to scrape the username correctly
            user = picHref.split("/")
            user = user[3]
            try:
                followButtons = self.driver.find_elements_by_css_selector('button')
                for button in followButtons:
                    if button.text == "Follow":
                        followButton = button
                        break
            except Exception:
                badFollowButtons.append(user)
            try:
                if (followButton.text == 'Follow'):
                    followButton.click()
                    self.runFile.write(user)
                elif ((followButton.text == 'Following') or (followButton.text == 'Requested')):
                    alreadyFollowing.append(user)
                else:
                    if alreadyFollowing.__contains__(user) == False:
                        alreadyFollowing.append(user)
            except Exception:
                    invalidUsername.append(user)
            time.sleep(random.randint(2, 10))

        if (alreadyFollowing.__len__() != 0):
            self.runFile.write('(ALREADY FOLLOWING:) ')
            for u in alreadyFollowing:
                self.runFile.write(u)
        if (badFollowButtons.__len__() != 0):
            self.runFile.write('COULDNT FIND FOLLOW BUTTON FOR: ')
            for u in badFollowButtons:
                self.runFile.write(u)
        if (invalidUsername.__len__() != 0):
            self.runFile.write('INVALID USERNAMES: ')
            for u in invalidUsername:
                self.runFile.write(u)
        self.runFile.write('\n\nCompleted at ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '\n')


    def unfollowUsers(self, hrefs):
        for picHref in hrefs:
            self.driver.get(picHref)
            time.sleep(random.randint(2, 10))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                unfollowButton = self.driver.find_element_by_css_selector('button')
            except:
                self.runFile.write('Error: Couldnt find the unfollow button for: ' + picHref)
            if (unfollowButton.text == 'Following'):
                unfollowButton.click()
                unfollowButton2 = self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')
                if (unfollowButton2.text == 'Unfollow'):
                    unfollowButton2.click()
                    self.runFile.write(picHref)
            time.sleep(random.randint(2, 7))
        self.runFile.write('Completed.')
    #endregion



#region MAIN
if __name__ == "__main__" :
    myIG = IGActionAutomator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
    try:
        myIG.login()
        myIG.resolveDataSource()
        myIG.logout()
    except Exception:
        myIG.logout

#endregion