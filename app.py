import tkinter as tk
import os
from pygame import mixer
from tinytag import TinyTag
from threading import Timer


class Player(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        mixer.init()

        self.browser_window = 1
        self.playlist = []
        self.current_song = 0
        self.pause = True
        self.timer = None

        self.create_frames()
        self.taskbar()
        self.browser()
        self.current()

    def create_frames(self):
        self.taskbar_frame = tk.LabelFrame(self, bg="black", borderwidth=0, highlightthickness=0, padx=0, pady=0)
        self.taskbar_frame.config(width=296, height=50)
        self.taskbar_frame.grid(row=0, column=0, sticky='nsew')

        self.browser_frame = tk.LabelFrame(self, bg="grey", borderwidth=0, highlightthickness=0)
        self.browser_frame.config(width=296, height=400)
        self.browser_frame.grid(row=1, column=0)

        self.current_frame = tk.LabelFrame(self, bg="red", borderwidth=0, highlightthickness=0)
        self.current_frame.config(width=296, height=50)
        self.current_frame.grid(row=2, column=0)

    def taskbar(self):
        home = tk.Button(self.taskbar_frame, text="Home", borderwidth=0, highlightthickness=0, height=3, width=10)
        track = tk.Button(self.taskbar_frame, text="Track", borderwidth=0, highlightthickness=0, height=3, width=10)
        album = tk.Button(self.taskbar_frame, text="album", borderwidth=0, highlightthickness=0, height=3, width=10)
        artist = tk.Button(self.taskbar_frame, text="artist", borderwidth=0, highlightthickness=0, height=3, width=10)

        home.grid(row=0, column=0, sticky="nw")
        track.grid(row=0, column=1, sticky="n")
        album.grid(row=0, column=2, sticky="n")
        artist.grid(row=0, column=3, sticky="ne")

    def browser(self):
        if self.browser_window == 0:
            pass
        elif self.browser_window == 1:
            track_list_scrollbar = tk.Scrollbar(self.browser_frame, borderwidth=0, highlightthickness=0, orient=tk.VERTICAL, width=14)

            self.track_list = tk.Listbox(self.browser_frame, height=25, width=47, borderwidth=0, highlightthickness=0, yscrollcommand=track_list_scrollbar.set)
            self.track_list.grid(row=0, column=0)

            track_list_scrollbar.config(command=self.track_list.yview)
            track_list_scrollbar.grid(row=0, column=1, sticky='ns')
            
            self.retrieve_songs()

            self.track_list.bind('<<ListboxSelect>>', self.play_song)

    def play_song(self, event = None):
        self.pause = False

        if event == None: 
            self.timer.cancel() 
            self.current(self.playlist[self.current_song])
            mixer.music.load(self.playlist[self.current_song]['dirpath'])
            mixer.music.play()

            self.timer = Timer(self.playlist[self.current_song]['duration'] + 1, self.next_song)
            self.timer.start()
        else:  
            if self.timer != None:
                self.timer.cancel()

            self.current_song = self.track_list.curselection()[0]
            title = self.track_list.get(self.track_list.curselection())
            
            for song in self.playlist:
                if song['title'] == title:
                    self.current(song)

                    mixer.music.load(song['dirpath'])
                    mixer.music.play()

                    self.timer = Timer(song['duration'] + 1, self.next_song)
                    self.timer.start()           

    def retrieve_songs(self):
        directory = 'C:/Users/setuk/Music'

        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith('.mp3') or filename.endswith('.flac'):
                    metadata = TinyTag.get(dirpath + '/' + filename)
                    self.playlist.append({
                        'dirpath': dirpath + '/' + filename,
                        'title': metadata.title,
                        'artist': metadata.artist,
                        'duration': metadata.duration
                    })

                    self.track_list.insert('end', metadata.title)

    def current(self, song_data = None):
        song = 'Song'
        artist = 'Artist'

        if song_data != None:
            if len(song_data['title']) > 23:
                song = song_data['title'][:20] + '...'
            else:
                song = song_data['title']
            artist = song_data['artist']

        current_song_label = tk.Label(self.current_frame, text=song, font=("Arial", 12))
        current_artist_label = tk.Label(self.current_frame, text=artist, font=("Arial", 7))
        play_btn = tk.Button(self.current_frame, text='play', command=self.play_pause)
        pre_btn = tk.Button(self.current_frame, text='pre', command=self.pre_song)
        next_btn = tk.Button(self.current_frame, text='nxt', command=self.next_song)

        current_song_label.grid(row=0, column=0, sticky='w')
        current_artist_label.grid(row=1, column=0, sticky='w')
        play_btn.grid(row=0, column=2)
        pre_btn.grid(row=0, column=1)
        next_btn.grid(row=0, column=3)

    def next_song(self):
        self.current_song = self.current_song + 1
        self.play_song()

    def pre_song(self):
        self.current_song = self.current_song - 1
        self.play_song()

    def play_pause(self):
        if self.pause == True:
            self.pause = False
            mixer.music.unpause()
        else:
            self.pause = True
            mixer.music.pause()    


root = tk.Tk()
root.geometry('296x500')
root.wm_title('Suno')
# root.resizable(False, False)

app = Player(root)
app.mainloop()