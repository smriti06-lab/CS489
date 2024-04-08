# Replicating an Immersive Sound System


## Overview

Develop a system capable of creating high-fidelity, three-dimensional sound, enhancing virtual reality experiences, and aiding in personalized audio delivery.

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

Work in progress

## Features

The GUI features include: 
- Select folder of songs you wish to play
- Be able to seek to next and previous songs in the music player
- Convert the song of your selection to 8D by adding panning, slow effect and reverb.
- Plot a waveform of the original song and the 8D audio to see a comparision.

## Acknowledgements

Work in progress

## Contact

-> Smriti Sharma (s462shar@uwaterloo.ca)
-> Tarun Velicheti (tveliche@uwaterloo.ca)
