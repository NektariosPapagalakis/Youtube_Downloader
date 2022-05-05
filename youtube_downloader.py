from tkinter import *
from tkinter import messagebox
import youtube_dl


def download_as_mp3(video_url):
    video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
    filename = f"{video_info['title']}.mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    print("Download complete... {}".format(filename))


BACKGROUND_COLOR = "#2C2C2C"
COLOR_1 = "#3796F6"
COLOR_2 = "#474747"


class YoutubeDownloader(Tk):

    def check_hand_enter(self, e):
        self.button_download_video.config(cursor="hand2")

    def __init__(self):
        super(YoutubeDownloader, self).__init__()

        self.geometry("600x200")
        self.title('Youtube Downloader')
        self.configure(background=BACKGROUND_COLOR)
        # Create Frames
        frame_insert_url = Frame(self, background=BACKGROUND_COLOR)
        frame_insert_url.pack(pady=10)
        label_insert_url = Label(frame_insert_url, text="Video url : ", bg=BACKGROUND_COLOR, foreground=COLOR_1,
                                 font=50)
        label_insert_url.grid(row=0, column=0)
        self.entry_insert_url = Entry(frame_insert_url, width=50, background=COLOR_2, foreground=COLOR_1, font=50)
        self.entry_insert_url.grid(row=0, column=1)

        self.button_download_video = Button(self, text="download", bg=COLOR_2, foreground=COLOR_1,
                                            command=self.download)
        self.button_download_video.bind("<Enter>", self.check_hand_enter)
        self.button_download_video.pack(pady=10)

    def download(self):
        url = self.entry_insert_url.get()
        download_as_mp3(url)
        messagebox.showinfo('Complete', 'Download is Complete')

    def on_closing(self):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = YoutubeDownloader()
    app.start()
