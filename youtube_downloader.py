from tkinter import *
from tkinter import messagebox
import youtube_dl
from pytube import YouTube


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


# https://stackoverflow.com/questions/58662397/python-how-do-i-get-the-download-percentage-from-youtube-dl-when-im-downloading

BACKGROUND_COLOR = "#303030"
COLOR_1 = "#3796F6"
COLOR_2 = "#626262"

class YoutubeDownloader(Tk):

    def __init__(self):
        super(YoutubeDownloader, self).__init__()
        self.song_list_url = []
        self.song_list_name = []
        self.mode = "single_song"

        self.geometry("700x200")
        self.title('Youtube Downloader')
        self.configure(background=BACKGROUND_COLOR)
        # Mode
        frame_mode = Frame(self, background=BACKGROUND_COLOR)
        frame_mode.pack(pady=(10, 0))

        self.button_mode = Button(frame_mode, bd=0, background=BACKGROUND_COLOR,
                                  activebackground=BACKGROUND_COLOR,
                                  foreground=COLOR_1, text='Mode Song List : OFF', font=("Arial", 12),
                                  command=self.switch_mode)
        self.button_mode.pack()

        # Insert Url
        frame_insert_url = Frame(self, background=BACKGROUND_COLOR)
        frame_insert_url.pack(pady=(10, 30))
        label_insert_url = Label(frame_insert_url, text="Video url : ", bg=BACKGROUND_COLOR, foreground=COLOR_1,
                                 font=("Arial", 17))
        label_insert_url.grid(row=0, column=0)
        self.entry_insert_url = Entry(frame_insert_url, width=50, background=COLOR_2, foreground=COLOR_1,
                                      font=("Arial", 12))
        self.entry_insert_url.bind("<Button-1>", self.clear_input)
        self.entry_insert_url.grid(row=0, column=1)

        # Buttons
        frame_buttons = Frame(self, background=BACKGROUND_COLOR)
        frame_buttons.pack()
        # Download
        self.button_download_video = Button(frame_buttons, text="Download", bg=COLOR_2, foreground=COLOR_1,
                                            command=self.download, font=("Arial", 17), width=15, cursor="hand2")
        self.button_download_video.grid(row=0, column=0, padx=10)
        # ADD
        self.button_add_song = Button(frame_buttons, text="Add", bg=COLOR_2, foreground=COLOR_1,
                                      font=("Arial", 17), width=15, command=self.add, cursor="hand2")
        # Clear
        self.button_clear_song = Button(frame_buttons, text="Clear", bg=COLOR_2, foreground=COLOR_1,
                                        font=("Arial", 17), width=15, command=self.clear, cursor="hand2")
        # Show Section
        self.label_show = Label(self, text="", bg=BACKGROUND_COLOR, foreground=COLOR_1, font=("Arial", 10),
                                justify=LEFT)
        self.label_show.pack(pady=(15,5))

        #Bing Enter button
        self.bind('<Return>', self.call_def_with_enter)

    def check_url(self):
        checks = True
        url = self.entry_insert_url.get()
        if url == "":
            messagebox.showerror("Error", "You must provide a Youtube url")
            checks = False
        elif not (url.startswith('https://www.youtube.com/watch')):
            messagebox.showerror("Error", "Improper url")
            checks = False
        if checks:
            return True
        return False

    def download(self):
        if self.mode == "single_song":
            if self.check_url():
                try:
                    url = self.entry_insert_url.get()
                    download_as_mp3(url)
                    messagebox.showinfo('Complete', 'Download is Complete')
                except youtube_dl.utils.DownloadError:
                    messagebox.showerror("Error", "You must provide a url from Youtube")
                except:
                    messagebox.showerror("Error", "Something went wrong !")
        else:
            for url in self.song_list_url:
                try:
                    download_as_mp3(url)
                except youtube_dl.utils.DownloadError:
                    messagebox.showerror("Error", "You must provide a url from Youtube")
                except:
                    messagebox.showerror("Error", "Something went wrong !")
            messagebox.showinfo('Complete', 'Download is Complete')

    def add(self):
        if self.check_url():
            video_url = self.entry_insert_url.get()
            self.song_list_url.append(video_url)

            yt = YouTube(video_url)
            self.song_list_name.append(yt.title)
            text = ""
            for i in range(len(self.song_list_url)):
                text = text + str(i) + "  :  " + self.song_list_name[i] + "\n"
                text = text + "       " + self.song_list_url[i] + "\n" + "\n"
            self.label_show.config(text=text)
            self.geometry("700x"+str(200+(50*len(self.song_list_url))))

    def clear(self):
        self.song_list_url = []
        self.song_list_name = []
        self.label_show.config(text="")

    def switch_mode(self):
        if self.mode == "single_song":
            self.button_mode.config(text="Mode Song List : ON", font=("Arial", 12, "underline"))
            self.mode = "song_list"
            self.button_add_song.grid(row=0, column=1, padx=10)
            self.button_clear_song.grid(row=0, column=2, padx=10)
        else:
            self.button_mode.config(text="Mode Song List : OFF", font=("Arial", 12))
            self.mode = "single_song"
            self.button_add_song.grid_forget()
            self.button_clear_song.grid_forget()

    def switch_mode_to_song_list(self):
        self.mode = "song_list"
        self.button_mode_song_list.config(font=("Arial", 12, "underline"))
        self.button_mode_singe_song.config(font=("Arial", 12))

    def call_def_with_enter(self,e):
        if self.mode == "single_song":
            self.download()
        else:
            self.add()

    def clear_input(self, e):
        self.entry_insert_url.delete(0, END)

    def on_closing(self):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = YoutubeDownloader()
    app.start()
