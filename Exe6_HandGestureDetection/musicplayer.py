import os
import pygame

class MusicPlayer:
    def __init__(self):
        """Description of the __init__ function
             Set up initial data
        """
        self.playlist = []
        self.current_index = 0
        self.volume_step = 0.1
        self.add_songs_from_folder("playlist")

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.20)

    def add_songs_from_folder(self, folder_path):
        """Description of the __init__ function
             Set up initial data
             Parameters:
                 folder_path(String): Path to folder that contains songs
        """
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            music_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp3', '.wav'))]
            if music_files:
                for music_file in music_files:
                    file_path = os.path.join(folder_path, music_file)
                    self.playlist.append(file_path)
                    print(f"Song '{os.path.basename(file_path)}' added to the playlist.")
            else:
                print("No music files found.")
        else:
            print("Wrong folder path.")

    def play_song(self):
        """Description of the play_song function
             When called start playing song
        """
        if self.playlist:
            song_path = self.playlist[self.current_index]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            print(f"Song start!")
    def pause_song(self):
        """Description of the pause_song function
             When called stop playing song
        """
        pygame.mixer.music.pause()
        print(f"Song paused!")

    def play_next_song(self):
        """Description of the play_next_song function
             When called start playing next song from the playlist
        """
        if self.playlist:
            self.current_index += 1
            if self.current_index >= len(self.playlist):
                self.current_index = 0
            self.play_song()
            print(f"Next song!")

    def increase_volume(self):
        """Description of the increase_volume function
             When called increase volume of sounds
        """
        current_volume = pygame.mixer.music.get_volume()
        new_volume = min(1.0, current_volume + self.volume_step)
        pygame.mixer.music.set_volume(new_volume)
        print(f"Volume increased to {int(new_volume * 100)}%")

    def decrease_volume(self):
        """Description of the decrease_volume function
             When called decrease volume of sounds
        """
        current_volume = pygame.mixer.music.get_volume()
        new_volume = max(0.0, current_volume - self.volume_step)
        pygame.mixer.music.set_volume(new_volume)
        print(f"Volume decreased to {int(new_volume * 100)}%")