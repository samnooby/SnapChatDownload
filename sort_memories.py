import json
import os
import requests
import sys

FOLDER_NAME = "memories"

# findMissingMemories checks all the folders and 
def findMissingMemories():
    print("Finding missing memories...")
    # Gets the memories from the json file
    with open('memories_history.json', 'r') as f:
        data = json.loads(f.read())
        data = data["Saved Media"]

    missing_memories = []

    # Makes sure memories folder exists
    try:
        os.listdir(f'./{FOLDER_NAME}')
    except FileNotFoundError:
        print("Memories folder not found...\nCreating memories folder")
        os.makedirs(f'./{FOLDER_NAME}')
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
            if not filename in os.listdir(f'./{FOLDER_NAME}') and not filename in os.listdir(f'./{FOLDER_NAME}/{year}'):
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
            except requests.exceptions.Timeout:
                print(f'Timed out on memory {index}, {length - index} memories left')
                return
            except Exception as e:
                sys.exit(e)


            with open(filename, 'wb') as f:
                f.write(file_data.content)
    
            print(f'Created file {filename}')
        index = index + 1
    
    os.remove("./missingmemories.json")
    

def sortMemories():
    print("Sorting memories..")
    downloaded_memories = os.listdir(f'./{FOLDER_NAME}')

    for item in downloaded_memories:
        if item[-len(".jpg"):] in [".jpg", ".mp4"]:
            year = item[:len("2021")]

            # Make sure the folder for the year exists
            try:
                os.listdir(f'./{FOLDER_NAME}/{year}')
            except FileNotFoundError:
                print(f'Folder for {year} not found\nCreating {year} folder...')
                os.makedirs(f'./{FOLDER_NAME}/{year}')

            os.rename(f'./{FOLDER_NAME}/{item}', f'./{FOLDER_NAME}/{year}/{item}')
    
    print("Memories Sorted")

if __name__ == "__main__":
    # while findMissingMemories() > 0:
    #     downloadMemories()
    findMissingMemories()
    sortMemories()