from pprint import pprint
import time
import random
import praw
import re
import getpass

user_agent = ("Header Image Swappexr v0.1.0 by /u/bobjrsenior") #Let reddit know who you are
r = praw.Reddit(user_agent=user_agent)
r.login(input('Username: '), getpass.getpass()) #Input username, pass here
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
imageNameTemp = input('Image Name (q for done): ')
while (imageNameTemp != 'q'):
    images.append(imageNameTemp)
    imageNameTemp = input('Image Name (q for done): ')

#get the delat between image changes
timeDelay = int(input('Time between images (minutes): '))
timeDelay *= 60
cycles = 0
while True: #Infinite Loop since it is a bot
    cycles += 1
    settings = r.get_settings(subredditName) #Get the subreddits settings
    #Update the local css with a new image
    stylesheet = re.sub(startKeywordSan + '.*' + endKeywordSan, startKeyword + 'background:url(%%' + images[random.randint(0, len(images) - 1)] + '%%) no-repeat top left;'+ endKeyword, stylesheet, 1)
    #Update the sub's css
    subreddit.set_stylesheet(stylesheet)
    pprint(cycles)
    #Sleep until we need to update again
    time.sleep(timeDelay)
