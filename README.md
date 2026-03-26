# 🎬 Netflix-Style Movie Recommender

A content-based movie recommendation system featuring a beautiful, dark-themed UI built with **Streamlit**. This application recommends movies based on similarity in genres, keywords, cast, and crew. It also fetches real-time movie posters, ratings, YouTube trailers, and streaming platform (OTT) availability using the TMDB API.

## ✨ Features
* **Machine Learning Powered:** Uses scikit-learn's `CountVectorizer` and `cosine_similarity` to find the closest movie matches.
* **Rich Metadata:** Integrates with the TMDB API to display dynamic posters, user ratings, and where to stream the movie.
* **Netflix-Style UI:** Custom CSS with glass-morphism effects, a dark gradient background, and hover animations.
* **Favorites System:** Save movies you want to watch later to a dedicated sidebar list.
* **Trending Section:** Discover what's hot right now with a constantly refreshing trending movies section.

## 🛠️ Tech Stack
* **Language:** Python
* **Data Processing:** Pandas, NumPy, Ast
* **Machine Learning:** Scikit-Learn (Natural Language Processing)
* **Frontend/Framework:** Streamlit
* **External APIs:** The Movie Database (TMDB) API

---

## 🚀 How to Run this Project Locally

**Note:** To keep this repository lightweight and fast, the raw datasets (`.csv`) and generated machine learning models (`.pkl` > 170MB) are *not* included. You will need to generate them locally by following these steps:

### 1. Clone the Repository
Open your terminal and run:
```bash
git clone [https://github.com/vaibhavmurty4518/movie-recommender.git](https://github.com/vaibhavmurty4518/movie-recommender.git)
cd movie-recommender
2. Install Dependencies
Make sure you have Python installed. Then, install the required libraries:

Bash
pip install pandas numpy scikit-learn streamlit requests
3. Download the Datasets
Go to Kaggle and download the TMDB 5000 Movie Dataset.

Extract the archive.

Place movies.csv and credits.csv directly into the root folder of this project.

4. Train the Model (Generate .pkl files)
Run the main.py script to clean the data, calculate cosine similarities, and generate the necessary model files:

Bash
python main.py
Wait for the terminal to print: ✅ DONE: Files created successfully!
(You should now see movie_dict.pkl and similarity.pkl in your folder).

5. Run the Application
Start the Streamlit web server:

Bash
streamlit run app.py
The application will automatically open in your default web browser!

🔑 API Configuration (Optional)
This project uses a TMDB API key to fetch movie posters and trailers. A default key is included in app.py, but if you plan to deploy this or use it heavily, it is highly recommended to get your own free API key from The Movie Database (TMDB) and replace the API_KEY variable in app.py.

