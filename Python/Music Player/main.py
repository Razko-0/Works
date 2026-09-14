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
    pygame.mixer.music.play()

    print(f"Now playing: {music_name}")
    print("Commands: [P]ause, [R]esume, [S]top")

    while True:
        command = input("> ").upper()

        if command == "P":
            pygame.mixer.music.pause()
            print("Paused")
        elif command == "R":
            pygame.mixer.music.unpause()
            print("Resumed")
        elif command == "S":
            pygame.mixer.music.stop()
            print("Stopped")
            return
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
        # 2 possible arguments thanks to 'enumerate'; 'start' lets you start counting from 1
        for index, song in enumerate(mp3_files, start=1):
            print(f"{index}. {song}")

        choice_input = input("\nEnter the music index to play ('Q' to quit):")

    # Errors
        if not choice_input.isdigit():
            print("Please enter a valid number.")
            continue

        # "upper" allows you to type in uppercase (so "q" and "Q" are accepted)
        if choice_input.upper() == "Q":
            break

    # Selection
        # Match the audio index
        choice = int(choice_input) - 1
        if 0 <= choice < len(mp3_files):
            play_music(folder, mp3_files[choice])
        else:
            print("Music index out of range !")
        

if __name__ == "__main__":
    main()
