import os
import requests
import sys

def count_words(url):
    response = requests.get(url)
    count = len(response.text.split(" "))
    print(f"There are {count} words at {url!r}.")

    proc = os.getpid()

    print(f"Processed {url} with process id: {proc}")

if __name__ == "__main__":
    count_words(sys.argv[1])