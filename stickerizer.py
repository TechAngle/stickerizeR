from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from ttkthemes import ThemedTk
import config
import image
import video
import os

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
        file_types = [("JPEG", "*.jpg"), ("Video files", "*.mp4"), ("PNG", "*.png")]
        filename = filedialog.askopenfilename(filetypes=file_types)

        return filename

class GUI:
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

    def run_stickerizing(self):
        if self.file is None:
            self.textbox.delete(1.0, 'end')
            self.textbox.insert(INSERT, "File wasn't selected")
            return

        self.textbox.delete(1.0, 'end')
        self.textbox.insert(INSERT, 'Starting stickerizing image...\n')

        if self.file.endswith('.png') or self.file.endswith('.jpg'):
            self.textbox.insert(INSERT, "Using Image processing...\n")
            result = Utils(self.file).stickerize_photo()
            self.textbox.insert(INSERT, f'File successfully saved to {result}\n')
        else:
            self.textbox.insert(INSERT, 'Using Video processing...\n')
            result = Utils(self.file).stickerize_video()
            self.textbox.insert(INSERT, f'Video Sticker successfully saved to {result}\n')

    def run(self):
        self.ws.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
