README:
This project aims to create an easy to understand automation toolkit for Instagram that can be collaboratively built on
and improved.



FUNCTIONALITY:
- Like from:
    + Hashtag
    + Location
    + File
- Comment from:
    + Hashtag
    + Location
    + File
- Follow from:
    + Hashtag
    + Location
    + File
- Unfollow users that:
    + You recently followed
    + You recently followed and didn't follow you back



REQUIREMENTS (PIP INSTALL):
- numpy
- selenium
    + ChromeDriver
- explicit
- https://github.com/jacexh/pyautoit/archive/master.zip



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



TO DO:
- TODO: Figure out when/which hrefs I pass into all my level 2 methods
- TODO: Get rid of command line option
- TODO: Change the way that the main object is created (to the way that IGAccountCurator does it)
- Create test plan
- Do test scripts
- Make a master file that keeps track of every person followed from upload files
- Make a master file of users from upload file that followed you back
- Add more locations to resolve locations method