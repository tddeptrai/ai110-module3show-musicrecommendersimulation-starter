"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: a late-night study listener who wants calm,
    # mildly warm, acoustic-leaning background music
    user_prefs = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "valence": 0.58,
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    header = f"{'#':<3}{'Title':<22}{'Artist':<16}{'Genre':<11}{'Mood':<10}{'Score':>6}"
    print(header)
    print("-" * len(header))
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank:<3}{song['title']:<22}{song['artist']:<16}{song['genre']:<11}{song['mood']:<10}{score:>6.2f}")
        # Explanation sentence goes on its own indented line(s) under the row
        print(textwrap.fill(explanation, width=len(header), initial_indent="   ", subsequent_indent="   "))
        print()


if __name__ == "__main__":
    main()
