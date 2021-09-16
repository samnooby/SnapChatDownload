import sys
import json

if __name__ == '__main__':
    sys.exit('Please run main.py')


def showAccountInfo():
    with open('./json/account.json', 'r') as f:
        data = json.loads(f.read())
    
    with open('./json/friends.json', 'r') as f:
        friends = json.loads(f.read())

    with open('./json/location_history.json', 'r') as f:
        locations = json.loads(f.read())
    
    with open('./json/user_profile.json') as f:
        user_profile = json.loads(f.read())

    # Account info
    username = data['Basic Information']['Username']
    name = data['Basic Information']['Name']
    created = data['Basic Information']['Creation Date']
    num_devices = len(data['Device History'])
    current_device = f'{data["Device Information"]["Make"]} {data["Device Information"]["Model Name"]}'

    # Friends info
    num_friends = len(friends['Friends'])

    # Location info
    home = locations['Frequent Locations'][0]['City']
    latest_location = locations['Latest Location'][0]['City']

    sex = user_profile['Demographics']['Derived Ad Demographic']
    age = user_profile['Demographics']['Cohort Age']

    print(f'Hello {name}!')
    print(f'Your username is {username} and your account was created on {created}')
    print(f'You have had {num_devices} devices and are currently using a {current_device}')
    print(f'You have {num_friends} friends')
    print(f'You are a {age} {sex}')
    print(f'You probably live in {home} and are currently in {latest_location}')
