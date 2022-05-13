from tkinter import *
from tkinter import messagebox
import youtube_dl
from pytube import YouTube
from tkinter import ttk


def download_as_mp3(video_url, video_title):
    video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
    filename = video_title + ".mp3"
    options = {
        'format': 'bestaudio/best',
        'keepvideo': False,
        'outtmpl': filename,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    print("Download complete... {}".format(filename))


def get_video_name(url):
    yt = YouTube(url)
    return yt.title


def check_url(url):
    checks = True
    if url == "":
        messagebox.showerror("Error", "You must provide a Youtube url")
        checks = False
    elif not (url.startswith('https://www.youtube.com/watch')):
        messagebox.showerror("Error", "Improper url")
        checks = False
    if checks:
        return True
    return False


BACKGROUND_COLOR = "#303030"
COLOR_1 = "#3796F6"
COLOR_2 = "#626262"


class YoutubeDownloader(Tk):
    def __init__(self):
        super(YoutubeDownloader, self).__init__()
        self.song_list_url = []
        self.song_list_name = []
        self.song_list_labels = []
        self.mode = "single_song"
        self.count_of_songs = 0

        self.geometry("700x250")
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
        frame_buttons.pack(pady=(0, 15))
        # Download
        self.button_download_video = Button(frame_buttons, text="Download", bg=COLOR_2, foreground=COLOR_1,
                                            command=self.download, font=("Arial", 17), width=15, cursor="hand2")
        self.button_download_video.grid(row=0, columnspan=2, pady=(0, 10))
        # ADD
        self.button_add_song = Button(frame_buttons, text="Add", bg=COLOR_2, foreground=COLOR_1,
                                      font=("Arial", 17), width=15, command=self.add, cursor="hand2")
        # Clear
        self.button_clear_song = Button(frame_buttons, text="Clear", bg=COLOR_2, foreground=COLOR_1,
                                        font=("Arial", 17), width=15, command=self.clear, cursor="hand2")
        # Progress Bar
        frame_download_progress_bar = Frame(self, background=BACKGROUND_COLOR)
        frame_download_progress_bar.pack()
        self.progress_bar_download_progress = ttk.Progressbar(frame_download_progress_bar, orient=HORIZONTAL,
                                                              length=500,
                                                              mode="determinate")
        self.label_download_progress_percentage = Label(frame_download_progress_bar, text="0%",
                                                        background=BACKGROUND_COLOR, foreground=COLOR_1,
                                                        font=("Arial", 12))

        # Show song_list
        self.frame_song_list = Frame(self, bg=BACKGROUND_COLOR)

        # Bing Enter button
        self.bind('<Return>', self.call_def_with_enter)

        self.label_progress = Label(self, text="", bg=BACKGROUND_COLOR, foreground=COLOR_1,
                                    font=("Arial", 17))
        self.label_progress.pack()

    def add_song_label(self, text):
        label = Label(self.frame_song_list, text=text, bg=BACKGROUND_COLOR, foreground=COLOR_1, font=("Arial", 10),
                      justify=LEFT)
        label.pack(pady=5, anchor="w", padx=(50, 0))
        self.song_list_labels.append(label)
        number = len(self.song_list_labels) - 1
        label.bind("<Button-1>", lambda event: self.remove_url(number))
        self.geometry("700x" + str(250 + (60 * self.count_of_songs)))

    def download(self):
        if self.mode == "single_song":
            self.label_progress.config(text="Please wait...")
            self.label_progress.update()
            url = self.entry_insert_url.get()
            if check_url(url):
                try:
                    download_as_mp3(url, get_video_name(url))
                    self.entry_insert_url.delete(0, END)
                    self.label_progress.config(text="")
                    self.label_progress.update()
                    messagebox.showinfo('Complete', 'Download is Complete')
                except youtube_dl.utils.DownloadError:
                    self.label_progress.config(text="")
                    self.label_progress.update()
                    messagebox.showerror("Error", "You must provide a url from Youtube")
                except:
                    self.label_progress.config(text="")
                    self.label_progress.update()
                    messagebox.showerror("Error", "Something went wrong !")
                # ERROR: unable to download video data: HTTP Error 403: Forbidden
        else:
            self.progress_bar_download_progress.pack()
            self.label_download_progress_percentage.pack(padx=5, pady=1, side="right")

            error = False
            downloaded_urls = 0
            for url in self.song_list_url:
                if url != "x":
                    if check_url(url):
                        try:
                            download_as_mp3(url, get_video_name(url))
                            downloaded_urls = downloaded_urls + 1
                            self.update_progress_bar(downloaded_urls)

                        except youtube_dl.utils.DownloadError:
                            messagebox.showerror("Error", "You must provide a url from Youtube")
                            error = True
                        except:
                            error = True
                            messagebox.showerror("Error", "Something went wrong !")
            if not error:
                messagebox.showinfo('Complete', 'Download is Complete')
            elif downloaded_urls < self.count_of_songs:
                messagebox.showerror("Error", f"{downloaded_urls} out of {self.count_of_songs} were Downloaded")

    def add(self):
        video_url = self.entry_insert_url.get()
        if check_url(video_url):
            self.count_of_songs = self.count_of_songs + 1
            self.song_list_url.append(video_url)
            self.song_list_name.append(get_video_name(video_url))
            text = str(self.count_of_songs) + "  :  " + get_video_name(video_url) + "\n" + "       " + video_url
            self.add_song_label(text)

    def clear(self):
        self.song_list_url = []
        self.song_list_name = []
        for label in self.song_list_labels:
            label.pack_forget()
        self.song_list_labels = []
        self.geometry("700x250")

    def update_progress_bar(self, number):
        num = (number * 100) / self.count_of_songs
        self.progress_bar_download_progress["value"] = round(num, 2)
        self.progress_bar_download_progress.update()
        self.label_download_progress_percentage.config(text=str(round(num, 2)) + "%")
        self.label_download_progress_percentage.update()

    def switch_mode(self):
        if self.mode == "single_song":
            self.button_mode.config(text="Mode Song List : ON", font=("Arial", 12, "underline"))
            self.mode = "song_list"
            self.button_add_song.grid(row=1, column=0, padx=10)
            self.button_clear_song.grid(row=1, column=1, padx=10)
            self.frame_song_list.pack(fill=BOTH, pady=(0, 10))
        else:
            self.button_mode.config(text="Mode Song List : OFF", font=("Arial", 12))
            self.mode = "single_song"
            self.button_add_song.grid_forget()
            self.button_clear_song.grid_forget()
            self.frame_song_list.pack_forget()

    def call_def_with_enter(self, e):
        if self.mode == "single_song":
            self.download()
        else:
            self.add()

    def clear_input(self, e):
        self.entry_insert_url.delete(0, END)

    def remove_url(self, number_of_url):
        number_of_url = int(number_of_url)
        print(number_of_url)
        if len(self.song_list_labels) > 0:
            self.count_of_songs = self.count_of_songs - 1
            self.song_list_labels[number_of_url].pack_forget()
            self.geometry("700x" + str(250 + (50 * self.count_of_songs)))
            self.song_list_url[number_of_url] = "x"
            self.song_list_name[number_of_url] = "x"
            for x in self.song_list_name:
                print(x)

    def on_closing(self):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = YoutubeDownloader()
    app.start()
