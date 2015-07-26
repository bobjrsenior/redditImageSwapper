from pprint import pprint
import time
import random
import praw
import re
import getpass
import webbrowser
user_agent = ("Header Image Swappexr v0.2.1 by /u/bobjrsenior") #Let reddit know who you are
r = praw.Reddit(user_agent=user_agent)
#Get the App information
r.set_oauth_app_info(client_id=input('Client ID: '),
                      client_secret=getpass.getpass(),
                      redirect_uri='http://127.0.0.1:65010/'
                                   'authorize_callback')
#Set permissions
url = r.get_authorize_url('uniqueKey', 'modconfig', True)
#Prompt user to grant access and get access code
print('Open the following url in a browser to authorize')
print(url)
print('After authorization copy the code at the end of the new url')
#Code from url after authorization
access_information = r.get_access_information(input('Access Code (In URL): '))

#r.login(input('Username: '), getpass.getpass()) #Input username, pass here
r.config.decode_html_entities = True
subredditName = input('Subreddit Name: ') #Name of the subreddit
subreddit = r.get_subreddit(subredditName)  #get the subreddit
stylesheet = subreddit.get_stylesheet()['stylesheet'] #get the css

#get The location of the css to replace
startKeyword = input('Keyword in sidebar to find: ')
endKeyword = input('Keyword that marks the end of the replacement (\\n if new line): ')

#Make keywords more regex compatable
startKeywordSan = re.sub('\*', '\*', startKeyword)
endKeywordSan = re.sub('\*', '\*', endKeyword)

#get the images in the cycle
images = []
curImage = 0
print('Order image names by time of day\nstarting with what the current image would be')
imageNameTemp = input('Image Name (q for done): ')
while (imageNameTemp != 'q'):
    images.append(imageNameTemp)
    imageNameTemp = input('Image Name (q for done): ')

#get the delay between image changes
timeDelay = int(input('Time between images (minutes): '))
timeDelay *= 60
cycles = 0
while True: #Infinite Loop since it is a bot
    cycles += 1
    settings = r.get_settings(subredditName) #Get the subreddits settings
    #Update the local css with a new image
    stylesheet = re.sub(startKeywordSan + '.*' + endKeywordSan, startKeyword + 'background:url(%%' + images[curImage] + '%%) no-repeat top left;'+ endKeyword, stylesheet, 1)
    #Update the sub's css
    subreddit.set_stylesheet(stylesheet)
    pprint(cycles)
    #Cycle to the next image
    curImage += 1
    if curImage == len(images):
        curImage = 0
    #Sleep until we need to update again
    time.sleep(timeDelay)
    r.refresh_access_information(access_information['refresh_token'])
