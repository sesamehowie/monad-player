from src.utils.file_manager import FileManager
from src.modules.autoplayer import AutoPlayer


def main():
    file_manager = FileManager("data/private_keys.txt")
    private_keys = file_manager.open_file()
    autoplayer = AutoPlayer(private_keys)
    autoplayer.play_indefinitely()


if __name__ == "__main__":
    main()
