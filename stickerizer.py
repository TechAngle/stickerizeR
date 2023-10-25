from tkinter import *
from tkinter import filedialog

from flask import Flask, render_template, request

import config
import image
import video

import os, time, sys
import webbrowser as web
from multiprocessing import Process

sys.argv = [f'{__file__}']
app = Flask(__name__)

filen = None

class Utils:
    def __init__(self, file: str):
        self.output_file = f'sticker#{config.video_sticker_type}' if file.endswith('.mp4') else f'sticker#{config.image_sticker_type}'
        self.output_folder = 'output'
        self.script_folder = os.path.dirname(__file__)
        self.current_file = file

        self.counter = 0

    def generate_unique_output_name(self, base_name: str) -> str:
        output_file = base_name.replace("#", '0') # Changing to zero
        #print(output_file)
        while os.path.exists(f"{self.script_folder}/{self.output_folder}/{output_file}"):
            # File with the same name exists, increment the counter
            output_file = output_file.replace(f'{str(self.counter)}', f"{str(self.counter+1)}")
            self.counter += 1
            #print(output_file)

        return output_file

    def stickerize_photo(self):
        img = image.ChangeImage()

        if not os.path.exists(f"{self.script_folder}/{self.output_folder}"):
            os.mkdir(f'{self.script_folder}/{self.output_folder}')

        output_file = self.generate_unique_output_name(self.output_file)
        save_file = os.path.join(self.script_folder, self.output_folder, output_file)

        img_result = img.reduce_image_size(self.current_file)

        if img_result:
            img_result.save(save_file)
            return save_file
        else:
            print("Error occurred while processing the image.")
            return None


    def stickerize_video(self):
        _video = video.VideoChange()
        seq = _video.reduce_video(self.current_file)

        return seq

class TKFunctions:
    @staticmethod
    def choose_file():
        file_types = [("Images", "*.jpg *.png"), ("Videos", "*.mp4 *.avi *.mkv")]
        filename = filedialog.askopenfilename(filetypes=file_types)

        return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_file', methods=['POST'])
def choose_file():
    global filen
    file_path = TKFunctions().choose_file()
    filen = file_path
    return file_path

# Function restarting server if error occurred
def restart():
    os.execv(sys.executable, ['python'] + sys.argv)

def run_stickerizing(file):
    if file is None:
        return "File wasn't selected"

    result = ""
    utils = Utils(filen)
    try:
        if file.lower().endswith('.png') or file.lower().endswith('.jpg'):
            result = f'\nUsing Image processing...\n'
            r = utils.stickerize_photo()
            result += r
        else:
            result = '\nUsing Video processing...\n'
            r = utils.stickerize_video()
            result += r

        return result

    except AttributeError as e:
        print("Error occurred, restarting app...")
        print("Error:", e)
        restart()

@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = request.form.get('file_path')
    processing_result = run_stickerizing(file_path)

    with open('log.txt', 'a') as log_file:
        log_file.write(f'{processing_result}\n')

    return f'{processing_result}'

def run_flask_app():
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.run(host=config.host, port=config.port)

if __name__ == "__main__":
    app.config['PROPAGATE_EXCEPTIONS'] = True
    tk_functions = TKFunctions()

    web_thr = Process(target=web.open, args=(f'http://{config.host}:{config.port}',))
    web_thr.start()
    time.sleep(1)
    thr = Process(target=run_flask_app)
    thr.start()
