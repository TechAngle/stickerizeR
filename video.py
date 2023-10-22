from moviepy.editor import *
import cv2
import config
from stickerizer import Utils


class VideoChange:
    """
    This class is used to change the video by reducing its size and speeding it up.

    Attributes:
        output_folder (str): The folder where the output video will be saved.
        script_folder (str): The folder where the script is located.
        max_video_size (tuple): The maximum size of the video.
        recommended_fps (int): The recommended frames per second for the output video.
    """
    def __init__(self):
        self.output_folder = 'output'
        self.script_folder = os.path.dirname(__file__)
        self.max_video_size = config.max_sticker_size
        self.recommended_fps = 30

    def reduce_video_ratio(self, vid: VideoFileClip):
        """
        Reduces the size of the video if its size exceeds the maximum size.

        Args:
            vid (VideoFileClip): The video to be resized.

        Returns:
            VideoFileClip: The resized video.
        """
        if tuple(vid.size) > self.max_video_size:
            # Resize the video to fit the max size using cv2.resize
            resized_frames = []
            for frame in vid.iter_frames(fps=vid.fps):
                resized_frame = cv2.resize(frame, self.max_video_size)
                resized_frames.append(resized_frame)
            # Creating VideoClip
            resized_video = ImageSequenceClip(resized_frames, fps=vid.fps,)

            return resized_video
        else:
            return 0

    def reduce_video(self, video: str) -> str:
        """
        Reduces the size and speeds up the video.

        Args:
            video (str): The path to the video to be changed.

        Returns:
            str: The path to the output video.
        """
        vid = VideoFileClip(video)

        duration = int(vid.duration)
        speedup = (duration // 3)  # Amount of speed up video

        if speedup > 10:
            return "Error: Video speedup too high"
        else:
            vid = vid.fx(vfx.speedx, speedup)  # Speed up the video
            resized_video = self.reduce_video_ratio(vid=vid)

        if resized_video == 0:
            return "Error: Video resizing failed"
        else:
            output_file = Utils(video).generate_unique_output_name(f'sticker#{config.video_sticker_type}')
            image_output_folder = os.path.join(self.script_folder, self.output_folder, output_file)

            # Write the video frames with the specified name format and codec
            resized_video.write_videofile(image_output_folder, codec="libvpx", fps=self.recommended_fps)

            return output_file
