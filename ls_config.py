import os
WORKING_DIRECTORY = "/Users/noah/Convex/LikelihoodShape/"
def get_abspath(path):
    return WORKING_DIRECTORY + path

def get_cache_dir():
    return get_abspath("cache_dir")

def path_to_podcast(stem):
    directory = get_abspath("podcasts/")
    best_number = 0
    for number in range(1, 10000):
        if os.path.exists(directory + stem + f"_podcast{number}.wav"):
            best_number = number
        else:
            break
    if best_number == 0:
        raise FileNotFoundError(f"Could not find podcast {directory + stem + "_podcast1.wav"}")
    else:
        return directory + stem + f"_podcast{best_number}.wav"