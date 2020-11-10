# TwitchStreamNotifier
A python script that uses the Twitch API to notify a user on the desktop when Twitch streamers of their choosing go online.

Important Information:

  StreamerNames.txt must be updated manually by the user to track their streamers of choice.
  Usernames should be entered one per line (some examples are included in the file by default).
  
  The script (TwitchStreamNotifier.pyw) REQUIRES that Config.txt is filled out.
  To get a ClientID and Client Secret, head to https://dev.twitch.tv/, login using your
  Twitch account, and head to "Your Console." On this page, click "Applications," and
  "Register Your Application." Set the name to anything of your choosing, and the 
  OAuth Redirect URLs to http://localhost. The category can be anything of your
  choosing as well. "Manage" this application to get a Client ID and Client Secret, and
  enter these into the Config.txt file.
