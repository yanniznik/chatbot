"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
import urllib.request



@route('/', method='GET')
def index():
    return template("chatbot.html")



# all the words and responses

UNKNOWN_RESPONSES = ["I have no idea what that means", "What did you say?", "What?", "Syntax Unrecognized, aborting speech protocol."]

GREETINGS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]

BYE = ("bye", "see ya", "cheers", "hasta la vista")
BYE_RESPONSES = ["bye dude", "see ya!", "don't forget to refresh me!", "OK, just don't shut me down"]

SWEAR = ("fuck", "dick", "balls", "asshole", "clusterfuck", "fuckface", "dipshit", "dumblefuck", "buttcrack")
SWEAR_RESPONSES = ["Congrats on swearing on an if/else statement", "Did your mom teach you that?", "Awww.."]

LOCATION = ("location", "live", "city", "from")

BOT = ("you", "your", "yours")

USER = ("me", "i", "my", "mine")

WEATHER = ("weather", "temperature")

JOKE_REQUEST = ("joke", "something funny", "make me laugh", "surprise me", "i'm bored")
JOKE_RESPONSES = ("A naked woman robbed a bank filled with men. Nobody could remember her face.", "Two women were sitting quietly", "Velcro, what a ripoff!")

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg').lower()
    return_message = checkSentence(user_message)
    return json.dumps(return_message)

def checkSentence(message):
    if "?" in message:
        if checkWord(BOT, message) and checkWord(LOCATION, message):
            return {"animation": "laughing", "msg": "I'm just code! I live in the computer"}
        elif checkWord(USER, message) and checkWord(LOCATION, message):
            return {"animation": "ok", "msg": "You're probably from Tel Aviv!"}
    if checkWord(GREETINGS, message):
        return {"animation": "ok", "msg": random.choice(GREETING_RESPONSES)} 
    elif checkWord(BYE, message):
        return {"animation": "heartbroke", "msg": random.choice(BYE_RESPONSES)} 
    elif checkWord(SWEAR, message):
        return {"animation": "no", "msg": random.choice(SWEAR_RESPONSES)} 
    elif checkWord(JOKE_REQUEST, message):
        return {"animation": "giggling", "msg": random.choice(JOKE_RESPONSES)}
    elif checkWord(WEATHER, message):
        return {"animation": "giggling", "msg": data_fetch(url_builder("Tel Aviv"))} 
    else: 
        return {"animation": "confused", "msg": json.dumps(random.choice(UNKNOWN_RESPONSES))}

def checkWord(WORDS, message):
    for word in WORDS:
        if word in message:
            return True

#weather API

def url_builder(city_name):
    user_api = '9ae7fcb5721160d3f02a61f08d111fec'  # Obtain yours form: http://openweathermap.org/
    unit = 'metric'  # For Fahrenheit use imperial, for Celsius use metric, and the default is Kelvin.
    api = 'http://api.openweathermap.org/data/2.5/weather?q='     # Search for your city ID here: http://bulk.openweathermap.org/sample/city.list.json.gz
    full_api_url = api + str(city_name) + '&mode=json&units=' + unit + '&APPID=' + user_api
    return full_api_url

def data_fetch(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    return raw_api_dict

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
