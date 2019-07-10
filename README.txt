README:
This project is my first attempt at creating a more comprehensive look at Instagram automation. The main purpose of this
project is to create an easy to understand automation toolkit that can be built on and improved.


REQUIREMENTS (PIP INSTALL):
- numpy
- selenium
    + ChromeDriver
- explicit
- https://github.com/jacexh/pyautoit/archive/master.zip


TO DO:
- TODO: Figure out when/which hrefs I pass into all my level 2 methods
- TODO: Get rid of command line option
- TODO: Change the way that the main object is created (to the way that IGAccountCurator does it)
- Create test plan
- Do test scripts
- Make a master file that keeps track of every person followed from upload files
- Make a master file of users from upload file that followed you back
- Add more locations to resolve locations method


LEVEL ONE METHOD STATUS:
hashtagMethod:
- Working
- Converted (need to clean up last half)

locationMethod:
- Working
- Converted (need to clean up last half)

fileMethod:
- Working
- Converted (need to clean up last half)

combomashMethod:
- Working

checkForFollowing:
- Working

LEVEL TWO METHOD STATUS:
likePics:
- Working

commentPics:
- Working

followUsers:
- Working

unfollowUsers:
- Working

compareHrefs:
- Working





PARAMETER STRUCTURE:
"username" "password" "sourceType" "sourceParamsSepBy|" "numberOfActions" "actionVariance" "actionsString" "commentsSepBy|"


username: User intstagram username
password: User instagram password
sourceType:
    + Hashtags: 1
    + Locations: 2
    + Upload Files Folder: 3
sourceParamsSepBy|:
    + Hashtags: "hashtagOne|hashtagTwo|hashtagThree|etc"
    + Locations: "locationOne|locationTwo|locationThree|etc"
    + Files: "" (this is empty because it is take from a default location)
numberOfActions: The number of actions that you wan tot be performed in total for each action type
actionVariance: The max/min number of you want your actions to vary
actionsString: A string argument that is 4 characters long with each character being a 'y' or 'n', each position
corresponds to the following actions:
    + 1: Liking
    + 2: Commenting
    + 3: Following
    + 4: Unfollowing
commentsSepBy|: A list of all of the comments you wan to with '|' in between each comment


EXAMPLES:
"coppenmor" "Chicago2019!" 2 "fitness|chicago|health" 10 2 "ynnn" "Great post!|Love it!|Cool"