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
import librosa

from audio_effects import loadSound, effect8d, effectSlowedDown, effectReverb, saveSound

# Initialize pygame mixer
pygame.mixer.init()

# Store the current position of the music
current_position = 0
paused = False
selected_folder_path = ""  # Store the selected folder path
analysis_directory = "Analysis/"


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

        # Play the converted audio
        outpath = selected_folder_path + "/converted" + selected_song
        saveSound(sound_8d_slowed_reverb, sr, outpath)
        update_song_list()

        # Waveform comparison
        data1 = np.array(sound.get_array_of_samples())
        converted_sound = loadSound(outpath)
        data2 = np.array(converted_sound.get_array_of_samples())
        sample_rate = sound.frame_rate
        plot_waveform_comparison(data1, data2, sample_rate=sample_rate)

        # Frequency Spectrum and Energy Density
        plot_spectrum_and_envelope(data1, data2, sample_rate, "Compare Regular and 8D Music")

        # Plotting MFCCs
        mfccs_regular = compute_mfcc(sound)
        mfccs_8d = compute_mfcc(converted_sound)
        plot_mfccs(mfccs_regular, mfccs_8d, "MFCC Comparison - Regular cs. 8D Music")


def plot_waveform_comparison(data1, data2, sample_rate, start_time =10, end_time = 20):
    # Determine start and end indices for selected portions
    start_index = int(start_time * sample_rate)
    end_index = int(end_time * sample_rate)

    # Plot selected portions of waveforms
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(start_index, end_index) / sample_rate, data1[start_index:end_index], label='Regular Music', color='blue')
    plt.plot(np.arange(start_index, end_index) / sample_rate, data2[start_index:end_index], label='8D Music', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Comparison of Regular and 8D Music')
    plt.legend()
    # plt.show()
    plot_window = tk.Toplevel(window)
    plot_window.title('Waveform Comparison')
    plot_window.geometry('800x600')
    plot_filename = analysis_directory + 'waveform_comparison.png'
    plt.savefig(plot_filename)

    # Embed the plot into the Tkinter window
    # canvas = FigureCanvasTkAgg(plt.gcf(), master=plot_window)
    # canvas.draw()
    # canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)


# Function to plot frequency spectrum and energy envelope
def plot_spectrum_and_envelope(data1, data2, sample_rate, title):
    # Extract data and sample rate from sounds
    # data1 = np.array(sound1.get_array_of_samples())
    # data2 = np.array(sound2.get_array_of_samples())
    # sample_rate = sound1.frame_rate

    # Calculate frequency spectrum and energy envelope
    frequencies1, spectrum1 = plt.psd(data1, Fs=sample_rate)
    envelope1 = np.abs(data1)
    frequencies2, spectrum2 = plt.psd(data2, Fs=sample_rate)
    envelope2 = np.abs(data2)

    # Plot frequency spectrum and energy envelope
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(frequencies1, 10 * np.log10(spectrum1), label='Regular Music', color='blue')
    plt.plot(frequencies2, 10 * np.log10(spectrum2), label='8D Music', color='red')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.title('Frequency Spectrum Comparison')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(np.arange(len(data2)) / sample_rate, envelope2, label='8D Music', color='red')
    plt.plot(np.arange(len(data1)) / sample_rate, envelope1, label='Regular Music', color='blue')

    plt.xlabel('Time (s)')
    plt.ylabel('Energy')
    plt.title('Energy Envelope Comparison')
    plt.legend()
    plot_filename = analysis_directory + "freq_energy_env.png"

    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(plot_filename)


def compute_mfcc(sound):
    # Convert audio signal to a numpy array with floating-point values for processing
    data = np.array(sound.get_array_of_samples(), dtype=np.float32)

    # Retrieve the sampling rate from the sound object, which is necessary for MFCC calculation
    sample_rate = sound.frame_rate

    # Compute the MFCCs using librosa's feature.mfcc function, which extracts
    # the Mel Frequency Cepstral Coefficients representing the sound
    mfccs = librosa.feature.mfcc(y=data, sr=sample_rate, n_mfcc=13)

    # Return the computed MFCCs back to the caller
    return mfccs


def plot_mfccs(mfccs1, mfccs2, title):
    # Set up the figure size for the plots
    plt.figure(figsize=(10, 6))

    # Plot the MFCCs for the first sound (e.g., regular music)
    # It uses a subplot for multi-part figures - in this case, 2 rows by 1 column, 1st position
    plt.subplot(2, 1, 1)

    # Display the MFCCs as a heatmap using librosa's specshow function
    librosa.display.specshow(mfccs1, x_axis='time')

    # Include a colorbar to indicate the scale
    plt.colorbar()

    # Title for the first MFCC plot (regular music)
    plt.title('MFCCs - Regular Music')

    # Plot the MFCCs for the second sound (e.g., 8D music)
    # Similar layout as the first, but in the 2nd position
    plt.subplot(2, 1, 2)
    librosa.display.specshow(mfccs2, x_axis='time')
    plt.colorbar()

    # Title for the second MFCC plot (8D music)
    plt.title('MFCCs - 8D Music')

    # Set an overall title for the combined figure
    plt.suptitle(title)

    # Adjust the layout so everything fits without overlapping
    plt.tight_layout()
    plot_path = analysis_directory + "mfcc.png"
    plt.savefig(plot_path)  # Or use .jpg, .pdf, etc.


# -------------------------------------------- GUI CODE --------------------------------------------

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
