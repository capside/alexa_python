from __future__ import print_function
import random

original_number=random.randint(1,100)
 
def lambda_handler(event, context):
    app_id = event['session']['application']['applicationId']
    tipo_req=event['request']['type']

    print("event.session.application.applicationId=" + app_id)
 
    #if (app_id != "Your Alexa APP ID"):
    #   raise ValueError("Invalid Application ID")
 
    if event['session']['new']:
        starting_session({'requestId': event['request']['requestId']},event['session'])

    if tipo_req == "LaunchRequest":
        return launch(event['request'], event['session'])
    elif tipo_req == "IntentRequest":
        return intent(event['request'], event['session'])
    elif tipo_req == "SessionEndedRequest":
        return session_end(event['request'], event['session'])
 
 
def starting_session(session_request_id, session):
    print("Session started: requestId=" + session_request_id['requestId']+", sessionId=" + session['sessionId'])
 
 
def launch(launch_request, session): 
    print("Launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    return welcome()
 
 
def intent(intent_request, session):
 
    print("Intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])
 
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == "GiveMeSomething":
        return give_me_number(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return welcome()
    else:
        raise ValueError("Intent does not exist")
 
 
def session_end(session_ended_request, session):
    """ Called when the user ends the session.
 
    Is not called when the skill returns end_session=true
    """
    print("Session end: requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
 
# ---------------skill's functions------------------
 
 
def welcome():
    session_attributes = {}
    card_title = "Welcome"
    speech = "Welcome to busy app. " \
                    "I'm very busy, so I will tell you a number and you can ask for the next one, the previous one or a random one, " \
                    "that's all..." \
                    "your number is" + str(original_number)

    re_speech = " you can tell me, next number, previous number or random number, your number is " + str(original_number)
    end_session = False
    return build_complete_response(session_attributes, build_response_internals(card_title, speech, re_speech, end_session))
 
 
def give_me_number(intent, session):
 
    card_title = intent['name']
    session_attributes = {}
    end_session = True
    number_type=''

    if 'Numbertype' in intent['slots']:
        number_type = intent['slots']['Numbertype']['value']
    
    numbercito=0
    if number_type == "next":
        numbercito=original_number+1
    elif number_type == "previous":
        numbercito=original_number-1
    elif number_type == "random":
        numbercito=random.randint(1,100)
    else:
        numbercito=200
 
    speech="you really want "+ str(numbercito) + " as a response, there you go"
    re_speech="tell me what I want to hear mate..."

    return build_complete_response(session_attributes, build_response_internals(card_title, speech, re_speech, end_session))
 
 
# ---------------Response Builders----------------
 
 
def build_response_internals(title, speech, re_speech, end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': speech
        },
        'card': {
            'type': 'Standard',
            'title': 'SessionSpeechlet - ' + title,
            'text' : 'SessionSpeechlet - ' + speech,
            'image' :  {
               'smallImageUrl' : "https://s3-eu-west-1.amazonaws.com/testskillbuc/busyskill.gif",
               'largeImageUrl' : "https://s3-eu-west-1.amazonaws.com/testskillbuc/busyskill.gif"
            } 
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': re_speech
            }
        },
        'shouldEndSession': end_session
    }
 
 
def build_complete_response(session_attributes, speech_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speech_response
    }
