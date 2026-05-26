import os
WORKING_DIRECTORY = "/Users/noah/Convex/LikelihoodShape/"
def get_abspath(path):
    return WORKING_DIRECTORY + path

def get_cache_dir():
    return get_abspath("cache_dir")

def path_to_podcast(stem : str, make_new : bool = False):
    """Return the path to the highest-numbered podcast WAV file matching the given stem.

    Scans the podcasts/ directory for files named ``<stem>_podcast<N>.wav`` and
    returns the one with the largest consecutive N starting from 1.

    Args:
        stem: Base name prefix for the podcast files (e.g. ``"episode1"`` matches
              ``episode1_podcast1.wav``, ``episode1_podcast2.wav``, etc.).
        make_new: If True, returns the lowest unoccupied number for podcasts. If False, returns
          the highest contiguous occupied number for podcasts.

    Returns:
        Absolute path to the highest-numbered matching WAV file.

    Raises:
        FileNotFoundError: If no matching file is found (i.e. ``<stem>_podcast1.wav``
                           does not exist).
    """
    directory = get_abspath("podcasts/")
    best_number = 0
    for number in range(1, 10000):
        if os.path.exists(directory + stem + f"_podcast{number}.wav"):
            best_number = number
        else:
            break
    best_number += make_new # If we're making a new podcast, we go 1 higher than the highest podcast number we found

    if best_number == 0:
        raise FileNotFoundError(f"Could not find podcast {directory + stem + "_podcast1.wav"}")
    else:
        return directory + stem + f"_podcast{best_number}.wav"