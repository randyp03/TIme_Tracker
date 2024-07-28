import data_visuals
import json

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

    # prints summary of activity logs, either as a whole or by activity
    @classmethod
    def get_summary(cls, contents):        
        choices = ['All Activities', 'Each Acvitity']
        num_activities = len(contents['activities'])
        # checks if there are any activities to summarize
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

    @classmethod
    def get_visuals(cls):
        data_visuals.main()