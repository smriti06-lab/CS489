# Replicating an Immersive Sound System


## Overview

Develop a system capable of creating high-fidelity, three-dimensional sound, enhancing virtual reality experiences, and aiding in personalized audio delivery.

![Logo](https://github.com/smriti06-lab/CS489/blob/main/Images/repooverview.gif)

## Problem statement

Upon extensive research, we found that modern solutions fall short in delivering authentic 3D auditory experiences without resorting to elaborate multi-speaker arrangements, which can be intrusive and expensive. The goal is to transcend these constraints by harnessing artificial intelligence to create a more organic and enveloping soundscape.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Installation

The project requires:
  1) Python v 3.10 and above
  2) `pip` (python package installation)
  3) [ffmpeg](https://ffmpeg.org/about.html)

[ffmpeg installation guide](https://windowsloop.com/install-ffmpeg-windows-10/)<br />
`ffmpeg` is a universal media converter. It can read a wide variety of inputs - including live grabbing/recording devices - filter, and transcode them into a plethora of output formats.
It is crucial to make sure that `ffmpeg` is properly installed for the project to run.

Once you have `ffmpeg` installed, make sure the following libraries are installed using `pip` (`pip install <library>`):
- `tkinkter` : Generates a GUI for the music player
- `customtkinter` : Provides UI components used in the GUI
- `mutagen` : Use to process `mp3` format files
- `pygame` : Used to perform operations in the GUI and play music through the GUI
- `numpy` : Used in signal processing
- `matplotlib` : Used in plotting the waveforms
- `pydub` : Used in audio file processing
- `soundfile` : Used in audio file processing (has functions absent in pydub)
- `pedalboard` : Used to add effects to the audio files.

## Usage

The program files that generate the GUI and conver the audio are `audio_effects.py` and `music_player.py`. The `gen8d.ipynb` is our initial project file we developed for testing on Google colab but switched to Python because GUIs are not compatible on google colab.

- Clone the repository in the folder of your choice and open the project using the IDE of your choice.
- Installation guide in the above section has all the libraries nedded to run the app.
- run the command `python music_player.py` for the GUI to pop up and select the Music folder in the GUI pop up to use the app!

  [Youtube Link](https://www.youtube.com/watch?v=CbPVmHjnqx4)


## Features

The GUI features include: 
- Select folder of songs you wish to play
- Be able to seek to next and previous songs in the music player
- Convert the song of your selection to 8D by adding panning, slow effect and reverb.
- Plot a waveform of the original song and the 8D audio to see a comparision.

## Acknowledgements

We would like to thank Prof. Richard Mann for giving us a chance and for mentoring us throughout the project timeline. His feedbacks on our progress and submissions gave us much needed insights into shaping the project and the report.

## Contact

- Smriti Sharma (s462shar@uwaterloo.ca)
- Tarun Velicheti (tveliche@uwaterloo.ca)
