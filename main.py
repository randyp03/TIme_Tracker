import datetime as dt
import json
import activities
import entry_class

# get time elapsed in seconds
def get_seconds(time):
    a_timedelta = time - dt.datetime(1900,1,1)
    sec = a_timedelta.total_seconds()
    return sec

# gets the current time
def get_now():
    now = dt.datetime.now().strftime("%H:%M:%S")
    return now

# asks user to input activity and whether to start/end time for activity
# or quit to exit application altogether
def get_input():
    action, activity = input('Enter action (add/end) and corresponding activity, or "quit app" to exit: ').split(' ')
    action = action.strip()
    activity = activity.strip()
    return action, activity

# gets total time elapsed
def get_total_time():
    # opens json file and loads it into json module
    f = open("time_data.json", "r")
    data = json.load(f)
    f.close()

    print('Time Elapsed per Activity')

    # prints the name of each activity and
    # subtracts the start and end time to get total time spent
    for activity in data['activities']:
        total_time = 0
        for entry in activity['time entries']:
            start_time = dt.datetime.strptime(entry['start'], '%H:%M:%S')
            start_sec = get_seconds(start_time)

            end_time = dt.datetime.strptime(entry['end'], '%H:%M:%S')
            end_sec = get_seconds(end_time)

            sec_diff = end_sec - start_sec

            total_time += sec_diff

            td = dt.timedelta(seconds=total_time)

        print(f"{activity['name']}: {td}")

# function gets list of all activities in json file
def get_activity_list(filename='time_data.json'):
    file = open(filename, 'r+')
    # First we load existing data into a dict.
    file_data = json.load(file)
    # gets all activities already entered
    activity_list=[]
    for activity in file_data["activities"]:
    	activity_list.append((activity["name"]))
    
    return activity_list




def main():

    activity_list = get_activity_list()
    object_dict = {} # creates dictionary to allow control over two or more activties at once
    action, activity = get_input()

    while True:
        
        if action == 'start':
            # checks if this is a new activity or not
            if activity not in activity_list:
                print('New activity started')
                object_dict[activity] = entry_class.entry(activity) # creates a new activity object
                object_dict[activity].start_time = get_now() # gets start time for new activity

            elif activity in activity_list:
                object_dict[activity].start_time = get_now() # starts a new time for an old activity

        elif action == 'end': # gets end time
            object_dict[activity].end_time = get_now()

            # json format to enter into file
            y = {
                'name':'%s' %(object_dict[activity].activity),
                'time entries':[
                    {
                        'start':'%s' %(object_dict[activity].start_time),
                        'end':'%s' %(object_dict[activity].end_time)
                    }
                ]
            }

            # calls add_entry_data fucntion to add a new time entry
            activities.add_entry_data(y, activity_list)

        # in case user needs to know list of already used activities
        elif action == 'get' and activity == 'list':
            print('Activities on file:', activity_list)
            print('Activities currently in use:', list(object_dict.keys()))
        
        elif action == 'quit':
            break
        else:
            print('Invalid action, please restart program')
            break

        action, activity = get_input() # wait for new input

    # calls function to get total time elasped for each activity
    print()
    get_total_time()

# calls main function
main()
