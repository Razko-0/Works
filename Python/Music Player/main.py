import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import random

def play_music(folder, musics, index):

    file_path = os.path.join(folder, musics[index])
    if not os.path.exists(file_path):
        print("File not found.")
        return

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(0.50)
    pygame.mixer.music.play(-1) # -1 = play in loop

    print(f"Now playing: {musics[index]}")
    print("Commands: [-][+]Volume, res[T]art, [P]ause, [R]esume, [N]ext, [S]top")

    while True:
        command = input("> ").upper()

        if command == "T":
            pygame.mixer.music.rewind()
            print("Restarted")

        elif command == "P":
            pygame.mixer.music.pause()
            print("Paused")

        elif command == "R":
            pygame.mixer.music.unpause()
            print("Resumed")

        elif command == "S":
            pygame.mixer.music.stop()
            print("Stopped")
            return

        elif command == "N":
            pygame.mixer.music.stop()
            if index == len(musics) - 1:
                index = 0
            else:
                index += 1

            # Probably not optimized but it works
            file_path = os.path.join(folder, musics[index])
            if not os.path.exists(file_path):
                print("File not found.")
                return
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play(-1)

        elif command == "-":
            current_volume = pygame.mixer.music.get_volume()
            new_volume = max(0.0, current_volume - 0.10) # max is used so it can't be less than 0
            pygame.mixer.music.set_volume(new_volume)
            print(f"Volume down: {new_volume:.1f}")

        elif command == "+":
            current_volume = pygame.mixer.music.get_volume()
            new_volume = min(1.0, current_volume + 0.10) # min is used so it can't be higher than 1
            pygame.mixer.music.set_volume(new_volume)
            print(f"Volume up: {new_volume:.1f}")

        else:
            print("Invalid Command.")


def main():
# Init
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print("Audio initialization failed ! ", e)
        return

# Variables
    folder = "Music"
    mp3_files = [file for file in os.listdir(folder) if file.endswith(".mp3")]

# Errors
    if not os.path.isdir(folder):
        print(f"folder '{folder}' not found.")

    if not mp3_files:
        print("No music files found.")

# Loop
    while True:
        # Decoration
        print("\n----- MUSIC PLAYER -----")
        print("  My titles:\n")
        # 2 possible arguments thanks to `enumerate`; `start` lets you start counting from 1
        for index, song in enumerate(mp3_files, start=1):
            print(f"{index}. {song}")

        choice_input = input("\nEnter the music index to play ('R' for random / 'Q' for quit):")

    # Errors
        # "upper" lets you switch to uppercase (so "q" and "Q" are accepted)
        if choice_input.upper() == "Q":
            break
        if choice_input.upper() == "R":
            choice_input = random.randint(1, len(mp3_files))

        elif not choice_input.isdigit():
            print("Please enter a valid number.")
            continue

    # Selection
        # Match music index
        choice = int(choice_input) - 1

        # Play the music
        if 0 <= choice < len(mp3_files):
            play_music(folder, mp3_files, choice)
        else:
            print("Music index out of range !")


if __name__ == "__main__":
    main()
