"""
Uses a file which generates a history of played songs on spotify using
dunst's scripting tool to predict when a song has started playing and
when the song has finished to accurately record the song and save it
with the approrpiate data
"""
import sys
import os
import pyaudio
import wave
from pydub import AudioSegment
import music_tag
HISTORY_FILE = "/home/nzmichael118/.cache/spotify-history/songs"
MUSIC_DIR = "/home/nzmichael118/music"
MIN_SONG_LENGTH = 10

# Music data
sample_rate = 48000 # 160kbps (spotifys high setting)
chunk = 1024
sample_format = pyaudio.paInt16
channels = 2

pa = pyaudio.PyAudio()

dev_index = 4
 
def main():
    init_history_output = read_history()
    while init_history_output == read_history():
        pass
    print("first song of recording")
    history_ouptut = read_history()

    while True:
        record_song(history_ouptut[0], history_ouptut[1], history_ouptut[2])
        history_ouptut = read_history()


def record_song(track, artist, album):
    """records song and saves it and logs it"""
    stream = pa.open(format=sample_format,
                     channels=channels,
                     rate=sample_rate,
                     frames_per_buffer=chunk,
                     input=True,
                     )

    frames = []
    currently_playing = read_history()
    while currently_playing == (track, artist, album):
        data = stream.read(chunk)

        frames.append(data)
        currently_playing = read_history()
    print(f"Finished recording {track} - {album} by {artist}")
    # close stream stuff
    stream.stop_stream()
    stream.close()
    #pa.terminate()

    if not len(frames) < sample_rate / chunk * MIN_SONG_LENGTH:
        # Valid song length
        #save_dir = f"{MUSIC_DIR}/{artist}/{album}/{track}.wav"
        save_dir = f"{MUSIC_DIR}/{track} - {artist}.wav"
        save_dir_mp3 = f"{MUSIC_DIR}/{track} - {artist}.mp3"
        wf = wave.open(save_dir, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(pa.get_sample_size(sample_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        AudioSegment.from_wav(save_dir).export(save_dir_mp3, format="mp3")
        os.remove(save_dir)
        f = music_tag.load_file(save_dir_mp3)
        f["title"] = track
        f["album"] = album
        f["artist"] = artist
        f["albumartist"] = artist
    else:
        print("Too short of a song... Suspected skip")
        



def read_history():
    """Returns the last song played as followed (track, artist, album)"""
    with open(HISTORY_FILE, "r") as hf:
        for line in hf:
            pass
        # Skip the unneccesary lines
        last_line = line
        # track ; artist - album
        split = last_line.split(" ; ")
        track = split[0]
        split = split[1].split(" - ")
        artist = split[0]
        album = split[1]
        return(track, artist, album)



if __name__ == "__main__":
    main()
