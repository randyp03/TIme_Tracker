import datetime as dt

# class to create activity entries
class entries:
    DATE_FORMAT = "%x %X"

    def __init__(self, 
                 activity: str, 
                 start: str = None, 
                 end: str = None, 
                 time_elapsed: int = None) -> None:
        self.activity = activity
        self.start = start
        self.end = end
        self.time_elapsed = time_elapsed

    # starts the activity
    def start_activity(self):
        self.start = dt.datetime.today().strftime(self.DATE_FORMAT) 

    # ends the activity and calculated time elapsed during activity
    def end_activity(self):
        self.end = dt.datetime.today().strftime(self.DATE_FORMAT)

        self.time_elapsed = dt.timedelta.total_seconds(
            dt.datetime.strptime(self.end, self.DATE_FORMAT)
            - dt.datetime.strptime(self.start, self.DATE_FORMAT))
        