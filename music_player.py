import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import customtkinter as ctk
from mutagen.mp3 import MP3
import threading
import pygame
import time
import os
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from audio_effects import loadSound, effect8d, effectSlowedDown, effectReverb, saveSound

# Initialize pygame mixer
pygame.mixer.init()

# Store the current position of the music
current_position = 0
paused = False
selected_folder_path = ""  # Store the selected folder path


def update_progress():
    global current_position
    while True:
        if pygame.mixer.music.get_busy() and not paused:
            current_position = pygame.mixer.music.get_pos() / 1000
            pbar["value"] = current_position

            # Check if the current song has reached its maximum duration
            if current_position >= pbar["maximum"]:
                stop_music()  # Stop the music playback
                pbar["value"] = 0  # Reset the pbar

            window.update()
        time.sleep(0.1)


# Create a thread to update the progress bar
pt = threading.Thread(target=update_progress)
pt.daemon = True
pt.start()


def select_music_folder():
    global selected_folder_path
    selected_folder_path = filedialog.askdirectory()
    if selected_folder_path:
        lbox.delete(0, tk.END)
        for filename in os.listdir(selected_folder_path):
            if filename.endswith(".mp3"):
                lbox.insert(tk.END, filename)  # Insert only the filename, not the full path


def previous_song():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index > 0:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(current_index - 1)
            play_selected_song()


def next_song():
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        if current_index < lbox.size() - 1:
            lbox.selection_clear(0, tk.END)
            lbox.selection_set(current_index + 1)
            play_selected_song()


def play_music():
    global paused
    if paused:
        # If the music is paused, unpause it
        pygame.mixer.music.unpause()
        paused = False
    else:
        # If the music is not paused, play the selected song
        play_selected_song()


def play_selected_song():
    global current_position, paused
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        selected_song = lbox.get(current_index)
        full_path = os.path.join(selected_folder_path, selected_song)  # Add the full path again
        pygame.mixer.music.load(full_path)  # Load the selected song
        pygame.mixer.music.play(start=current_position)  # Play the song from the current position
        paused = False
        audio = MP3(full_path)
        song_duration = audio.info.length
        pbar["maximum"] = song_duration  # Set the maximum value of the pbar  to the song duration


def pause_music():
    global paused
    # Pause the currently playing music
    pygame.mixer.music.pause()
    paused = True


def stop_music():
    global paused
    # Stop the currently playing music and reset the progress bar
    pygame.mixer.music.stop()
    paused = False


def update_song_list():
    global selected_folder_path
    if selected_folder_path:
        lbox.delete(0, tk.END)
        for filename in os.listdir(selected_folder_path):
            if filename.endswith(".mp3"):
                lbox.insert(tk.END, filename)


def convert_to_8d_audio():
    global selected_folder_path
    if len(lbox.curselection()) > 0:
        current_index = lbox.curselection()[0]
        selected_song = lbox.get(current_index)
        full_path = selected_folder_path + "/" + selected_song
        print(full_path)

        # Load the selected song
        sound = loadSound(full_path)

        # Apply the 8D audio effect
        sound_8d = effect8d(sound)
        sound_8d_slowed = effectSlowedDown(sound_8d)
        sound_8d_slowed_reverb, sr = effectReverb(sound_8d_slowed)

        # data1 = np.array(sound.get_array_of_samples())
        # data2 = np.array(sound_8d_slowed_reverb)
        # sample_rate = sound.frame_rate
        # plot_waveform_comparison(data1, data2, sample_rate=sample_rate)

        # Play the converted audio
        outpath = selected_folder_path + "/converted" + selected_song
        saveSound(sound_8d_slowed_reverb, sr, outpath)
        update_song_list()
        data1 = np.array(sound.get_array_of_samples())
        data2 = np.array(sound_8d_slowed_reverb)
        sample_rate = sound.frame_rate
        plot_waveform_comparison(data1, data2, sample_rate=sample_rate)


def plot_waveform_comparison(data1, data2, sample_rate, start_time =10, end_time = 20):
    # Determine start and end indices for selected portions
    start_index = int(start_time * sample_rate)
    end_index = int(end_time * sample_rate)

    # Plot selected portions of waveforms
    plt.figure(figsize=(10, 6))
    time = np.arange(start_index, end_index) / sample_rate
    plt.plot(time, data1[start_index:end_index], label='Regular Music', color='blue')
    plt.plot(time, data2[start_index:end_index], label='8D Music', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Comparison of Regular and 8D Music')
    plt.legend()
    # plt.show()
    plot_window = tk.Toplevel(window)
    plot_window.title('Waveform Comparison')
    plot_window.geometry('800x600')

    # Embed the plot into the Tkinter window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)


# Create the main window
window = tk.Tk()
window_icon = tk.PhotoImage(file="Images/1.png")
window.iconphoto(True, window_icon)
window.title("Music Player")
window.geometry("600x500")
window.configure(bg="#0D0D0D")  # Set background color to a dark shade

# Create a label for the music player title
l_music_player = tk.Label(window, text="Music Player", font=("Courier", 30, "bold"))
l_music_player.pack(pady=10)

# Create a button to select the music folder
btn_select_folder = ctk.CTkButton(window, text="Select Music Folder",
                                  command=select_music_folder,
                                  font=("Courier", 14))  # Set background and foreground color
btn_select_folder.pack(pady=20)

# Create a listbox to display the available songs
lbox = tk.Listbox(window, width=50, font=("Courier", 14), bg="#333", fg="#FFD700", selectbackground="#FFD700", selectforeground="#0D0D0D")
lbox.pack(pady=10)

# Create a frame to hold the control buttons
btn_frame = tk.Frame(window, bg="#0D0D0D")
btn_frame.pack(pady=20)

# Create a button to go to the previous song
btn_previous = ctk.CTkButton(btn_frame, text="<", command=previous_song,
                             width=6, font=("Courier", 14))
btn_previous.pack(side=tk.LEFT, padx=5)

# Create a button to play the music
btn_play = ctk.CTkButton(btn_frame, text="Play", command=play_music, width=6,
                         font=("Courier", 14))
btn_play.pack(side=tk.LEFT, padx=5)

# Create a button to pause the music
btn_pause = ctk.CTkButton(btn_frame, text="Pause", command=pause_music, width=6,
                          font=("Courier", 14))
btn_pause.pack(side=tk.LEFT, padx=5)

# Create a button to go to the next song
btn_next = ctk.CTkButton(btn_frame, text=">", command=next_song, width=6,
                         font=("Courier", 14))
btn_next.pack(side=tk.LEFT, padx=5)

# Create a button to convert the currently playing song to 8D audio and play it
btn_8d_audio = ctk.CTkButton(btn_frame, text="Convert to 8D Audio", command=convert_to_8d_audio, width=15,
                              font=("Courier", 14))
btn_8d_audio.pack(side=tk.LEFT, padx=5)

# Create a progress bar to indicate the current song's progress
pbar = Progressbar(window, length=300, mode="determinate", style="custom.Horizontal.TProgressbar")
pbar.pack(pady=10)

window.mainloop()
