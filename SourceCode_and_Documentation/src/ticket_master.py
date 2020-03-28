import json, requests
from event import Event
from datetime import datetime, timedelta

URL = 'https://app.ticketmaster.com/discovery/v2/events'

CLASSIFICATIONS = [
    'Hip-Hop',
    'Arts & Theatre'
]

def get_events():
    event_list = []

    for classification in CLASSIFICATIONS:
        # Parameters for get request which includes , apikey, classifications and event date times.
        client_info = dict(
            classificationName=classification,
            apikey = 's1zvxw6AwOPPr7ej3vaA4EykE2LeO0vU',
            source='ticketmaster',
            countryCode='AU',
            stateCode='NSW',
            StartDateTime=datetime.now().isoformat()[:-7] + 'Z',
            EndDateTime=(datetime.now() + timedelta(days=1)
                         ).isoformat()[:-7] + 'Z'
        )

        response = requests.get(url=URL, params=client_info)
        data = json.loads(response.text)
        
        if '_embedded' in data:
            event = data['_embedded']['events']
            
            for info in event:
                event_obj = parseInfoToEvent(info)
                event_list.append(event_obj)

    return event_list
                
def parseInfoToEvent(info):
    start_time = ""
    end_time = ""
    url = ""
    summary = ""
    organiser = ""
    tags = []
    latitude = info['_embedded']['venues'][0]['location']['latitude']
    longitude = info['_embedded']['venues'][0]['location']['longitude']
    is_online = True
    price = False
    
    if info['dates']['status']['code'] == 'cancelled':
        is_online = False
    if 'dates' in info:
        if 'start' in info['dates']:
            if 'dateTime' in info['dates']['start']:
                start_time = info['dates']['start']['dateTime']
    if 'info' in info:
        summary = info['info']
    if 'promoter' in info:
        organiser = info['promoter']['name']
    if 'url' in info:
        url = info['url']
    if 'classifications' in info:
        call = info['classifications'][0]
        tags = [call['segment']['name'],call['genre']['name'],call['subGenre']['name']]
    
    event_info = Event(info['id'],url, start_time, end_time, latitude, longitude, 
        info['name'], organiser ,price, is_online, summary, tags, [])

    return event_info
