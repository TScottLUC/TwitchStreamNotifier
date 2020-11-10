import requests #for getting Twitch data from the web
import time
from plyer import notification #allows use of desktop notifications
from PIL import Image #used to make the streamer's profile image the notification icon

#readConfigFile reads information used for API calls (Client ID and Client Secret)
#that should not be shared with others and returns a dictionary containing
#the two. All it searches for is a Config text file with two lines,
#one starting with "Client_ID:" and one starting with "Client_Secret:"
def readConfigFile():
    configFile = open("Config.txt")
    d = dict()
    for line in configFile:
        if line.startswith("Client_ID:"):
            client_id = line[line.index(":")+1:].strip()
        elif line.startswith("Client_Secret:"):
            client_secret = line[line.index(":")+1:].strip()
    configFile.close()
    d["client_id"] = client_id
    d["client_secret"] = client_secret
    return d

#read the client id and secret from the config file
#and store them in variables
config = readConfigFile()
client_id = config.get("client_id")
client_secret = config.get("client_secret")

#getAccessToken allows the user access to the twitch API
#through the use of their client id and secret, returning
#the access token given
def getAccessToken():
    autURL = "https://id.twitch.tv/oauth2/token"
    autParams={"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}
    autCall = requests.post(url=autURL, params=autParams)
    autData=autCall.json()
    return autData["access_token"]

access_token = getAccessToken()

#information needed to get Twitch streamer data
streamsURL = "https://api.twitch.tv/helix/streams"
headers = {"Client-ID": config.get("client_id"), "Authorization": "Bearer " + access_token}

#used to track whether the user was already notified of a streamer going live
#for each username provided, the value will be True if the user was already
#notified, or False if they have not (or the streamer is offline)
notifiedAlready = dict()

while(True): #repeats the following over and over

    namesFile = open("StreamerNames.txt") #user needs to add the streamers they want to be notified about to this text file

    for line in namesFile:

        user_login = line.strip()
        params = {"user_login": user_login} #used to pass the username to the API call

        StreamsCall = requests.get(url=streamsURL, headers=headers, params=params).json()
        stream = StreamsCall.get('data') #this will return nothing if the streamer is not live

        try:
            isLive = stream[0]['type'] == "live" #will return True if there is data, and the stream is live

        except: #there is no data, and therefore the streamer is not live
            isLive = False
            notifiedAlready[user_login] = False

        if (isLive and not notifiedAlready.get(user_login)): #streamer is live and user has not been notified yet

            #get the streamers user_name and their stream title from the API call
            userName=stream[0]["user_name"]
            streamTitle=stream[0]["title"]

            #get the streamers user_id from the API call
            userID = stream[0]['user_id']
            userParams={"id": userID}

            #get the user's profile picture URL from their data (passing the user_id) to the API parameters
            userURL="https://api.twitch.tv/helix/users"
            userCall=requests.get(url=userURL, headers=headers, params=userParams).json()
            imageURL = userCall.get('data')[0]["profile_image_url"]

            #use PIL's Image to open the imageURL and save it as an ICO
            profilePic = Image.open(requests.get(imageURL, stream=True).raw)
            profilePic.save('profile.ico',format = "ICO")
            profileICO = "profile.ico"

            #notify the user that the streamer is live, using their profile picture as the icon
            notification.notify(
                title = userName + " is live on Twitch!",
                message=streamTitle,
                app_icon=profileICO,
                timeout=10
            )

            notifiedAlready[user_login] = True #the user has now been notified
            
    namesFile.close() 
    time.sleep(120) #wait 2 minutes before checking if the streamers are live again
