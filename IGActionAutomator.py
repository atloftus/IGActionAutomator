import time
import sys
import random
import datetime
import os.path
import numpy as np
import autoit
import itertools
import selenium

from explicit import waiter, XPATH, NAME, CSS
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import ui

class IGActionAutomator :
    #region INITIALIZATION
    def __init__ (self, username, password) :
        self.username = username
        self.password = password
        self.sourceType = 0
        self.sourceParams = ""
        self.numberOfActions = 0
        self.actionsString = ""
        self.comments = ""
        cOptions = Options()
        cOptions.add_argument("--incognito")
        cOptions.add_argument("--start-maximized")
        cOptions.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
        self.driver = webdriver.Chrome(executable_path="venv/Lib/chromedriver_win32/chromedriver.exe", options=cOptions)
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
        time.sleep(random.randint(1,2))


    def setUpPassedInParams(self, sourceType, sourceParams, numberOfActions, actionVariance, actionsString, comments):
        self.sourceType = int(sourceType)
        sourceParamsFull = str(sourceParams)
        self.sourceParams = sourceParamsFull.split('|', 30)
        self.numberOfActions = int(numberOfActions)
        self.actionVariance= int(actionVariance)
        self.actionsString = str(actionsString).lower()
        commentsFull = str(comments)
        self.comments = commentsFull.split('|', 30)


    def getDataSource(self):
        myIG.setupLogFiles(username)
        myIG.login()

        if (self.sourceType == 0):
            print('')
            print('Possible data sources: ')
            print('1.) Hashtag')
            print('2.) Location')
            print('3.) File')
            self.sourceType = int(input('What source do you want to use for your actions? '))
            if ((self.sourceType != 1) or (self.sourceType != 2) or (self.sourceType != 3)):
                self.sourceType = 1

        if (self.sourceType == '1'):
            myIG.hashtagMethod()
        elif (self.sourceType == '2'):
            myIG.locationMethod()
        elif (self.sourceType == '3'):
            myIG.fileMethod()
        myIG.closeLogFiles()


    def logout(self) :
        self.driver.close()
        self.closeLogFiles()


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


    def resolveActionsToPerform(self):
        if (self.actionsString == ''):
            self.actionString[0] = str(input('Do you want to like random pictures (y/n)')).lower()
            if ((self.actionString[0] != 'y') or (self.actionString[0] != 'n')) :
                self.actionString[0] = 'n'
            self.actionString[1] = str(input('Do you want to comment on random pictures (y/n)')).lower()
            if ((self.actionString[1] != 'y') or (self.actionString[1] != 'n')) :
                self.actionString[1] = 'n'
            if (self.actionsString[1] == 'y'):
                self.comments = []
                newComment = input(
                    'Please enter each comment and then hit enter (hit enter on a new line to complete entering comments) (hit enter without entering anything to use default comments): ')
                while newComment != '':
                    self.comments.append(newComment)
                    newComment = input('Next Comment: ')
            self.actionString[2] = str(input('Do you want to follow random users (y/n)')).lower()
            if ((self.actionString[2]  != 'y') or (self.actionString[2]  != 'n')) :
                self.actionString[2] = 'n'
            if (self.actionString[2] == 'n'):
                self.actionString[3] = input('Do you want to unfollow these users if they havent followed you back (y/n)')
                if ((self.actionString[3] != 'y') or (self.actionString[3] != 'n')):
                    self.actionString[3] = 'n'


    def debugMethod(self):
        self.hashtagMethod()
    #endregion



    #region LEVEL ONE METHODS
    def hashtagMethod(self):
        self.runFile.write('HASHTAG SOURCE:')
        if (self.sourceParams == ''):
            self.sourceParams = str(input('What hashtags would you like to use as action sources (separate tags with a comma): '))
            self.sourceParams = self.sourceParams.split(',', 20)
        random.shuffle(self.sourceParams)
        self.runFile.write('These are the hashtags used:')
        for tag in self.sourceParams:
            self.runFile.write(tag)

        self.resolveActionsToPerform()

        if(self.numberOfActions == 0):
            self.numberOfActions = int(input('On average how many actions do you want to preform for each hashtag: '))
            self.actionVariance = int(input('How many actions +/- do you want the average to vary for each hashtag: '))
            print('Running...')

        maxNumberOfActionsPerHour = 60
        numberOfActioned = 0

        for hashtag in self.sourceParams:
            if (random.randint(0, 1)):
                numToAct = self.numberOfActions + random.randint(0, self.actionVariance)
            else:
                numToAct = self.numberOfActions - random.randint(0, self.actionVariance)

            if (numberOfActioned + numToAct >= maxNumberOfActionsPerHour):
                break
            else:
                self.runFile.write('These are the users followed from #' + hashtag + ':')
                numberOfActioned += numToAct

                driver = self.driver
                driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
                time.sleep(random.randint(3,5))
                picHrefs = []
                hrefsScraped = 0
                while (hrefsScraped <= numToAct):
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(random.randint(4,5))
                        allHrefs = driver.find_elements_by_tag_name('a')
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
        if (self.sourceParams == ''):
            self.sourceParams = str(input(
                'What locations would you like to like pics from (separate tags with a comma): '))
            self.sourceParams = self.sourceParams.split(',', 20)
        self.sourceParams = myIG.resolveLocations(self.sourceParams)
        random.shuffle(self.sourceParams)
        self.runFile.write('These are the locations used:')
        for tag in self.sourceParams:
            self.runFile.write(tag)

        self.resolveActionsToPerform()

        if(self.numberOfActions == 0):
            self.numberOfActions = int(input('On average how many actions do you want to preform for each hashtag: '))
            self.actionVariance = int(input('How many actions +/- do you want the average to vary for each hashtag: '))

        maxNumberOfActionsPerHour = 60
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
                driver = self.driver
                driver.get("https://www.instagram.com/explore/locations/" + location + "/")

                time.sleep(random.randint(4,6))
                picHrefs = []
                hrefsScraped = 0
                while (hrefsScraped <= numToAct):
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(random.randint(2,6))
                        allHrefs = driver.find_elements_by_tag_name('a')
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

        self.resolveActionsToPerform()

        if (self.actionString[0]):
            self.likePics(href)
        if (self.actionString[1]):
            self.commentPics(href, self.comments)
        if (self.actionString[2]):
            self.followUsers(href)
        if (self.actionString[3]):
            recentFollowers = self.checkForFollowing()
            hrefsToUnfollow = []
            for h in href:
                if (recentFollowers.__contains__(h) == False):
                    hrefsToUnfollow.append(h)
            self.unfollowUsers(hrefsToUnfollow)


    def combomashMethod(self):
        firstHashtag = input('What hashtag do you want to use as the first reference: ')
        while(True):
            whatIsSecondRef = input('Do you want to use a location or a second hashtag as your second source (enter H for hashtag and L for location): ')
            if ((whatIsSecondRef == 'h') or (whatIsSecondRef == 'h')):
                secondRef = input('What hashtag do you want to use as the second reference: ')
                break
            elif ((whatIsSecondRef == 'l') or (whatIsSecondRef == 'L')):
                holder = input('What location do you want to use as the second reference: ')
                secondRef = self.resolveLocation(holder)
                break
            else:
                print('Please pic chose one of the two options')
        numToAct = int(input('How many pictures from each source do you want to get: '))

        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + firstHashtag + "/")
        time.sleep(random.randint(3,5))
        picHrefs = []
        hrefsScraped = 0
        while (hrefsScraped <= numToAct):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randint(2,7))
                allHrefs = driver.find_elements_by_tag_name('a')
                allHrefs = [elem.get_attribute('href') for elem in allHrefs if
                            '.com/p/' in elem.get_attribute('href')]
                [picHrefs.append(href) for href in allHrefs if href not in picHrefs]
                hrefsScraped = picHrefs.__len__()
            except Exception:
                self.errorFile.write('Exception thrown when getting hrefs for #' + firstHashtag)
                continue
        firstHrefs = []
        counter = 0
        for h in allHrefs:
            if counter < numToAct:
                if firstHrefs.__contains__(h):
                    a = 1
                else:
                    firstHrefs.append(h)
                    counter += 1
            else:
                break

        if ((whatIsSecondRef == 'h') or (whatIsSecondRef == 'h')):
            driver.get("https://www.instagram.com/explore/tags/" + firstHashtag + "/")
        else:
            driver.get("https://www.instagram.com/explore/locations/" + secondRef + "/")

        time.sleep(random.randint(3,7))
        picHrefs = []
        hrefsScraped = 0
        while (hrefsScraped <= numToAct):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randint(2,7))
                allHrefs = driver.find_elements_by_tag_name('a')
                allHrefs = [elem.get_attribute('href') for elem in allHrefs if
                            '.com/p/' in elem.get_attribute('href')]
                [picHrefs.append(href) for href in allHrefs if href not in picHrefs]
                hrefsScraped = picHrefs.__len__()
            except Exception:
                self.errorFile.write('Exception thrown when getting hrefs for #' + firstHashtag)
                continue
        secondHrefs = []
        counter = 0
        for h in allHrefs:
            if counter < numToAct:
                if secondHrefs.__contains__(h):
                    #Do nothing
                    a = 1
                else:
                    secondHrefs.append(h)
                    counter += 1
            else:
                break
        self.compareHrefs(firstHrefs, secondHrefs)


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



    #region LEVEL TWO METHODS
    def likePics(self, hrefs):
        driver = self.driver
        for picHref in hrefs:
            driver.get(picHref)
            time.sleep(random.randint(2,10))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(3,6))
                likeButton = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                likeButton().click()
            except Exception:
                myIG.errorFile.write('Error: There was a problem liking this pic: ' + picHref)
                time.sleep(random.randint(3,6))
        self.runFile.write('Completed.')


    def commentPics(self, hrefs, comments):
        driver = self.driver
        numOfComments = comments.count() - 1
        for picHref in hrefs:
            driver.get(picHref)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            commentSection = ui.WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
            driver.execute_script("arguments[0].scrollIntoView(true);", commentSection)
            while(1 == 1):
                try:
                    commentSection = ui.WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
                    comment = comments[random.randint(0,numOfComments)]
                    commentSection.send_keys(comment)
                    commentSection.send_keys(Keys.ENTER)
                    time.sleep(random.randint(3,4))
                    break
                except Exception:
                    time.sleep(random.randint(5,6))
            time.sleep(random.randint(2,8))
        self.runFile.write('Completed.')


    def followUsers(self, hrefs):
        driver = self.driver
        for picHref in hrefs:
            driver.get(picHref)
            time.sleep(random.randint(2, 10))
            user = picHref.split("/")
            user = user[3]
            badFollowButtons = []
            invalidUsername = []
            alreadyFollowing = []

            try:
                followButtons = driver.find_elements_by_css_selector('button')
                for button in followButtons:
                    if button.text == "Follow":
                        followButton = button
                        break
            except:
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
            except StaleElementReferenceException:
                    invalidUsername.append(user)
            time.sleep(random.randint(2, 10))

        if (alreadyFollowing.count() != 0):
            self.runFile.write('(ALREADY FOLLOWING:) ')
            for u in alreadyFollowing:
                self.runFile.write(u)
        if (badFollowButtons.count() != 0):
            self.runFile.write('COULDNT FIND FOLLOW BUTTON FOR: ')
            for u in badFollowButtons:
                self.runFile.write(u)
        if (invalidUsername.count() != 0):
            self.runFile.write('INVALID USERNAMES: ')
            for u in invalidUsername:
                self.runFile.write(u)
        self.runFile.write('\n\nCompleted at ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '\n')


    def unfollowUsers(self, hrefs):
        driver = self.driver
        for picHref in hrefs:
            driver.get(picHref)
            time.sleep(random.randint(2, 10))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                unfollowButton = driver.find_element_by_css_selector('button')
            except:
                self.runFile.write('Error: Couldnt find the unfollow button for: ' + picHref)
            if (unfollowButton.text == 'Following'):
                unfollowButton.click()
                unfollowButton2 = driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')
                if (unfollowButton2.text == 'Unfollow'):
                    unfollowButton2.click()
                    self.runFile.write(username)
            time.sleep(random.randint(2, 7))
        self.runFile.write('Completed.')


    def dmUsers(self, hrefs):
        for picHref in hrefs:
            self.driver.get('https://www.instagram.com/')
            time.sleep(random.randint(2, 10))
            user = picHref.split("/")
            user = user[3]
            waiter.find_element(self.driver, "//*[@id=\"react-root\"]/section/nav[1]/div/div/header/div/div[2]/a", by=XPATH).click()
            time.sleep(random.randint(2, 4))
            waiter.find_element(self.driver, "/ html / body / div[3] / div / div / div[3] / button[2]",
                                by=XPATH).click()
            waiter.find_element(self.driver, "// *[ @ id = \"react-root\"] / section / div[1] / header / div / div[2] / button",
                                by=XPATH).click()
            toField = waiter.find_element(self.driver,
                                "// *[ @ id = \"react-root\"] / section / div[2] / div / div[1] / div / div[2] / input",
                                by=XPATH)
            time.sleep(random.randint(2, 5))
            toField.send_keys(user)
            time.sleep(random.randint(2, 5))
            waiter.find_element(self.driver,
                                "// *[ @ id = \"react-root\"] / section / div[2] / div / div[2] / div[1]",
                                by=XPATH).click()

            time.sleep(random.randint(2, 5))
            waiter.find_element(self.driver,
                                "//*[@id=\"react-root\"]/section/div[1]/header/div/div[2]/div/button",
                                by=XPATH).click()
            time.sleep(random.randint(2, 5))
            messageField = waiter.find_element(self.driver,
                                               "//*[@id=\"react-root\"]/section/div[2]/div[2]/div/div/div/textarea",
                                               by=XPATH)
            time.sleep(random.randint(2, 5))
            #TODO: Insert custom direct messages here
            messageField.send_keys("Hey I love your account!")
            time.sleep(random.randint(2, 5))
            waiter.find_element(self.driver,
                                "// *[ @ id = \"react-root\"] / section / div[2] / div[2] / div / div / div[2] / button",
                                by=XPATH).click()
            time.sleep(random.randint(30, 100))


    def compareHrefs(self, hrefs1, hrefs2):
        driver = self.driver
        firstUserArray = []
        secondUserArray  = []
        for h1 in hrefs1 :
            driver.get(h1)
            time.sleep(random.randint(1, 3))
            usernameLink = driver.find_element_by_xpath('// *[ @ id = "react-root"] / section / main / div / div / article / header / div[2] / div[1] / div[1] / h2 / a')
            user1 = usernameLink.text
            firstUserArray.append(user1)
            time.sleep(random.randint(1, 3))
        for h2 in hrefs2 :
            driver.get(h2)
            time.sleep(random.randint(1, 3))
            usernameLink = driver.find_element_by_xpath('// *[ @ id = "react-root"] / section / main / div / div / article / header / div[2] / div[1] / div[1] / h2 / a')
            user2 = usernameLink.text
            secondUserArray.append(user2)
            time.sleep(random.randint(1, 3))

        firstUserArray = np.array(firstUserArray)
        secondUserArray = np.array(secondUserArray)
        resultUserArray = np.intersect1d(firstUserArray, secondUserArray)

        self.userleadsFile.write('User Leads:\n')
        self.userleadsFile.write('Started At: ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '\n')
        self.userleadsFile.write('Total objects compared: ' + (hrefs1.count() * 2) + '\n\n')

        self.userleadsFile.write('Users in both sources: ' '\n')
        for u in resultUserArray:
            self.userleadsFile.write(u + '\n')
        if (resultUserArray.count() == 0):
            self.userleadsFile('None.\n')
        self.userleadsFile.write('Stopped At: ' + datetime.datetime.now().strftime("%I%M%p_%d%b%y") + '\n\n')
        self.userleadsFile.close()
    #endregion



#region MAIN
def main(argv):
    myIG = IGActionAutomator(argv[0], argv[1])
    myIG.setUpPassedInParams(argv[2],argv[3],argv[4],argv[5],argv[6],argv[7])
    myIG.setupLogFiles(myIG.username)
    myIG.login()
    myIG.closeLogFiles()


if __name__ == "__main__" :
    if (sys.argv.__len__() == 1):
        print('Hello and welcome to IGA1.0! \n')
        print('Please enter your Instagram information, or press enter to proceed in debug mode.\n')
        username = input('IG Username: ')
        #TODO: (Once param passing works) delete this debug functionality
        if (username == ''):
            auto = input('Hit enter again if you want to run the debug method: ')
            myIG = IGActionAutomator("coppenmor", "Chicago2019!")
            if (auto == ''):
                myIG.setupLogFiles(username)
                myIG.login()
                time.sleep(random.randint(2, 4))
                myIG.debugMethod()
            else:
                myIG.getDataSource()
        else:
            password = input('IG Password: ')
            myIG = IGActionAutomator(username, password)
            myIG.getDataSource()
        myIG.logout()
    else:
        main(sys.argv[1:])
#endregion