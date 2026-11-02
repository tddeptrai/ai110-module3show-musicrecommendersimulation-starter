# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube blend two approaches. **Collaborative filtering** recommends what similar listeners played ("people who liked X also liked Y"). **Content-based filtering** compares the attributes of songs themselves: genre, mood and audio features such as energy and valence. They mix both with behavior signals like skips, replays and saves, then rank millions of candidates by predicted engagement. My version is a small, purely content-based simulation. It has no listening history, so it scores every song by how closely it matches a user's stated taste. It prioritizes **genre and mood matches first**, then **closeness in energy and valence**, which together capture most of a song's "vibe" (how intense it feels and how positive it sounds). In this dataset tempo, danceability and acousticness almost exactly track energy (r ≈ 0.86–0.99), so scoring them separately would count the same thing several times. They stay in the data but carry little or no weight. Each song gets a score, the catalog is sorted, and the top *k* are returned with a short explanation of why each one matched.

### `Song` features

| Feature | Type | Used for |
|---|---|---|
| `genre` | category | exact match with the user's favorite genre (highest weight) |
| `mood` | category | exact match with the user's favorite mood |
| `energy` | 0.0–1.0 | closeness to the user's target energy |
| `valence` | 0.0–1.0 | closeness to the user's target valence (how positive or upbeat it sounds) |
| `acousticness` | 0.0–1.0 | small bonus when the user likes acoustic songs |
| `tempo_bpm`, `danceability` | numeric | stored but not scored (they repeat energy) |
| `id`, `title`, `artist` | metadata | identification and display only |

### `UserProfile` features

| Feature | Type | Meaning |
|---|---|---|
| `favorite_genre` | str | genre the user wants most, e.g. `"lofi"` |
| `favorite_mood` | str | mood the user wants, e.g. `"chill"` |
| `target_energy` | float 0.0–1.0 | how intense the user wants songs to feel |
| `likes_acoustic` | bool | whether acoustic songs get a bonus |
| `target_valence` | float 0.0–1.0 | how positive or upbeat the user wants songs to sound (defaults to 0.5) |

### Taste profile used for comparisons

The simulation compares every song against one listener: a **late-night studier** who wants calm, mildly warm, acoustic-leaning background music.

| Field | Value | Why |
|---|---|---|
| `favorite_genre` | `"lofi"` | lofi is the main study-music genre, and the catalog has three lofi songs, so the ranking has real competition |
| `favorite_mood` | `"chill"` | relaxed, not sleepy |
| `target_energy` | `0.38` | low, but not ambient-quiet (lofi songs sit at 0.35–0.42) |
| `target_valence` | `0.58` | mildly positive: neither sad nor bubbly |
| `likes_acoustic` | `True` | prefers warm, organic texture over synths |

In `src/main.py` this is written as:

```python
user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.38,
              "valence": 0.58, "likes_acoustic": True}
```

**Expected behavior:** *Library Rain* and *Midnight Coding* match on everything and should come first. The interesting test is next. *Focus Flow* matches the genre but not the mood (focused), while *Spacewalk Thoughts* matches the mood but not the genre (ambient). Their order shows whether genre or mood carries more weight. High-energy songs like *Iron Verdict* and *Glowstick Heaven* should land at the bottom.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



