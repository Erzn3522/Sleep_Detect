import cv2
import time
import os

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

class FolderController:
    def __init__(self, folder_path, max_size_gb):
        self.folder_path = folder_path
        self.max_size_gb = max_size_gb

    def check_folder_size(self):
        # Calculate the current folder size
        folder_size = sum(os.path.getsize(os.path.join(self.folder_path, filename)) for filename in os.listdir(self.folder_path))
        
        # Convert the maximum size from GB to bytes
        max_size_bytes = self.max_size_gb * (1024 ** 3)
        
        if folder_size > max_size_bytes:
            cv2.destroyAllWindows()            
            # Stop the script
            print(f"Folder size exceeded {self.max_size_gb} GB. Stopping the script.")
            exit()

class VideoStream:
    def __init__(self, video_source=0):
        self.video = cv2.VideoCapture(video_source)
    
    def __del__(self):
        self.video.release()

    def read_frame(self):
        ret, frame = self.video.read()
        if ret:
            return frame
        return None

class FrameProcessor:
    def __init__(self, max_buffer_size=150, area_threshold=1000):
        self.prev_frame = None
        self.back_frame_buffer = []
        self.new_frame_buffer = []
        self.max_buffer_size = max_buffer_size
        self.area_threshold = area_threshold
        self.video_record_enabled = False
        self.timer_start = 0
    
    def process_frame(self, frame):
        self.video_record_enabled = False
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        if self.prev_frame is None:
            self.prev_frame = gray
            return
        
        frame_diff = cv2.absdiff(self.prev_frame, gray)
        thresh = cv2.threshold(frame_diff, 30, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        thresh = cv2.erode(thresh, None, iterations=2)
        cv2.imshow("Movement ", thresh)
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        movement_detected = False
        
        for contour in contours:
            if cv2.contourArea(contour) > self.area_threshold:
                print(cv2.contourArea(contour))
                movement_detected = True
                break

        if movement_detected:
            self.new_frame_buffer.append(frame.copy())
        else:
            if len(self.new_frame_buffer) > 60:
                self.back_frame_buffer.extend(self.new_frame_buffer)
                self.new_frame_buffer.clear()
                self.video_record_enabled = True

            self.back_frame_buffer.append(frame.copy())

            if len(self.back_frame_buffer) > self.max_buffer_size:
                self.back_frame_buffer = self.back_frame_buffer[-self.max_buffer_size:]
             
        self.prev_frame = gray
        return self.video_record_enabled

class VideoProcessor:
    def __init__(self, video_source=0, output_file='documents/merged_frames.mp4'):
        self.video_stream = VideoStream(video_source)
        self.frame_processor = FrameProcessor()
        self.folder_controller = FolderController("/Users/abdullaherzin/Documents/Projects/Sleep_Detect", 20)
        self.time_controller = TimeController()
        self.output_file = output_file
        self.video_out = None
        self.record_count = 0
        
    
    def __del__(self):
        if self.video_out is not None:
            self.video_out.release()
    
    def run(self):
        started_first_time = True
        while True:
            if started_first_time:
                # self.time_controller.set_timer(1, 'minutes')
                started_first_time = False
            frame = self.video_stream.read_frame()
            if frame is None:
                break
            self.folder_controller.check_folder_size()
            video_record_enabled = self.frame_processor.process_frame(frame)
            if video_record_enabled:
                self.merge_and_save_frames()
            cv2.imshow("Movement Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    
    def merge_and_save_frames(self):
        back_frame_buffer = self.frame_processor.back_frame_buffer
        
        if len(back_frame_buffer) > 0:
            height, width, _ = back_frame_buffer[0].shape
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            file_name = self.record_name_creator(self.output_file)
            self.video_out = cv2.VideoWriter(file_name, fourcc, 20.0, (width, height))
            
            for frame in back_frame_buffer:
                self.video_out.write(frame)
            self.frame_processor.back_frame_buffer.clear()
            self.video_out.release()

    def record_name_creator(self, record_file_name):
        # Split the filename into the base name and extension
        base_name, extension = record_file_name.rsplit('.', 1)
        
        # Add the number at the end of the base name
        new_filename = f"{base_name}_{self.record_counter()}.{extension}"
        return new_filename
    
    def record_counter(self):
        self.record_count += 1
        return self.record_count

# Usage
if __name__ == '__main__':
    video_processor = VideoProcessor()
    video_processor.run()
