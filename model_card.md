# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**: it matches songs to the vibe you describe.

---

## 2. Intended Use  

**Goal.** You describe your taste, and VibeMatch suggests the 5 songs from its catalog that fit it best. It doesn't predict what you'll play next. It only ranks songs by how closely they match what you said you want. Each pick comes with a short reason.

**Assumptions about the user.** It assumes you can name one favorite genre and one mood. It assumes your taste stays the same over time. It assumes you type genre and mood the same way the catalog spells them (for example, "lofi", not "LoFi").

**Intended use.**
- Classroom exploration of how content-based recommenders work.
- Trying out different taste profiles and seeing how the ranking changes.
- Learning where simple scoring rules go wrong.

**Not intended for.**
- Real users or a real music app. The catalog has only 19 songs.
- Judging what music is "good". The scores only measure how close a song is to one profile.
- Users with mixed or changing tastes, such as someone who wants both jazz and metal. The system can only hold one genre and one mood.
- Any decision that matters, such as which artists get promoted or paid. The data is made up, and so are the numbers.

---

## 3. How the Model Works  

The recommender works like a friend who knows your taste and gives every song in the catalog a "how well does this fit you?" score out of 6 points.

**What it knows about you.** You tell it five things: your favorite genre (like lofi), the mood you want (like chill), how energetic you want the music to be, how happy or dark you want it to sound, and whether you like acoustic songs.

**What it looks at in each song.** Every song has a genre, a mood, and a few sound measurements between 0 and 1: *energy* (calm to intense), *valence* (dark or sad to bright or happy), and *acousticness* (electronic to acoustic).

**How it scores a song.**
- **Same genre as your favorite:** +2 points. This is the biggest reward, because genre says the most about what a song sounds like.
- **Same mood as you asked for:** +1 point.
- **Energy:** up to 1.5 points. A song gets the full amount when its energy exactly matches what you want, and fewer points the further away it is. It doesn't reward "more energy" or "less energy," only being close to your target.
- **Happy or dark feel (valence):** up to 1 point, using the same closeness idea.
- **Acoustic bonus:** up to 0.5 points if you like acoustic music. The more acoustic the song, the bigger the bonus.

**How it picks songs.** It scores every song, sorts them from highest to lowest, and shows you the top five. Each song comes with a sentence explaining why it was picked, such as "it has the chill mood you're looking for and its energy level is right where you like it." It also points out drawbacks, such as "it's much more intense than you prefer."

**Changes from the starter.** The starter returned the first few songs with no scoring. I added the point system above and the plain-English explanations. I added valence as a user preference because it is the one sound measurement that doesn't just repeat energy. Tempo and danceability are left out of the score because, in this catalog, they rise and fall almost exactly with energy, so counting them would reward the same thing several times.

---

## 4. Data  

**Size.** The catalog is `data/songs.csv`, with 19 songs. The starter had 10. I added 9 more (ids 11–19) to cover more genres: hip-hop, classical, country, metal, reggae, edm, r&b, folk and flamenco.

**Features.** Each song has a title, artist, genre and mood. It also has five numbers: energy, valence, danceability and acousticness (all 0–1), plus tempo in BPM.

**Variety.** There are 16 genres and 15 moods. Most genres and moods have just one song. Lofi has the most songs (3), then pop (2). "Chill" is the most common mood (3 songs).

**Limits.**
- It's tiny. Most genres get one shot at the top 5, then the system has to fill the list with other genres.
- The numbers are made up by hand, not measured from real audio.
- Tempo, danceability and energy move almost together in this data, so they mostly say the same thing.
- It has no lyrics, language, release year, or listening history.
- Each song has only one genre and one mood. Real songs often have several.

---

## 5. Strengths  

- **Clear profiles get clear results.** For Chill Lofi, High-Energy Pop and Deep Intense Rock, the #1 song is the one I would have picked by hand.
- **Opposite users get opposite lists.** The lofi and pop listeners share no songs. One gets quiet acoustic tracks, the other gets loud electronic ones.
- **It reads the whole description, not just the genre.** The Calm Metal Fan got calm, happy, acoustic songs, not the one metal song. Several matching numbers together can beat one label.
- **The explanations are honest.** They point out drawbacks too, like "it's much calmer than you prefer". You can see why a song made the list, even when it's a bad pick.
- **It doesn't crash on bad input.** An empty profile still returns sensible middle-of-the-road songs.

---

## 6. Limitations and Bias 

The system trusts genre and mood labels over how a song actually sounds, and the small catalog makes this worse: 14 of the 16 genres have only one song each. A genre match plus a mood match is worth 3 of the 6 points, while the biggest possible energy penalty is only 1.5, so a song with the right labels wins even when it feels completely wrong. In my "energetic but sad" test (energy 0.9, mood sad), the only folk/sad song, *Paper Boats*, ranked #1 by more than 2.5 points even though its energy is 0.26, nowhere near the 0.9 target. Matching is also exact and case-sensitive, so a user who types "LoFi" instead of "lofi" loses all 3 label points and gets a jazz song ranked above a perfect lofi/chill match. Together, these mean users whose taste is in a well-stocked genre and who type labels exactly as the catalog stores them get much better results than everyone else.

---

## 7. Evaluation  

**Profiles tested.** I ran nine profiles through `python -m src.main` and read the top 5 for each (full output is in the README).

- *Standard:* **Chill Lofi** (lofi / chill, energy 0.38, likes acoustic), **High-Energy Pop** (pop / happy, energy 0.85, valence 0.85) and **Deep Intense Rock** (rock / intense, energy 0.92, valence 0.40).
- *Adversarial:* **Energetic but Sad** (folk / sad but energy 0.90), **Calm Metal Fan** (metal genre, but chill, quiet, happy and acoustic), **Ghost Genre** (k-pop / dreamy, neither of which exists in the catalog), **Case Mismatch** (Chill Lofi with "LoFi" / "Chill" capitalized), **Out of Range** (energy 1.8, valence -0.5) and **Empty Profile** (`{}`).

**What I looked for.** For each profile I checked whether #1 was the song I would hand-pick for that listener, whether the rest of the top 5 shared the requested "feel" (energy, brightness, acoustic or electronic), and whether the explanation sentence matched what the scores were really rewarding.

**What surprised me.**
- *Gym Hero* ranked #2 for **both** the pop and the rock listener, for different reasons: for pop it's the genre match, for rock it's the "intense" mood plus 0.93 energy. One song can be a good fit for two very different users.
- The **Energetic but Sad** profile got a quiet folk song (energy 0.26) at #1 by a wide margin. The labels outvoted the energy request completely.
- Capitalizing "LoFi" cut every score by about 3 points and let a jazz song pass a perfect lofi/chill match. One keystroke mattered more than any number in the profile.
- The **Calm Metal Fan** was *not* fooled: the only metal song came in #4, behind three chill songs. Mood plus energy, valence and acousticness together can outweigh a genre match.
- Out-of-range inputs produced a **negative** score (-0.07), which the 0–6 scale isn't supposed to allow.

**Pairwise comparisons.**

1. **Chill Lofi vs. High-Energy Pop:** The two lists share no songs. Lofi's top 5 all sit at energy 0.28–0.42 and acousticness ≥ 0.71, while pop's sit at energy 0.76–0.95 and are mostly electronic. That makes sense: the two energy targets are almost 0.5 apart, and only the lofi listener gets the acoustic bonus, so each profile pulls from the opposite end of the catalog.
2. **High-Energy Pop vs. Deep Intense Rock:** Both lists are loud and share *Gym Hero* and *Fuego Lento*, but the pop list is bright (*Sunrise City* valence 0.84, *Rooftop Lights* 0.81) while the rock list adds the dark *Iron Verdict* (valence 0.21) and the moody *Night Drive Loop*. The energy targets are nearly the same (0.85 vs. 0.92), so the difference comes from valence (0.85 vs. 0.40) and the genre/mood labels, which is exactly what those settings should do.
3. **Chill Lofi vs. Deep Intense Rock:** These are complete opposites. Lofi gets soft, acoustic study tracks, and rock gets fast, mostly electronic songs (acousticness 0.03–0.22 for all but *Fuego Lento*). Rock's top 5 is also much less "pure": after *Storm Runner* (5.40) and *Gym Hero* (3.11), positions 3–5 are separated by only 0.08 points. The catalog has three lofi songs but only one rock song, so the rock listener runs out of genre matches after #1.
4. **Chill Lofi vs. Case Mismatch:** The same five songs appear in both lists, but scores fall from 2.80–5.87 to 2.74–2.87, and *Midnight Coding* drops from #2 to #4 while *Coffee Shop Stories* (jazz) rises from #5 to #3. With the labels silently ignored, only energy, valence and acousticness are left, and those barely separate the songs. The list still looks fine, but only because the numbers happen to point at the same songs.
5. **Deep Intense Rock vs. Energetic but Sad:** Both ask for energy around 0.9 and low valence, and positions 2–5 of the "sad" list (*Fuego Lento*, *Iron Verdict*, *Storm Runner*, *Night Drive Loop*) look almost like the rock list. Only #1 differs: the folk/sad label match puts *Paper Boats* on top despite its low energy. This shows the labels decide the winner, and the numeric preferences only decide who comes after it.
6. **Chill Lofi vs. Calm Metal Fan:** The metal fan's top 3 (*Spacewalk Thoughts*, *Library Rain*, *Midnight Coding*) are the lofi listener's chill songs in a different order. *Spacewalk Thoughts* moves to #1 because its energy (0.28) and valence (0.65) are closer to this profile's 0.20 / 0.80 targets. The "chill + quiet + acoustic" description wins over the one-word genre, which is the right result for what this user actually described.
7. **Ghost Genre vs. Empty Profile:** Neither profile can earn genre or mood points, so both get mid-energy songs packed into a narrow score band (2.15–2.39) and share *Velvet Hours* and *Dusty Porch Lights*. The ghost-genre list leans brighter (*Island Time* valence 0.88, *Rooftop Lights* 0.81) because its valence target is 0.70 instead of the default 0.50. When labels can't match, valence and energy are the only things steering the list.
8. **High-Energy Pop vs. Out of Range:** Both want loud music, but an energy target of 1.8 doesn't make loud songs score higher. Every song is now "far away", so all scores shrink toward zero and one goes negative. Only *Glowstick Heaven* scores well (2.82), and only because of its edm/euphoric label match. This shows that the closeness formula assumes inputs between 0 and 1 and breaks rather than exaggerating when they aren't.

**Other checks.** The two unit tests in `tests/test_recommender.py` pass. For the weight-shift experiment (genre 1.0, energy 3.0), I scored every song against a grid of preference combinations to confirm every score stays between 0 and the new maximum of 6.5 and equals the sum of its listed points. That experiment reshuffled close calls but did not make the rankings more accurate overall (details in the README).

---

## 8. Future Work  

1. **Clean up user input.** Lowercase and trim genre and mood before comparing, so "LoFi" matches "lofi". Clamp energy and valence to 0–1 so scores can't go negative. Warn the user when their genre or mood isn't in the catalog.
2. **Give partial credit for similar labels.** Right now "indie pop" gets zero genre points for a pop fan, and "relaxed" gets zero for someone who wants "chill". A small table of related genres and moods could give these half points. That way labels count, but don't decide everything.
3. **Add more songs and mix up the top 5.** More songs per genre would give each listener real choices. A simple rule like "at most two songs from the same genre or artist" would keep the list from repeating itself.

---

## 9. Personal Reflection  

**Biggest learning moment.** It was the "LoFi" test. I typed the same profile with two capital letters, and every score dropped by about 3 points. A jazz song jumped above a perfect lofi match. Nothing crashed and the list still looked fine, so I would never have noticed without testing it on purpose. That taught me that a recommender can be quietly wrong. You have to go looking for the failures.

**How AI tools helped, and when I double-checked.** The AI assistant was fast at the boring parts. It wrote the profile loop in `main.py`, ran all nine profiles, and built the before/after tables for the weight experiment. It also suggested adversarial profiles I hadn't thought of, like out-of-range numbers and an empty profile. But it made mistakes I had to catch:
- Its first script for comparing rankings printed empty tables because of a bad pattern match. It had to be fixed and rerun.
- In the Evaluation section, it first wrote that rock's positions 2–5 were within 0.08 points. Checking the output showed only positions 3–5 were that close.
- After the weight experiment, the code no longer matched the outputs in the README. I had to change the weights back so the documents and code agreed.

My rule now is that every number in a write-up has to be checked against real output, not taken from memory.

**What surprised me about simple algorithms.** The whole system is five additions. There's no learning and no history. But the results still *feel* personal, mostly because of the explanation sentences. "It has the chill mood you're looking for" sounds like the app understands you, even though it's just a string comparison. That made me realize the explanation does a lot of the work of seeming smart. It can also make a bad pick sound reasonable.

**What I'd try next.** First, I'd fix the input problems: lowercase the labels and clamp the numbers to 0–1. Then I'd give partial credit for related genres and moods, so "indie pop" counts a little for a pop fan. Finally, I'd like to add a tiny bit of collaborative filtering, like "people with your profile also liked...", to see how it changes the results compared to matching on features alone.  
