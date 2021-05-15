import youtube_dl
import cv2
import os
import shutil
import PIL.Image
import time

CHARSET = [".", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]
FPS = 30


def get_apple(video_link='https://www.youtube.com/watch?v=FtutLA63Cp8'):
    if os.path.exists('./video'):
        shutil.rmtree('./video')
    os.makedirs('./video')

    with youtube_dl.YoutubeDL({'format': 'bestvideo[ext=mp4][vcodec!*=av01]',
                               'outtmpl': '/video/video.mp4'}) as ydl:
        ydl.download([video_link])


def video_to_frames():
    cam = cv2.VideoCapture('./video/video.mp4')

    if os.path.exists('./frames'):
        shutil.rmtree('./frames')
    os.makedirs('./frames')

    currentframe = 0
    while True:
        ret, frame = cam.read()

        if ret:
            # resize/grayscale frame and write to ./frames directory
            frame = cv2.resize(frame, (96, 36))
            name = './frames/frame' + str(currentframe) + '.png'
            cv2.imwrite(name, frame)
            print('creating frame ' + str(currentframe))
            currentframe += 1
        else:
            # no more frames left
            break

    # properly shut down :)
    cam.release()
    cv2.destroyAllWindows()


def asciify(path):
    image = PIL.Image.open(path)
    pixels = image.convert('L').getdata()
    image_string = ''.join([CHARSET[pixel//25] for pixel in pixels])
    return image_string


def display_frames():
    currentframe = 0
    currentframe_path = './frames/frame' + str(currentframe) + '.png'
    try:
        image = PIL.Image.open(currentframe_path)
        width = image.size[0]
        image.close()
    except Exception:
        print('Could not find image sequence.')
        return

    while os.path.exists(currentframe_path):
        image_string = asciify(currentframe_path)
        total_pixels = len(image_string)

        result = '\n'.join(
            [image_string[index:index + width] for index in range(0, total_pixels, width)])

        os.system('cls')
        print(result)

        currentframe += 1
        currentframe_path = './frames/frame' + str(currentframe) + '.png'
        time.sleep(1/FPS)

    os.system('cls')
    print('End of video reached')


def main():
    os.system('cls')
    inp = None
    while inp not in ['1', '2', '3']:
        inp = input('What option would you like to select?\n1: Download Bad Apple and play\n2: Download custom video '
                    'and play\n3: Play downloaded video\nSelection: ')

    if inp == '1':
        get_apple()
        video_to_frames()
        display_frames()

    if inp == '2':
        os.system('cls')
        get_apple(input('Enter youtube link: '))
        video_to_frames()
        display_frames()

    if inp == '3':
        display_frames()


if __name__ == '__main__':
    main()
