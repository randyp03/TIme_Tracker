import entries
from data_class import DATA

COMMANDS = ["start (activity)",
            "end (activity)",
            "get summary", 
            "get visual",
            "quit app"]

# Returns desired command and activity
def get_input():
    try:
        print('\nEnter command:')
        command, activity = input().lower().split(' ')
        # checks if user entered possible options
        if command not in ('start','end') and (command + activity) not in ('quitapp', 
                                                                           'getsummary',
                                                                           'getvisual'): 
            raise ValueError
        else:
            return command, activity
    except ValueError:
        print('Invalid input. Please enter a valid command (Ex. start work).')
        return get_input()


def main():
    # initialize json file
    contents = DATA.initialize_json()

    # display available commands
    print(f"{'*' * 15} Commands {'*' * 15}")
    for i in range(len(COMMANDS)):
        print(f'{i + 1}: {COMMANDS[i]}')

    activity_obj = None
    
    while True:
        # gets user commands
        command, activity = get_input()

        if command == 'start':
            # users cannot start two tasks simultaneously,
            # so it checks if there is an activity already started
            if activity_obj is not None:
                print('You must end an activity before starting another.')
            else:
                activity_obj = entries.entries(activity=activity.capitalize())
                activity_obj.start_activity()
        elif command == 'end':
            # users cannot end a task that hasn't been started,
            # so it checks if there is an activity in use and if activity names match
            if activity_obj is None or activity_obj.activity != activity.capitalize():
                print('Cannot end an activity that hasn\'t started')
            else:
                activity_obj.end_activity()
                DATA.add_activity(contents=contents, activity_obj=activity_obj)
                print('\nActivity Logged')
                # reinitialize object to start next activity
                activity_obj = None
        elif (command + activity) == 'getsummary':
            DATA.get_summary(contents=contents)
        elif (command + activity) == 'getvisual':
            DATA.get_visuals()
        # if user chooses to quit the program
        else:
            break


if __name__ == "__main__":
    main()