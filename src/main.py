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


# Standard taste profiles: each one has a clear "home" in the catalog
STANDARD_PROFILES = {
    # Late-night study listener: calm, mildly warm, acoustic-leaning background music
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "valence": 0.58,
        "likes_acoustic": True,
    },
    # Workout / party listener: loud, bright, polished pop
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "valence": 0.85,
        "likes_acoustic": False,
    },
    # Heavy listener: fast, aggressive, darker-sounding rock
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "valence": 0.40,
        "likes_acoustic": False,
    },
}

# Adversarial / edge-case profiles: designed to see if the scoring can be "tricked"
ADVERSARIAL_PROFILES = {
    # Conflicting prefs: wants high energy but a sad mood. The only sad song
    # in the catalog (Paper Boats) has energy 0.26.
    "Conflict: Energetic but Sad": {
        "genre": "folk",
        "mood": "sad",
        "energy": 0.90,
        "valence": 0.15,
        "likes_acoustic": True,
    },
    # Genre trap: asks for metal, but everything else describes a quiet, happy,
    # acoustic song. Does the +2.0 genre weight drag Iron Verdict to the top?
    "Trap: Calm Metal Fan": {
        "genre": "metal",
        "mood": "chill",
        "energy": 0.20,
        "valence": 0.80,
        "likes_acoustic": True,
    },
    # Genre/mood that don't exist in the catalog: categorical points can never fire
    "Ghost Genre: K-pop / Dreamy": {
        "genre": "k-pop",
        "mood": "dreamy",
        "energy": 0.60,
        "valence": 0.70,
        "likes_acoustic": False,
    },
    # Same intent as "Chill Lofi", but capitalized: exact string matching fails
    "Case Mismatch: 'LoFi' / 'Chill'": {
        "genre": "LoFi",
        "mood": "Chill",
        "energy": 0.38,
        "valence": 0.58,
        "likes_acoustic": True,
    },
    # Out-of-range numbers: energy/valence outside 0-1 can produce negative points
    "Out of Range: energy 1.8, valence -0.5": {
        "genre": "edm",
        "mood": "euphoric",
        "energy": 1.8,
        "valence": -0.5,
        "likes_acoustic": False,
    },
    # Empty profile: every key falls back to a default (energy 0.5, valence 0.5)
    "Empty Profile {}": {},
}


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Prints the top 5 songs for one profile as a table with explanations."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    header = f"{'#':<3}{'Title':<22}{'Artist':<16}{'Genre':<11}{'Mood':<10}{'Score':>6}"
    print(f"\n=== {name} ===")
    print(f"Prefs: {user_prefs}\n")
    print(header)
    print("-" * len(header))
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank:<3}{song['title']:<22}{song['artist']:<16}{song['genre']:<11}{song['mood']:<10}{score:>6.2f}")
        # Explanation sentence goes on its own indented line(s) under the row
        print(textwrap.fill(explanation, width=len(header), initial_indent="   ", subsequent_indent="   "))
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in {**STANDARD_PROFILES, **ADVERSARIAL_PROFILES}.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
