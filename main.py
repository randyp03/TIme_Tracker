import entries
import json

COMMANDS = ["start (activity)", "end (activity)", "get summary", "quit app"]

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
    def get_summary(cls, contents):        
        choices = ['All Activities', 'Each Acvitity']
        num_activities = len(contents['activities'])
        if num_activities == 0:
            print('\nNo activities are logged.') 
            print('Please log an activity if you wish to view a summary')
            return
        
        try:
            print('\nFor which would you like a summary for?')
            for i in range(len(choices)):
                print(f'{i +1} - {choices[i]}')

            choice = int(input()) - 1

            if 0 <= choice < len(choices):
                # return total activities logged in json and average time elapsed for all activities
                if choice == 0:
                    avg_elapsed_time = sum([sum(activity['time_elapsed'])
                                            for activity 
                                            in contents['activities']]) / num_activities
                    print(f'\n{"*"*15} All Activities Summary {"*"*15}')
                    print(f'Total Activities: {num_activities}')
                    print(f'Average Time Elapsed: {round(avg_elapsed_time,2)} seconds')
                # return each activity, how many times they logged, and their average time elapsed
                elif choice == 1:
                    print(f'\n{"*"*15} Each Activity Summary {"*"*15}')
                    print('{:^15} - {:^25}'.format('Activities', 'Average Time (seconds)'))
                    for activity in contents['activities']:
                        print("{:^15} - {:^25}".format(activity['activity_name'],
                                                           sum(activity['time_elapsed'])/len(activity['time_elapsed'])))
            else: raise ValueError()
        except ValueError:
            print('Invalid input. Please enter a choice number.')
            cls.get_summary(contents=contents)

# Returns desired command and activity
def get_input():
    try:
        print('\nEnter command:')
        command, activity = input().lower().split(' ')
        # checks if user entered possible options
        if command not in ('start','end') and (command + activity) not in ('quitapp', 'getsummary'): 
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
        elif command == 'get':
            DATA.get_summary(contents=contents)
        # if user chooses to quit the program
        else:
            break


if __name__ == "__main__":
    main()