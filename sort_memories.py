import json
import os
import requests
import sys

from datetime import datetime

FOLDER_NAME = "memories"

# findMissingMemories checks all the folders and 
def findMissingMemories():
    print("Finding missing memories...")
    # Gets the memories from the json file
    try:
        with open('./json/memories_history.json', 'r') as f:
            data = json.loads(f.read())
            data = data["Saved Media"]
    except FileNotFoundError:
        sys.exit("Error: Make sure json folder is in directory")


    missing_memories = []

    # Makes sure memories folder exists
    try:
        os.listdir(f'./{FOLDER_NAME}')
    except FileNotFoundError:
        print("Memories folder not found...\nCreating memories folder")
        os.makedirs(f'./{FOLDER_NAME}')
        # os.makedirs("memories")
        with open('./missingmemories.json', 'w') as f:
            json.dump(data, f)
        
        print(f'Found {len(data)} missing memories')
        return len(data)

    for item in data:
        # Gets item information and filename
        date_time = item["Date"].split(" ")
        media_type = item["Media Type"]

        day = date_time[0]
        year = day[:len("2021")]
        time = date_time[1].replace(':', '-')

        filename = f'{day}_{time}.mp4' if media_type == 'VIDEO' else f'{day}_{time}.jpg'

        # check if it exists in memories or year folder
        try:
            if not filename in os.listdir(f'./{FOLDER_NAME}'):
                missing_memories.append(item)
        except FileNotFoundError:
            missing_memories.append(item)

    # Put remaining memories in json file to be downloaded
    with open('./missingmemories.json', 'w') as f:
        json.dump(missing_memories, f)
    
    print(f'Found {len(missing_memories)} missing memories')
    return(len(missing_memories))

def downloadMemories():
    print("Downloading missing memories...")
    # Gets all memory data from json file
    with open('missingmemories.json', 'r') as f:
        data = json.loads(f.read())
    
    index = 0
    length = len(data)
    
    for item in data:
        # Memory data
        url = item["Download Link"]
        date_time = item["Date"].split(" ")
        media_type = item["Media Type"]
        downloaded = False
    
        day = date_time[0]
        time = date_time[1].replace(':', '-')
        filename = f'{FOLDER_NAME}/{day}_{time}.mp4' if media_type == 'VIDEO' else f'{FOLDER_NAME}/{day}_{time}.jpg'
    
        # Check if exists
        if filename[len("memories/"):] in os.listdir(f'./{FOLDER_NAME}'):
            print("Memory already exists")
        else:
            print(f'Getting data for memory {index} out of {length}...')
            try:
                req = requests.post(url, allow_redirects=True)
                response = req.text
                file_data = requests.get(response)
                downloaded = True
            except requests.exceptions.Timeout:
                print(f'Timed out on memory {index}, {length - index} memories left')
                return
            except Exception as e:
                if req.status_code != 500:
                    print("Are your download links still valid? They exipire 7 days are the data is requested\nRedownload your data at: https://accounts.snapchat.com/accounts/downloadmydata")
                    sys.exit(e)
                print("Invalid download link... Memory may be deleted, moving on")

            if downloaded:
                with open(filename, 'wb') as f:
                    f.write(file_data.content)
    
                print(f'Created file {filename}')
        index = index + 1
    
    os.remove("./missingmemories.json")
    
def sortMemories(sort_by='year'):
    print("Sorting memories..")

    # Sets the level of sorting depeding on the input
    if sort_by == 'hour':
        sort_level = 3
    elif sort_by == 'day':
        sort_level = 2
    elif sort_by == 'month':
        sort_level = 1
    else:
        sort_level = 0

    downloaded_memories = os.listdir(f'./{FOLDER_NAME}')

    for item in downloaded_memories:
        if item[-len(".jpg"):] in [".jpg", ".mp4"]:
            levels_left = 0
            date = [item[:len("2021")], item[len("2021-"):len("2021-01")], item[len("2021-01-"):len("2021-01-01")], item[len("2021-01-01_"):len("2021-01-01_15")]]

            item_location = f'./{FOLDER_NAME}'

            while levels_left <= sort_level:
                # Make sure the folder for the year exists
                try:
                    os.listdir(f'{item_location}/{date[levels_left]}')
                except FileNotFoundError:
                    print(f'Folder for {date[levels_left]} not found\nCreating {date[levels_left]} folder...')
                    os.makedirs(f'{item_location}/{date[levels_left]}')

                item_location = f'{item_location}/{date[levels_left]}'
            
                levels_left = levels_left + 1

            print(f'Adding {item} to {item_location}')
            os.rename(f'./{FOLDER_NAME}/{item}', f'{item_location}/{item}')
    
    print("Memories Sorted")

def sortMemoriesByLocation():
    downloaded_memories = os.listdir(f'./{FOLDER_NAME}')
    try:
        with open('./json/location_history.json', 'r') as f:
            data = json.loads(f.read())
            locations = data["Areas you may have visited in the last two years"]
    except FileNotFoundError:
        sys.exit("Error: Make sure json folder is in directory")

    for location in locations:
        location_time = location['Time'][:len('2021/01/02 12:00:00')]
        location['Time'] = datetime.strptime(location_time, '%Y/%m/%d %H:%M:%S')

    def locationDateTime(e):
        return e['Time']

    locations.sort(key=locationDateTime)

    for memory in downloaded_memories:
        memory_date = datetime.strptime(memory[:len('2021-09-06_21-20-58')], '%Y-%m-%d_%H-%M-%S')
        index = 1
        memory_location = locations[0]

        while memory_date > memory_location['Time'] and len(locations) > index:
            memory_location = locations[index]
            index = index + 1

        try:
            os.listdir(f'./{FOLDER_NAME}/{memory_location["City"]}')
        except FileNotFoundError:
            os.makedirs(f'./{FOLDER_NAME}/{memory_location["City"]}')

        os.rename(f'./{FOLDER_NAME}/{memory}', f'./{FOLDER_NAME}/{memory_location["City"]}/{memory}')



def resetSorting():
    folders = [f'./{FOLDER_NAME}']

    while len(folders) > 0:
        current_directory = folders.pop(0)
        directory_items = os.listdir(current_directory)
        for item in directory_items:
            if item[-len(".jpg"):] in [".jpg", ".mp4"]:
                os.rename(f'{current_directory}/{item}', f'./{FOLDER_NAME}/{item}')
            else:
                folders.append(f'{current_directory}/{item}')
        if len(os.listdir(current_directory)) == 0 and current_directory != f'./{FOLDER_NAME}':
            os.removedirs(current_directory)

if __name__ == "__main__":
    resetSorting()
    print(f'You have {findMissingMemories()} missing memories')
    find_memories = input("Do you want to find missing memories? (Y/N)")
    if find_memories == 'Y':
        downloadMemories()
    elif find_memories != 'N':
        print("Invalid response: Please enter either Y or N")
    sort_method = input("Select sort method (year, month, day, hour, location):")
    if sort_method == 'location':
        sortMemoriesByLocation()
    else:
        sortMemories(sort_by=sort_method)