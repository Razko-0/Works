import os
# Hide the pygame welcome message for a cleaner result
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

def play_music(folder, music_name):

    file_path = os.path.join(folder, music_name)
    if not os.path.exists(file_path):
        print("File not found.")
        return

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1) # -1 = Play in loop

    print(f"Now playing: {music_name}")
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
        
        elif command == "-":
            current_volume = pygame.mixer.music.get_volume()
            new_volume = max(0.0, current_volume - 0.10) # max is used so it can't be less than 0
            pygame.mixer.music.set_volume(new_volume)
            print(f"Volume down: {new_volume:.1f}") # :'.1f' is for decimals

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
    folder = "Music" # You can set any path where you have music stored
    mp3_files = [file for file in os.listdir(folder) if file.endswith(".mp3")]

# Errors
    if not os.path.isdir(folder):
        print(f"folder '{folder}' not found.")

    if not mp3_files:
        print("No music files found.")

# Loop
    while True:
        # Deco
        print("\n----- MUSIC PLAYER -----")
        print("  My titles:\n")
        # 2 possible arguments thanks to 'enumerate'; 'start' lets you start counting from 1
        for index, song in enumerate(mp3_files, start=1):
            print(f"{index}. {song}")

        choice_input = input("\nEnter the music index to play ('R' for random / 'Q' for quit):")

    # Errors
        # "upper" allows you to type in uppercase (so "q" and "Q" are accepted)
        if choice_input.upper() == "Q":
            break
        if choice_input.upper() == "R":
            choice_input = random.randint(1, len(mp3_files))

        elif not choice_input.isdigit():
            print("Please enter a valid number.")
            continue

    # Selection
        # Match the audio index
        choice = int(choice_input) - 1
        if 0 <= choice < len(mp3_files):
            play_music(folder, mp3_files[choice])
        else:
            print("Music index out of range !")
        

if __name__ == "__main__":
    main()
