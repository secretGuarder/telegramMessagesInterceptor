# telegramMessagesInterceptor



**HELLO!**
**This is my first project in GitHub and i want to ask help me point out my shortcomings**

This algorithm monitors Telegram messages from a given user, immediately saves them and deletes them for you  
Thus you can protect yourself from unwanted messages at the wrong time without losing them  
At any time you can go to the local directory on your device and view incoming messages and media

## INSTALLATION
`pip install -r requirements.txt`

## USAGE
`python3 main.py`

## CONFIGURATION
- After launch will be requested path to save downloaded content  
  You can enter "d" to save default path
- After this you mast enter your Telegram API tokens
  If you don't know nothing about Telegram API read paragraph "How to get Telegram API tokens"  
- Then need to login using your telegram  
- In the end you must enter telegram Telegram User Id of your victim and set name for it
  If you don't know nothing about Telegram User Id read paragraph "How to get Telegram User Id"
  
The program will start listening messages and wait for victim message

## DEPENDENCIES

Outside libraries:
- Telethon

Included libraries:
- os
- json
- datetime
- re

### FILESYSTEM

1. Defaul path to save - ./saved_data (default)
    - Path with saved images       - ./saved_data/images
    - Path with saved videos       - ./saved_data/videos
    - Path with saved voices       - ./saved_data/voices
    - Path with saved documents    - ./saved_data/documents
2. config.json  
    This file contain current Telegram API tokens  
     Structure:
  ```
  {
  "api_id": 12345678,   
  "api_hash": "qwertyuiopasdfghjklzxcvbnm123456"
  }
  ```
  
4. target_list.json  
    This file contain current victims    
    Structure:    
  ```
  {
{"items":
  [
    {
    "id": 123456789,
    "name": "name1"
     },
     {
    "id": 987654321,
    "name": "name2"
     },  
   ]
  }
  ```
#### TELEGRAM API

You can get your tokens here https://my.telegram.org/apps
First of all you must login with Telegram  
API - GETTING STARTED - CREATE APPLICATION  
(it doesn't matter what you leave for app name and app web-site)  
__WARNING!!!__  
__Dont share recived tokens!!!__

#### TELEGRAM USER ID

Telegram user ID is a unique identifier assigned to each user account on the Telegram messaging platform.  
It is a numerical value that helps identify and distinguish individual users within the Telegram network.  

To get Telegram user id of victim you can use the https://t.me/userinfobot  
Resent him message from victim and you get him User Id

# DESIRE
This is my first project so i would like to ask for help  
If you find a bug, or my code is really bad, please tell me how to fix it. I will be very grateful)



