from pprint import pprint
import time
import random
import praw
import re
import datetime
import getpass

def timeTil(): #Returns a formatted length until the event
     td = datetime.datetime(year, month, day, hour, minute, 0) - datetime.datetime.now()
     days = td.days
     hours = int(td.seconds / 3600)
     minutes = int(td.seconds / 60) - (hours * 60) 
     return keyword + ': ' + str(days) + 'd:' + str(hours) + 'h:' + str(minutes) + 'm' + endKeyword

user_agent = ("Header Image Swappexr v0.0.5 by /u/bobjrsenior") #Let reddit know who you are
r = praw.Reddit(user_agent=user_agent)
r.login(input('Username: '), getpass.getpass()) #Input username, pass here
r.config.decode_html_entities = True
subredditName = input('Subreddit Name: ') #Name of the subreddit
subreddit = r.get_subreddit(subredditName)  #get the subreddit
updateSpeed = 60 #Update the timer every _ seconds
stylesheet = subreddit.get_stylesheet()['stylesheet']

#get inputs for dates and such
keyword = input('Keyword in sidebar to find: ')
endKeyword = input('Keyword that marks the end of the countdown (\\n if new line): ')
images = []
imageNameTemp = input('Image Name (q for done): ')
while (imageNameTemp != 'q'):
    images.append(imageNameTemp)
    imageNameTemp = input('Image Name (q for done): ')

while True: #Infinite Loop since it is a bot
    settings = r.get_settings(subredditName) #Get the subreddits settings
    #Update the local css with a new image
    stylesheet = re.sub(keyword + '.*' + endKeyword, keyword + '/background:url(%%' + images[random.randint(0, len(images) - 1)] + '%%)'+ endKeyword, stylesheet, 1)
    #Update the sub's css
    pprint(stylesheet)
    subreddit.set_stylesheet(stylesheet)
    #Sleep until we need to update again
    time.sleep(updateSpeed)
