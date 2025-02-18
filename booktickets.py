import json

def validate(slots):
    valid_cities = ['mumbai', 'delhi', 'bangalore', 'hyderabad']
    
    if not slots['theatre_location']:
        print("Inside Empty Location")
        return {
            'isValid': False,
            'violatedSlot': 'theatre_location'
        }
    
    if slots['theatre_location']['value']['originalValue'].lower() not in valid_cities:
        print("Not a valid location")
        return {
            'isValid': False,
            'violatedSlot': 'theatre_location',
            'message': f"We currently support only {', '.join(valid_cities)} as valid destinations."
        }
    
    if not slots['show_day']:
        return {
            'isValid': False,
            'violatedSlot': 'show_day',
        }
    
    if not slots['number_of_tickets']:
        return {
            'isValid': False,
            'violatedSlot': 'number_of_tickets'
        }
    
    if not slots['theater_name']:
        return {
            'isValid': False,
            'violatedSlot': 'theater_name'
        }
    
    if not slots['movie_name']:
        return {
            'isValid': False,
            'violatedSlot': 'movie_name'
        }
    
   
    
    return {'isValid': True}

def lambda_handler(event, context):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    validation_result = validate(event['sessionState']['intent']['slots'])
    
    print("Invocation Source:", event['invocationSource'])
    print("Slots:", slots)
    print("Intent Name:", intent)
    
    validation_result = validate(slots)
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit': validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
            
            if 'message' in validation_result:
                response["messages"] = [{
                    "contentType": "PlainText",
                    "content": validation_result['message']
                }]
            
            return response
        else:
            return {
                "sessionState": {
                    "dialogAction": { "type": "Delegate" },
                    "intent": { 'name': intent, 'slots': slots }
                }
            }
    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        return {
            "sessionState": {
                "dialogAction": { "type": "Close" },
                "intent": {
                    'name': intent,
                    'slots': slots,
                    'state': 'Fulfilled'
                }
            },
            "messages": [{
                "contentType": "PlainText",
                "content": "Thanks, I have placed your reservation."
            }]
        }
