import sort_memories
import sys

if __name__ == '__main__':
    print('1. Sort Memories')
    print('0. Exit')
    valid_choice = False
    while not valid_choice:
        valid_choice = True
        choice = input('Select option: ').strip(' ')
        if choice == '1':
            sort_memories.sortSnapchatMemories()
        elif choice == '0':
            sys.exit('Exiting program...')
        else:
            valid_choice = False
            print('Please enter a valid choice')