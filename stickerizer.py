from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from ttkthemes import ThemedTk
from flask import Flask, render_template, request
import config
import image
import video
import os, sys

app = Flask(__name__)

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
        save_file = f"{self.script_folder}/{self.output_folder}/{output_file}"

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

"""class GUI:
    def __init__(self):
        self.version = config.version
        self.ws = ThemedTk(theme=config.ttktheme)
        self.ws.geometry("400x400")
        self.ws.title(f"Stickerizer v{self.version}")
        self.ws.resizable(False, False)

        self.Labelframe = LabelFrame(self.ws, text='Stickerizer')
        self.Labelframe.pack(expand=1, fill=BOTH, padx=10, pady=10)

        self.file = None

        select = Button(self.Labelframe, text="Choose a file to stickerize", command=self.choose_file)
        select.pack(fill=BOTH, padx=10, pady=10)

        self.stick_file = Label(self.Labelframe, text='No file selected', font=('Calibri', 14))
        self.stick_file.pack(fill=BOTH, padx=10, pady=10)

        start = Button(self.Labelframe, text="Start Stickerizing", command=self.run_stickerizing)
        start.pack(fill=BOTH, padx=10, pady=10)

        log = LabelFrame(self.ws, text='Output Log')
        log.pack(fill=BOTH, expand=1, padx=10, pady=10)

        self.textbox = Text(log, height=8, width=50, wrap=WORD, background='lightgray')
        self.textbox.pack()

    def choose_file(self):
        f = TKFunctions.choose_file()
        self.file = f

        if self.file:
            message = f'Selected file: {self.file}'
            self.stick_file.config(text=message)
            self.textbox.insert(INSERT, message + '\n')



    def run(self):
        self.ws.mainloop()
        sys.exit(0)
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_file', methods=['POST'])
def choose_file():
    root = Tk()
    root.withdraw()  # Скрыть окно tkinter
    file_path = filedialog.askopenfilename()
    root.destroy()  # Закрыть окно tkinter после выбора файла
    return file_path

def run_stickerizing(file):
    if file is None:
        return "File wasn't selected"

    result = ""
    if file.endswith('.png') or file.endswith('.jpg'):
        result = f'\nUsing Image processing...\n'
        r = Utils(file).stickerize_photo()
        result += r
    else:
        result = '\nUsing Video processing...\n'
        r = Utils(file).stickerize_video()
        result += r

    return result

@app.route('/upload', methods=['POST'])
def upload_file():
    file_path = request.form.get('file_path')
    processing_result = run_stickerizing(file_path)

    # Откройте файл лога для записи (дописывания) и добавьте запись
    with open('log.txt', 'a') as log_file:
        log_file.write(f'Selected file: {file_path}\n{processing_result}\n')

    # Верните результат обработки клиенту
    return f'Selected file: {file_path}\n{processing_result}'

if __name__ == "__main__":
    app.run()
