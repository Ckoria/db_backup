from login import download_file
import time

if __name__ == "__main__":
    while True:
        download_file()
        time.sleep(3600 * 5)