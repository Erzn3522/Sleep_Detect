import cv2


class FrameProcessor:
    def __init__(self, max_buffer_size=150, area_threshold=1000):
        self.prev_frame = None
        self.back_frame_buffer = []
        self.new_frame_buffer = []
        self.max_buffer_size = max_buffer_size
        self.area_threshold = area_threshold
        self.video_record_enabled = False
        self.timer_start = 0
    
    def _movement_detector(self, contours):
        for contour in contours:
            if cv2.contourArea(contour) > self.area_threshold:
                print(cv2.contourArea(contour))
                movement_detected = True
                break
            else:
                movement_detected = False
        return movement_detected
    
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
        movement_detected = self._movement_detector(contours)
        

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