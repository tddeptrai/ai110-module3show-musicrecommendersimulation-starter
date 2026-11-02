import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: float = 0.5

# Scoring weights (max possible score = 6.0)
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.5
VALENCE_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for the user, ranked by score from highest to lowest."""
        prefs = _profile_to_prefs(user)
        ranked = sorted(self.songs, key=lambda song: score_song(prefs, asdict(song))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a plain-English sentence explaining why the song fits the user."""
        return explain_song(_profile_to_prefs(user), asdict(song))

def _profile_to_prefs(user: UserProfile) -> Dict:
    """Converts a UserProfile into the dict format score_song expects."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "valence": user.target_valence,
        "likes_acoustic": user.likes_acoustic,
    }

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += GENRE_WEIGHT
        reasons.append(f"genre matches ({song['genre']}) +{GENRE_WEIGHT:.2f}")

    if song["mood"] == user_prefs.get("mood"):
        score += MOOD_WEIGHT
        reasons.append(f"mood matches ({song['mood']}) +{MOOD_WEIGHT:.2f}")

    # Closeness: 1.0 when the song hits the target exactly, 0.0 when it's as far as possible
    energy_points = ENERGY_WEIGHT * (1 - abs(song["energy"] - user_prefs.get("energy", 0.5)))
    score += energy_points
    reasons.append(f"energy {song['energy']:.2f} is close to target +{energy_points:.2f}")

    valence_points = VALENCE_WEIGHT * (1 - abs(song["valence"] - user_prefs.get("valence", 0.5)))
    score += valence_points
    reasons.append(f"valence {song['valence']:.2f} is close to target +{valence_points:.2f}")

    if user_prefs.get("likes_acoustic"):
        acoustic_points = ACOUSTIC_WEIGHT * song["acousticness"]
        score += acoustic_points
        reasons.append(f"acousticness {song['acousticness']:.2f} +{acoustic_points:.2f}")

    return score, reasons

def _join_phrases(phrases: List[str]) -> str:
    """Joins phrases as "a", "a and b", or "a, b, and c"."""
    if len(phrases) <= 2:
        return " and ".join(phrases)
    return ", ".join(phrases[:-1]) + ", and " + phrases[-1]

def explain_song(user_prefs: Dict, song: Dict) -> str:
    """Describes in plain sentences why a song does or doesn't fit the user's taste."""
    matches = []
    drawbacks = []

    if song["genre"] == user_prefs.get("genre"):
        matches.append(f"it's a {song['genre']} song (your favorite genre)")
    if song["mood"] == user_prefs.get("mood"):
        matches.append(f"it has the {song['mood']} mood you're looking for")

    energy_gap = song["energy"] - user_prefs.get("energy", 0.5)
    if abs(energy_gap) <= 0.1:
        matches.append("its energy level is right where you like it")
    elif abs(energy_gap) <= 0.25:
        matches.append("its energy is fairly close to what you want")
    else:
        drawbacks.append("it's much more intense than you prefer" if energy_gap > 0
                         else "it's much calmer than you prefer")

    valence_gap = song["valence"] - user_prefs.get("valence", 0.5)
    if abs(valence_gap) <= 0.1:
        matches.append("its emotional tone fits your taste")
    elif abs(valence_gap) > 0.25:
        drawbacks.append("it sounds more upbeat than you usually like" if valence_gap > 0
                         else "it sounds darker than you usually like")

    if user_prefs.get("likes_acoustic"):
        if song["acousticness"] >= 0.6:
            matches.append("it has the warm acoustic sound you enjoy")
        elif song["acousticness"] < 0.3:
            drawbacks.append("it's mostly electronic rather than acoustic")

    if not matches and drawbacks:
        return "This isn't a close match: " + _join_phrases(drawbacks) + "."
    if not matches:
        return "Nothing stands out, but it's one of the closest songs available."

    sentence = "Recommended because " + _join_phrases(matches) + "."
    if drawbacks:
        sentence += " However, " + _join_phrases(drawbacks) + "."
    return sentence

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, _ = score_song(user_prefs, song)
        scored.append((song, score, explain_song(user_prefs, song)))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
