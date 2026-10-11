import os
import pygame


def init_music(folder, musics, index, volume): # init
    file_path = os.path.join(folder, musics[index])

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1) # -1 = play in loop
    pygame.mixer.music.pause()

def change_music(folder, musics, index, volume): # next / previous (index change in main loop)
    pygame.mixer.music.unload()
    init_music(folder, musics, index, volume)
    play(musics, index)

def pause(musics, index):
    pygame.mixer.music.pause()
    print(f"[PAUSED] {musics[index]}")

def play(musics, index):
    pygame.mixer.music.unpause()
    print(f"Now Playing: {musics[index]}")

def display_text(screen, text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


class Sliders:
    def __init__(self, pos, size, init_val, minimum, maximum, images):
        self.left_pos = pos[0] - (size[0]//2)
        self.right_pos = pos[0] + (size[0]//2)
        self.top_pos = pos[1] - (size[1]//2)
        self.min = minimum
        self.max = maximum

        self.init_val = (self.right_pos - self.left_pos)*init_val # percentage


        self.container_image = pygame.image.load(f"{images}/container.png").convert()
        self.container_image.set_colorkey((255,255,255))
        self.container_rect = self.container_image.get_rect(topleft=(self.left_pos, self.top_pos))
        
        self.button_image = pygame.image.load(f"{images}/slider.png").convert()
        self.button_image.set_colorkey((255,255,255))
        self.button_rect = self.button_image.get_rect(topleft=(self.container_rect.centerx - 10, self.top_pos-5))

    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

    def render(self, screen):
        screen.blit(self.container_image, self.container_rect)
        screen.blit(self.button_image, self.button_rect)

    def get_val(self):
        val_range = self.right_pos - self.left_pos - 1 # -1 = the padding so we can get to 100%
        button_val = self.button_rect.centerx - self.left_pos
        return (button_val/val_range)*(self.max-self.min)+self.min # percentage * range + offset
    

def main():
# Init
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print("Audio initialization failed ! ", e)
        return
            
    pygame.display.set_caption("Music Player")
    screen = pygame.display.set_mode((720, 720))

# Variables
    folder = "/path/to/music/foler" 
    images = "path/to/textures/folder" 
    mp3_files = [file for file in os.listdir(folder) if file.endswith(".mp3")]
    index = 11 # change later
    volume = 0.5 # initial volume

    sliders = [
        Sliders((350, 620), (300, 50), volume, 0, 1, images) # Coords, Size, init_value, min, max
    ]

# Errors
    if not os.path.isdir(folder):
        print(f"folder '{folder}' not found.")

    if not mp3_files:
        print("No music files found.")

# Init music
    init_music(folder, mp3_files, index, volume)

# GUI
    # play
    play_image = pygame.image.load(f"{images}/play.png").convert()
    play_image.set_colorkey((255,255,255))
    play_rect = play_image.get_rect(topleft=(360, 500))
    # pause
    pause_image = pygame.image.load(f"{images}/pause.png").convert()
    pause_image.set_colorkey((255,255,255))
    pause_rect = pause_image.get_rect(topleft=(280, 500))
    # next
    next_image = pygame.image.load(f"{images}/next.png").convert()
    next_image.set_colorkey((255,255,255))
    next_rect = next_image.get_rect(topleft=(440, 500))
    # previous
    prev_image = pygame.image.load(f"{images}/previous.png").convert()
    prev_image.set_colorkey((255,255,255))
    prev_rect = prev_image.get_rect(topleft=(200, 500))

# Loop
    running = True
    while running:

        # mouse
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        # init
        screen.fill("black")

        # GUI
        screen.blit(play_image, play_rect)
        screen.blit(pause_image, pause_rect)
        screen.blit(next_image, next_rect)
        screen.blit(prev_image, prev_rect)

        for slider in sliders:
            if slider.container_rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                slider.move_slider(mouse_pos)
            print(round(slider.get_val(), 2))
            pygame.mixer.music.set_volume(slider.get_val())
            slider.render(screen)

        # Texts
        display_text(screen, "-", pygame.font.SysFont("Arial", 50), (255, 255, 255), 170, 585)
        display_text(screen, "+", pygame.font.SysFont("Arial", 50), (255, 255, 255), 510, 585)
        display_text(screen, f"Now playing: {mp3_files[index]}", pygame.font.SysFont("Arial", 30), (255, 255, 255), 170, 450)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                print("Closing app.")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    play(mp3_files, index)
                if pause_rect.collidepoint(event.pos):
                    pause(mp3_files, index)
                if next_rect.collidepoint(event.pos):
                    if index == len(mp3_files) - 1:
                        index = 0
                    else:
                        index += 1
                    change_music(folder, mp3_files, index, pygame.mixer.music.get_volume())
                if prev_rect.collidepoint(event.pos):
                    if index == 0:
                        index = len(mp3_files) - 1
                    else:
                        index -= 1
                    change_music(folder, mp3_files, index, pygame.mixer.music.get_volume())

if __name__ == "__main__":
    main()
