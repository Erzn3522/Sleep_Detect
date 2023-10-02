import cv2
import os
from video_stream import VideoStream
from frame_processor import FrameProcessor
from folder_controller import FolderController
from time_controller import TimeController


class VideoProcessor:
    def __init__(self, video_source=0, output_file='merged_frames.mp4'):
        self.video_stream = VideoStream(video_source)
        self.frame_processor = FrameProcessor()
        self.documents_path = "Documents"

        project_root = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
        self.folder_controller = FolderController(project_root, 20)
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
            
            # If the file doesn't exist, create it and write some initial content
            if not os.path.exists(self.documents_path):
                os.makedirs(self.documents_path)
            combined_file_name = os.path.join(self.documents_path, file_name)
            self.video_out = cv2.VideoWriter(combined_file_name, fourcc, 20.0, (width, height))
            
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
