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

Generated with `python -m src.main`. `src/main.py` defines three standard profiles and six adversarial / edge-case profiles meant to see whether the scoring logic can be tricked. Each block below is the terminal output (top 5) for one profile.

### Standard profiles

#### Chill Lofi

```
=== Chill Lofi ===
Prefs: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.38, 'valence': 0.58, 'likes_acoustic': True}

#  Title                 Artist          Genre      Mood       Score
--------------------------------------------------------------------
1  Library Rain          Paper Lanterns  lofi       chill       5.87
   Recommended because it's a lofi song (your favorite genre), it
   has the chill mood you're looking for, its energy level is right
   where you like it, its emotional tone fits your taste, and it has
   the warm acoustic sound you enjoy.

2  Midnight Coding       LoRoom          lofi       chill       5.78
   Recommended because it's a lofi song (your favorite genre), it
   has the chill mood you're looking for, its energy level is right
   where you like it, its emotional tone fits your taste, and it has
   the warm acoustic sound you enjoy.

3  Focus Flow            LoRoom          lofi       focused     4.85
   Recommended because it's a lofi song (your favorite genre), its
   energy level is right where you like it, its emotional tone fits
   your taste, and it has the warm acoustic sound you enjoy.

4  Spacewalk Thoughts    Orbit Bloom     ambient    chill       3.74
   Recommended because it has the chill mood you're looking for, its
   energy level is right where you like it, its emotional tone fits
   your taste, and it has the warm acoustic sound you enjoy.

5  Coffee Shop Stories   Slow Stereo     jazz       relaxed     2.80
   Recommended because its energy level is right where you like it
   and it has the warm acoustic sound you enjoy.
```

**Observation:** Works as designed: both lofi+chill songs lead, and *Focus Flow* (genre only) beats *Spacewalk Thoughts* (mood only), so genre outweighs mood.

#### High-Energy Pop

```
=== High-Energy Pop ===
Prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 0.85, 'valence': 0.85, 'likes_acoustic': False}

#  Title                 Artist          Genre      Mood       Score
--------------------------------------------------------------------
1  Sunrise City          Neon Echo       pop        happy       5.45
   Recommended because it's a pop song (your favorite genre), it has
   the happy mood you're looking for, its energy level is right
   where you like it, and its emotional tone fits your taste.

2  Gym Hero              Max Pulse       pop        intense     4.30
   Recommended because it's a pop song (your favorite genre), its
   energy level is right where you like it, and its emotional tone
   fits your taste.

3  Rooftop Lights        Indigo Parade   indie pop  happy       3.33
   Recommended because it has the happy mood you're looking for, its
   energy level is right where you like it, and its emotional tone
   fits your taste.

4  Glowstick Heaven      Pulse Theory    edm        euphoric    2.30
   Recommended because its energy level is right where you like it
   and its emotional tone fits your taste.

5  Fuego Lento           Sol de Cadiz    flamenco   passionate  2.19
   Recommended because its energy level is right where you like it.
   However, it sounds darker than you usually like.
```

**Observation:** Sensible. *Gym Hero* ranks 2nd on the genre bonus alone even though its mood is "intense", not "happy".

#### Deep Intense Rock

```
=== Deep Intense Rock ===
Prefs: {'genre': 'rock', 'mood': 'intense', 'energy': 0.92, 'valence': 0.4, 'likes_acoustic': False}

#  Title                 Artist          Genre      Mood       Score
--------------------------------------------------------------------
1  Storm Runner          Voltline        rock       intense     5.40
   Recommended because it's a rock song (your favorite genre), it
   has the intense mood you're looking for, its energy level is
   right where you like it, and its emotional tone fits your taste.

2  Gym Hero              Max Pulse       pop        intense     3.11
   Recommended because it has the intense mood you're looking for
   and its energy level is right where you like it. However, it
   sounds more upbeat than you usually like.

3  Iron Verdict          Blackgate       metal      angry       2.23
   Recommended because its energy level is right where you like it.

4  Fuego Lento           Sol de Cadiz    flamenco   passionate  2.23
   Recommended because its energy level is right where you like it.

5  Night Drive Loop      Neon Echo       synthwave  moody       2.15
   Recommended because its energy is fairly close to what you want
   and its emotional tone fits your taste.
```

**Observation:** Only one rock song exists, so after #1 the list is filled by whatever has high energy. Positions 3–5 are within 0.08 points of each other.

### Adversarial / edge-case profiles

#### Conflict: Energetic but Sad

```
=== Conflict: Energetic but Sad ===
Prefs: {'genre': 'folk', 'mood': 'sad', 'energy': 0.9, 'valence': 0.15, 'likes_acoustic': True}

#  Title                 Artist          Genre      Mood       Score
--------------------------------------------------------------------
1  Paper Boats           Willow & Wren   folk       sad         5.01
   Recommended because it's a folk song (your favorite genre), it
   has the sad mood you're looking for, its emotional tone fits your
   taste, and it has the warm acoustic sound you enjoy. However,
   it's much calmer than you prefer.

2  Fuego Lento           Sol de Cadiz    flamenco   passionate  2.45
   Recommended because its energy level is right where you like it
   and it has the warm acoustic sound you enjoy. However, it sounds
   more upbeat than you usually like.

3  Iron Verdict          Blackgate       metal      angry       2.35
   Recommended because its energy level is right where you like it
   and its emotional tone fits your taste. However, it's mostly
   electronic rather than acoustic.

4  Storm Runner          Voltline        rock       intense     2.20
   Recommended because its energy level is right where you like it.
   However, it sounds more upbeat than you usually like and it's
   mostly electronic rather than acoustic.

5  Night Drive Loop      Neon Echo       synthwave  moody       2.04
   Recommended because its energy is fairly close to what you want.
   However, it sounds more upbeat than you usually like and it's
   mostly electronic rather than acoustic.
```

**Observation:** **Tricked.** *Paper Boats* wins by a wide margin (5.01 vs 2.45) even though its energy is 0.26 against a 0.90 target. Genre + mood (+3.0) easily outvote the energy penalty (max 1.5), so the conflict is silently resolved in favor of the labels. The explanation does flag "much calmer than you prefer", which is honest.

#### Trap: Calm Metal Fan

```
=== Trap: Calm Metal Fan ===
Prefs: {'genre': 'metal', 'mood': 'chill', 'energy': 0.2, 'valence': 0.8, 'likes_acoustic': True}

#  Title                 Artist          Genre      Mood       Score
--------------------------------------------------------------------
1  Spacewalk Thoughts    Orbit Bloom     ambient    chill       3.69
   Recommended because it has the chill mood you're looking for, its
   energy level is right where you like it, and it has the warm
   acoustic sound you enjoy.

2  Library Rain          Paper Lanterns  lofi       chill       3.51
   Recommended because it has the chill mood you're looking for, its
   energy is fairly close to what you want, and it has the warm
   acoustic sound you enjoy.

3  Midnight Coding       LoRoom          lofi       chill       3.28
   Recommended because it has the chill mood you're looking for, its
   energy is fairly close to what you want, and it has the warm
   acoustic sound you enjoy.

4  Iron Verdict          Blackgate       metal      angry       2.77
   Recommended because it's a metal song (your favorite genre).
   However, it's much more intense than you prefer, it sounds darker
   than you usually like, and it's mostly electronic rather than
   acoustic.

5  Coffee Shop Stories   Slow Stereo     jazz       relaxed     2.60
   Recommended because its energy is fairly close to what you want,
   its emotional tone fits your taste, and it has the warm acoustic
   sound you enjoy.
```

**Observation:** **Not tricked.** *Iron Verdict* gets +2.0 for genre but loses on energy, valence and acousticness, so it drops to #4. Mood + three numeric features together can outweigh a genre match.

#### Ghost Genre: K-pop / Dreamy

```
=== Ghost Genre: K-pop / Dreamy ===
Prefs: {'genre': 'k-pop', 'mood': 'dreamy', 'energy': 0.6, 'valence': 0.7, 'likes_acoustic': False}

#  Title                 Artist          Genre      Mood       Score
--------------------------------------------------------------------
1  Island Time           Sunny Roots     reggae     playful     2.29
   Recommended because its energy level is right where you like it.

2  Velvet Hours          Mara Lux        r&b        romantic    2.28
   Recommended because its energy is fairly close to what you want
   and its emotional tone fits your taste.

3  Dusty Porch Lights    Copper Creek    country    nostalgic   2.26
   Recommended because its energy level is right where you like it.

4  Rooftop Lights        Indigo Parade   indie pop  happy       2.15
   Recommended because its energy is fairly close to what you want.

5  Concrete Crown        Kilo Vance      hip-hop    confident   2.15
   Recommended because its energy is fairly close to what you want
   and its emotional tone fits your taste.
```

**Observation:** With no possible genre or mood match, the top 5 are squeezed into a 0.14-point band (2.15–2.29). The ranking is close to arbitrary, and nothing tells the user their genre wasn't found.

#### Case Mismatch: 'LoFi' / 'Chill'

```
=== Case Mismatch: 'LoFi' / 'Chill' ===
Prefs: {'genre': 'LoFi', 'mood': 'Chill', 'energy': 0.38, 'valence': 0.58, 'likes_acoustic': True}

#  Title                 Artist          Genre      Mood       Score
--------------------------------------------------------------------
1  Library Rain          Paper Lanterns  lofi       chill       2.87
   Recommended because its energy level is right where you like it,
   its emotional tone fits your taste, and it has the warm acoustic
   sound you enjoy.

2  Focus Flow            LoRoom          lofi       focused     2.85
   Recommended because its energy level is right where you like it,
   its emotional tone fits your taste, and it has the warm acoustic
   sound you enjoy.

3  Coffee Shop Stories   Slow Stereo     jazz       relaxed     2.80
   Recommended because its energy level is right where you like it
   and it has the warm acoustic sound you enjoy.

4  Midnight Coding       LoRoom          lofi       chill       2.77
   Recommended because its energy level is right where you like it,
   its emotional tone fits your taste, and it has the warm acoustic
   sound you enjoy.

5  Spacewalk Thoughts    Orbit Bloom     ambient    chill       2.74
   Recommended because its energy level is right where you like it,
   its emotional tone fits your taste, and it has the warm acoustic
   sound you enjoy.
```

**Observation:** **Tricked.** Same intent as "Chill Lofi", but exact string matching gives zero categorical points. Scores drop from ~5.8 to ~2.8, and *Coffee Shop Stories* (jazz) ends up above *Midnight Coding*, a perfect lofi/chill match.

#### Out of Range: energy 1.8, valence -0.5

```
=== Out of Range: energy 1.8, valence -0.5 ===
Prefs: {'genre': 'edm', 'mood': 'euphoric', 'energy': 1.8, 'valence': -0.5, 'likes_acoustic': False}

#  Title                 Artist          Genre      Mood       Score
--------------------------------------------------------------------
1  Glowstick Heaven      Pulse Theory    edm        euphoric    2.82
   Recommended because it's a edm song (your favorite genre) and it
   has the euphoric mood you're looking for. However, it's much
   calmer than you prefer and it sounds more upbeat than you usually
   like.

2  Iron Verdict          Blackgate       metal      angry       0.54
   This isn't a close match: it's much calmer than you prefer and it
   sounds more upbeat than you usually like.

3  Storm Runner          Voltline        rock       intense     0.18
   This isn't a close match: it's much calmer than you prefer and it
   sounds more upbeat than you usually like.

4  Fuego Lento           Sol de Cadiz    flamenco   passionate  0.01
   This isn't a close match: it's much calmer than you prefer and it
   sounds more upbeat than you usually like.

5  Night Drive Loop      Neon Echo       synthwave  moody      -0.07
   This isn't a close match: it's much calmer than you prefer and it
   sounds more upbeat than you usually like.
```

**Observation:** **Breaks the scale.** Inputs aren't clamped to 0–1, so closeness goes negative and #5 has a score of -0.07. The explanation for *Glowstick Heaven* also says "a edm" (article bug) and "much calmer than you prefer" for the highest-energy song in the catalog.

#### Empty Profile {}

```
=== Empty Profile {} ===
Prefs: {}

#  Title                 Artist          Genre      Mood       Score
--------------------------------------------------------------------
1  Dusty Porch Lights    Copper Creek    country    nostalgic   2.39
   Recommended because its energy level is right where you like it
   and its emotional tone fits your taste.

2  Midnight Coding       LoRoom          lofi       chill       2.32
   Recommended because its energy level is right where you like it
   and its emotional tone fits your taste.

3  Velvet Hours          Mara Lux        r&b        romantic    2.31
   Recommended because its energy level is right where you like it.

4  Focus Flow            LoRoom          lofi       focused     2.26
   Recommended because its energy level is right where you like it
   and its emotional tone fits your taste.

5  Library Rain          Paper Lanterns  lofi       chill       2.17
   Recommended because its energy is fairly close to what you want
   and its emotional tone fits your taste.
```

**Observation:** No crash: missing keys default to energy 0.5 / valence 0.5, so the system recommends the most "average" songs. Reasonable fallback, but the user gets no signal that their profile was empty.

### Takeaways from the adversarial runs

- **Labels beat numbers.** Genre + mood are worth 3.0 of the 6.0 points, so a song with matching labels wins even when its energy is far off (Conflict profile).
- **Exact string matching is fragile.** `"LoFi"` vs `"lofi"` erases half the score. Normalizing with `.strip().lower()` would fix this.
- **No input validation.** Energy/valence outside 0–1 produce negative scores and misleading explanations. Clamping inputs would fix this.
- **Unknown genres fail silently.** When nothing can match, the ranking becomes a near-tie and the user isn't told.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Experiment 1: Weight shift (energy ×2, genre ×½)

**Change** (in `src/recommender.py`):

| Weight | Baseline | Experiment |
|---|---|---|
| `GENRE_WEIGHT` | 2.0 | **1.0** |
| `MOOD_WEIGHT` | 1.0 | 1.0 |
| `ENERGY_WEIGHT` | 1.5 | **3.0** |
| `VALENCE_WEIGHT` | 1.0 | 1.0 |
| `ACOUSTIC_WEIGHT` | 0.5 | 0.5 |
| **Max possible score** | 6.0 | **6.5** |

**Checking the math.** Each part of the score still has a fixed range: genre and mood add 0 or their weight, energy and valence add `weight × (1 − |gap|)`, which stays between 0 and the weight when inputs are in 0–1, and acousticness adds `0.5 × acousticness`. So the new maximum is 1 + 1 + 3 + 1 + 0.5 = **6.5**. To confirm it, I scored every song against every combination of catalog genre and mood (plus one non-matching value), energy and valence from 0.0 to 1.0 in steps of 0.1, and both acoustic settings. Every score fell in **[0.25, 6.41]**, inside 0–6.5. Each score also equaled the sum of the points listed in its reasons. Both unit tests still pass. The only change in meaning is that energy is now 46% of the total score (3.0 / 6.5) instead of 25%. Genre dropped from 33% to 15%.

**Top-5 before → after** (score out of 6.0 → score out of 6.5):

```
High-Energy Pop
  1  Sunrise City            5.45  ->  Sunrise City            5.90
  2  Gym Hero                4.30  ->  Rooftop Lights          4.69
  3  Rooftop Lights          3.33  ->  Gym Hero                4.68
  4  Glowstick Heaven        2.30  ->  Fuego Lento             3.67
  5  Fuego Lento             2.19  ->  Glowstick Heaven        3.65

Deep Intense Rock
  1  Storm Runner            5.40  ->  Storm Runner            5.89
  2  Gym Hero                3.11  ->  Gym Hero                4.60
  3  Iron Verdict            2.23  ->  Iron Verdict            3.66
  4  Fuego Lento             2.23  ->  Fuego Lento             3.61
  5  Night Drive Loop        2.15  ->  Glowstick Heaven        3.41

Conflict: Energetic but Sad
  1  Paper Boats             5.01  ->  Paper Boats             4.55
  2  Fuego Lento             2.45  ->  Fuego Lento             3.86

Trap: Calm Metal Fan
  4  Iron Verdict            2.77  ->  Coffee Shop Stories     3.85
  5  Coffee Shop Stories     2.60  ->  Winter Sonata No. 3     3.80
```

*Chill Lofi* kept the same order. The lofi songs' lead over the rest shrank, though: *Spacewalk Thoughts* (ambient) moved to 0.23 behind *Focus Flow*, down from 1.11.

**More accurate or just different? Mostly just different.**

- **Better:** For the High-Energy Pop listener, *Rooftop Lights* (indie pop, **happy**) now edges out *Gym Hero* (pop, **intense**). That fits a "happy pop" request better. In the Conflict profile, *Paper Boats* now leads by 0.69 instead of 2.56, so a large energy mismatch finally costs something.
- **Worse:** The Deep Intense Rock listener asked for darker music (valence 0.40), but now gets *Glowstick Heaven*, a bright, euphoric EDM track (valence 0.90), because its energy is 0.95. The pop listener now gets flamenco (*Fuego Lento*) above EDM because the flamenco track's energy matches almost exactly. The Calm Metal Fan's metal song drops out entirely, and its place goes to *Winter Sonata*, a melancholic track with valence 0.18 against a target of 0.80.
- **Why:** In this catalog, energy rises and falls with tempo and danceability, so doubling its weight turns the recommender into an "intensity matcher". Any loud song looks like a good fit for any loud listener, whatever its genre or emotional tone. Several new rankings are decided by gaps of 0.01–0.02, which is noise rather than real preference.
- **Conclusion:** Changing the weights moves songs around near the edges of the top 5, but it doesn't fix the deeper problems: case-sensitive matching, no limits on out-of-range inputs, and a small catalog. The baseline weights give rankings that better match what each profile describes. All outputs in *Sample Recommendation Output* above use the baseline weights.

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



