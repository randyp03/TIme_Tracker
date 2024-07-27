import entries
import json

COMMANDS = ["start (activity)", "end (activity)", "quit app"]

class DATA:
    JSON_FILE = "activities.json"
    JSON_TEMPLATE = {'activities': []}

    # intializes the json file
    @classmethod
    def initialize_json(cls):
        try:
            with open(cls.JSON_FILE, 'r') as file:
                contents = json.load(file)
            return contents
        
        except FileNotFoundError:
            with open(cls.JSON_FILE, 'w') as file:
                json.dump(cls.JSON_TEMPLATE, file, indent=4)
            return cls.initialize_json()

    # adds current activity information to the json file
    @classmethod
    def add_activity(cls, contents, activity_obj):
        # json template for a new activity
        x = {
            "activity_name": activity_obj.activity,
            "start": [activity_obj.start],
            "end": [activity_obj.end],
            "time_elapsed": [activity_obj.time_elapsed]
        }

        activity_list = [activity['activity_name'] for activity in contents['activities']]
        # checks if the current activity had been logged before
        if activity_obj.activity in activity_list:
            # adds the times to the already created activity
            index = activity_list.index(activity_obj.activity)
            contents['activities'][index]['start'].append(activity_obj.start)
            contents['activities'][index]['end'].append(activity_obj.end)
            contents['activities'][index]['time_elapsed'].append(activity_obj.time_elapsed)
        else:
            # appends a new activity to the contents dict
            contents['activities'].append(x)

        with open(cls.JSON_FILE, 'w') as file:
            json.dump(contents, file, indent=4)

    # Coming soon
    @classmethod
    def get_summary(cls):
        pass

# Returns desired command and activity
def get_input():
    try:
        print('\nEnter command:')
        command, activity = input().lower().split(' ')
        # checks if user entered possible options
        if command not in ('start','end') and (command + activity) != 'quitapp': 
            raise ValueError
        else:
            return command, activity
    except ValueError:
        print('Invalid input. Please enter start/end and the activity (Ex. start work)')
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
                activity_obj = entries.entries(activity=activity)
                activity_obj.start_activity()
        elif command == 'end':
            # users cannot end a task that hasn't been started,
            # so it checks if there is an activity in use and if activity names match
            if activity_obj is None or activity_obj.activity != activity:
                print('Cannot end an activity that hasn\'t started')
            else:
                activity_obj.end_activity()
                DATA.add_activity(contents=contents, activity_obj=activity_obj)
                print('\nActivity Logged')
                # reinitialize object to start next activity
                activity_obj = None
        # if user chooses to quit the program
        else:
            break


if __name__ == "__main__":
    main()