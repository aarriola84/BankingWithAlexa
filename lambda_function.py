from botocore.vendored import requests
import json

customerId = '5c685e90322fa06b677946a8'
apiKey = '545cdbbdcc6fba18396e01874ef112e5'

url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)
urlAccounts = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AddAccount":
        return createAccount()
    elif intent_name == "GetBalance":
        return getBalance(session['attributes']["accountID"])
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome, what would you like to do?."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = "Welcome to the help section for your bank account. A couple of examples of phrases that I can accept are... Add an account... or, Pay my bill. Lets get started now by trying one of these."

    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the Bank Account skill! We hope you enjoyed the experience."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# ---------- Functions used to interact with CapitalOne API---------------------

def createAccount():
    # MAKE SURE EVERY ACCOUNT HAS A UNIQUE NICKNAME
    customerSingle = requests.get(url)
    userAccount = customerSingle.json()
    
    card_title = "Add_Account"
    speech_output = "Account has been created."
    reprompt_text = speech_output
    should_end_session = False
    
    typeAccount = "Savings"
    nicknameAccount = "SavingsFirst"
    payload = {
        "type": typeAccount,
        "nickname": nicknameAccount,
        "rewards": 20,
        "balance": 200,
        }
    # Create a new Account
    response = requests.post(
        url,
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        )

    responseOutput = response.json()
    print(responseOutput['code'])
    print(responseOutput['message'])
    #get account id
    allAccounts = requests.get(urlAccounts)
    accountJSON = allAccounts.json()
    accountID = accountJSON[0]['_id']
    session_attributes = {"accountID": accountID}
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def getBalance(id):
    accountID = id
    urlSingle = 'http://api.reimaginebanking.com/accounts/{}?key={}'.format(accountID,apiKey)
    singleAccount = requests.get(urlSingle)
    singleJSON = singleAccount.json()
    
    card_title = "Get_Balance"
    speech_output = "Your account balance is " + str(singleJSON['balance']) + " dollars."
    reprompt_text = speech_output
    should_end_session = False
    session_attributes = {"accountID": accountID} #must pass persistent attributes everytime
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }