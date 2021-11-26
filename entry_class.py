
class entry():
    def __init__(self, activity, start_time=None, end_time=None):
        self.activity = activity
        self.start_time = start_time
        self.end_time = end_time

    def get_activity(self):
        return self.activity
    def get_start_time(self):
        return self.start_time
    def get_end_time(self):
        return self.end_time