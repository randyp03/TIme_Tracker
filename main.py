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

    print('Total Alloted per Activity')

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


def main():
    # loop asks for activities to add/end time for 
    while True:
        action, activity = get_input()
        new_object = entry_class.entry(activity) # creates a new activity object

        while not action.startswith('quit'): # if user wants to end application,
                                             # enter 'quit app'

            if action == 'add': # gets start time
                new_object.start_time = get_now()
            elif action == 'end': # gets end time
                new_object.end_time = get_now()

            action, activity = get_input() # wait for new input
        break


    print(f'Activity: {new_object.get_activity()}\nStart Time: {new_object.get_start_time()}\nEnd Time: {new_object.get_end_time()}\n')


    # json format to enter into file
    y = {
        'name':'%s' %(new_object.activity),
        'time entries':[
            {
                'start':'%s' %(new_object.start_time),
                'end':'%s' %(new_object.end_time)
            }
        ]
    }

    # calls new_entry fucntion to add a new time entry
    activities.new_entry(y)

    # calls function to get total time elasped for each activity
    get_total_time()

main()








