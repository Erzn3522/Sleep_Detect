import time

class TimeController:
     def set_timer(self, duration, unit):
        if unit == "seconds":
            seconds = duration
        elif unit == "minutes":
            seconds = duration * 60
        elif unit == "hours":
            seconds = duration * 3600
        else:
            print("Invalid unit. Please choose 'seconds', 'minutes', or 'hours'.")
            return

        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Timer started at {start_time} for {duration} {unit}.")

        time.sleep(seconds)

        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Timer completed at {end_time}.")