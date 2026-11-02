# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
