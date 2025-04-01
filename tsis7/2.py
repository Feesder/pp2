import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.music_folder = music_folder
        self.music_files = self.load_music_files()
        self.current_track = 0

    def load_music_files(self):
        return [file for file in os.listdir(self.music_folder) if file.endswith(('.mp3', '.ogg', '.wav'))]

    def play(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(self.music_folder, self.music_files[self.current_track]))
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.pause()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.current_track = (self.current_track + 1) % len(self.music_files)
        pygame.mixer.music.load(os.path.join(self.music_folder, self.music_files[self.current_track]))
        pygame.mixer.music.play()

    def previous(self):
        self.current_track = (self.current_track - 1) % len(self.music_files)
        pygame.mixer.music.load(os.path.join(self.music_folder, self.music_files[self.current_track]))
        pygame.mixer.music.play()


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Music Player With Keyboard Controls")

    music_player = MusicPlayer("music")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music_player.play()
                elif event.key == pygame.K_s:
                    music_player.stop()
                elif event.key == pygame.K_RIGHT:
                    music_player.next()
                elif event.key == pygame.K_LEFT:
                    music_player.previous()

    pygame.quit()

if __name__ == '__main__':
    main()