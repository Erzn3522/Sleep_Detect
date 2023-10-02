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
