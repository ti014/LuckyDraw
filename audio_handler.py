from pygame import mixer
from gtts import gTTS
import pygame
import os

class AudioHandler:
    def __init__(self, root=None):
        self.root = root
        mixer.init()
        self.background_music = None

    def setup_audio(self):
        """Setup background music"""
        try:
            self.background_music = mixer.Sound("audio/music_background.mp3")
            self.background_music.set_volume(1.0)
            print("Background music loaded successfully.")
        except Exception as e:
            print(f"Error loading background music: {e}")

    def play_background_music(self):
        """Play the background music"""
        try:
            self.background_music.set_volume(0.9)
            self.background_music.play(loops=-1)
            print("Background music started.")
        except Exception as e:
            print(f"Error playing background music: {e}")

    def stop_background_music(self):
        """Stop the background music"""
        try:
            self.background_music.stop()
        except:
            pass

    def reduce_volume(self):
        """Gradually reduce the volume of the background music"""
        current_volume = self.background_music.get_volume()
        if current_volume > 0:
            new_volume = max(0, current_volume - 0.1)
            self.background_music.set_volume(new_volume)
            if self.root:
                self.root.after(300, self.reduce_volume)
        else:
            self.background_music.stop()

    def cleanup_winner_audio(self):
        """Ensure winner.mp3 is closed before next round"""
        try:
            if os.path.exists("winner.mp3"):
                os.remove("winner.mp3")
        except Exception as e:
            print(f"Error cleaning up winner.mp3: {e}")

    def fade_out(self, sound, duration=3000):
        """Gradually decrease volume and stop the sound"""
        for i in range(10, -1, -1):
            sound.set_volume(i / 10)
            pygame.time.wait(duration // 10)
        sound.stop()

    def announce_winner(self, winner):
        """Announce the winner using text-to-speech"""
        message_text = f"Xin chúc mừng {winner['Name']} - {winner['Group']} - {winner['Department']} ĐÃ GIÀNH CHIẾN THẮNG."
        tts = gTTS(text=message_text, lang='vi')
        try:
            if os.path.exists("winner.mp3"):
                os.remove("winner.mp3")
            tts.save("winner.mp3")
            mixer.music.load("winner.mp3")
            mixer.music.set_volume(1.0)  # Set volume to maximum
            mixer.music.play()
        except Exception as e:
            print(f"Error announcing winner: {e}")
        while mixer.music.get_busy():
            pygame.time.wait(10)
        mixer.music.unload()
        os.remove("winner.mp3")
