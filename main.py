import youtube_dl
import cv2
import os
import shutil
import PIL.Image
import time
from numpy import interp

FPS = 60
SAVE_DIR = "./video"
CHARSET = [" ", ".", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]
BAD_APPLE = "https://www.youtube.com/watch?v=FtutLA63Cp8"


class Player:
    def __init__(self, fps: int = FPS, size: tuple[int, int] = (96, 36),
                 save_dir: str = SAVE_DIR, charset: list[str] = CHARSET):
        self.fps = fps
        self.size = size
        self.save_dir = save_dir
        self.charset = charset
        self.id = None

    @staticmethod
    def __create_dir(dir: str, force_refresh: bool = False) -> None:
        if force_refresh:
            shutil.rmtree(dir)

        if not os.path.exists(dir):
            os.makedirs(dir)

    @staticmethod
    def __asciify(self, path: str) -> str:
        image = PIL.Image.open(path)
        # get pixel array as grayscale
        pixeldata = image.convert('L').getdata()
        # match pixel luminosity to a character in the charset
        pixels = ''.join([self.charset[int(interp(pixel, [0, 255],
                          [0, len(self.charset) - 1]))]
                          for pixel in pixeldata])

        # Add line breaks to the string
        width = self.size[0]
        return '\n'.join([pixels[i:i + width]
                          for i in range(0, len(pixels), width)])

    def start(self) -> None:
        os.system("cls")
        inp = None
        # This kinda sucks right now but I'll rewrite it with a match
        # statement when libs get updated to python 3.10 :^)
        while inp not in ["1", "2"]:
            inp = input('What option would you like to select?\n'
                        '1: Play Bad Apple\n'
                        '2: Play another video\n'
                        'Selection: ')

        if inp == '1':
            self.__get_video()
        if inp == '2':
            os.system('cls')
            self.__get_video(input('Enter youtube link: '))

        self.__video_to_frames()
        self.__play()

    def __get_video(self, video_link: str = BAD_APPLE,
                    force_refresh: bool = False) -> None:
        # store the youtube video ID as identifier
        self.id = video_link.split("=")[-1]
        video_dir = f"{self.save_dir}/{self.id}"

        self.__create_dir(video_dir, force_refresh)

        with youtube_dl.YoutubeDL({
                "format": "bestvideo[ext=mp4][vcodec!*=av01]",
                "outtmpl": f"{video_dir}/{self.id}.mp4"
            }
        ) as ydl:
            ydl.download([video_link])

    def __video_to_frames(self, force_refresh: bool = False) -> None:
        os.system('cls')

        video_dir = f"{self.save_dir}/{self.id}"
        video_file = f"{video_dir}/{self.id}.mp4"
        cam = cv2.VideoCapture(video_file)

        self.__create_dir(f"{video_dir}/frames", force_refresh)

        current_frame = 0
        while True:
            ret, frame = cam.read()

            if ret:
                frame_loc = f"{video_dir}/frames/{current_frame}.png"
                # skip existing frames
                if os.path.exists(frame_loc):
                    continue
                # resize/grayscale frame and write to ./frames directory
                frame = cv2.resize(frame, self.size)
                cv2.imwrite(frame_loc, frame)
                print(f"Created frame {current_frame}")
                current_frame += 1
            else:
                # Final frame passed
                break

        # Properly shut down
        cam.release()
        cv2.destroyAllWindows()

    def __play(self) -> None:
        os.system('cls')

        video_dir = f"{self.save_dir}/{self.id}"
        current_frame = 0
        frame_loc = f"{video_dir}/frames/{current_frame}.png"
        while os.path.exists(frame_loc):
            frame = self.__asciify(self, frame_loc)
            # Clear the screen using ANSI escape sequence to avoid flickering
            # After that output the frame
            print(f"\033[0d{frame}")
            current_frame += 1
            frame_loc = f"{video_dir}/frames/{current_frame}.png"

            time.sleep(1/FPS)

        os.system('cls')
        print('End of video reached!')


def main():
    player = Player()
    player.start()


if __name__ == '__main__':
    main()
