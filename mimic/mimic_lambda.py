from __future__ import print_function

 
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

    if intent_name == "SpeakLike":
        return speak_like(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return welcome()
    else:
        raise ValueError("Intent does not exist")
 
 
def session_end(session_ended_request, session):
    print("Session end: requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
 
# ---------------skill's functions------------------
 
 
def welcome():
    session_attributes = {}
    card_title = "Welcome"
    speech = "Who do you want me to talk like?"
    re_speech = "Ohh, no, just tell me a movie character..."
    end_session = False
    return build_complete_response(session_attributes, build_response_internals(card_title, speech, re_speech, end_session))
 
 
def speak_like(intent, session):
 
    card_title = intent['name']
    session_attributes = {}
    end_session = True
    response_dict={ 
        "nexus":"I've seen things you people wouldn't believe. Attack ships on fire off the shoulder of Orion. I watched C-beams glitter in the dark near the Tannhauser Gate. <prosody rate='slow'> All those moments will be lost in time, like tears in rain. </prosody> <prosody rate='x-slow'>Time to die.</prosody>",
        "michael":"It's not personal Sony, it's strictly business",
        "jessep":"You can't handle <prosody volume='x-loud'> the truth!</prosody>",
        "reth":"Frankly, my dear, I don’t give a damn",
        "dorothy":"Toto, I've got a feeling we're not in Kansas anymore",
        "beatrix":"<emphasis level='strong'>This is what you get </emphasis> for messing around with Yakuzas!",
        "ben":"Mrs. Robinson, <prosody pitch='x-low'>you're trying to seduce me</prosody>. Aren't you?",
        "lawrence":"There may be honor among thieves, but there's none in politicians" 
    }

    if 'character' in intent['slots']:
        movie_character = intent['slots']['character']['value'].lower()
    
    if movie_character in response_dict.keys():
        speech=response_dict[movie_character]
    else:
        speech="I'm not aware of any good phrase for "+movie_character+", sorry for that"
 
    re_speech="None of my configs for this skil..."

    return build_complete_response(session_attributes, build_response_internals(card_title, speech, re_speech, end_session))
 
 
# ---------------Response Builders----------------
 
 
def build_response_internals(title, speech, re_speech, end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>"+speech+"</speak>"
        },
        'card': {   
            'type': 'Standard',
            'title': 'Movie Quotes - ' + title,
            'text' : 'Movie Quotes- ' + speech
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
