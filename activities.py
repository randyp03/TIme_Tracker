import json

def new_entry(new_data, filename='time_data.json'):
	file = open(filename, 'r+')
	# First we load existing data into a dict.
	file_data = json.load(file)
	
    # gets all activities already entered
	activity_list=[]
	for activity in file_data["activities"]:
		activity_list.append((activity["name"]))

	# if activity is not in list, add new activity to json file    
	if new_data["name"] not in activity_list:
		# Join new_data with file_data inside activities
		file_data["activities"].append(new_data)
		# Sets file's current position at offset.
		file.seek(0)

	# if the activity is in the list, then add a new start time for current activity
	elif new_data["name"] in activity_list:
		temp_dict = {}
		index = activity_list.index(new_data["name"])

		for time in new_data["time entries"]:
			temp_dict.update(time)

		file.seek(0)
		file.truncate()
		file_data["activities"][index]["time entries"].append(temp_dict)

	# convert back to json.
	json.dump(file_data, file, indent = 2)

		