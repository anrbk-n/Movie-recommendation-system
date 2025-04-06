# Movie Recommendation System
A web application designed to help users find movies, even if they misspell the titles. This system leverages the T5 model to automatically correct errors and provides relevant recommendations based on the corrected title.

## Description

Users often misspell movie titles when searching. This system addresses this issue by employing the **T5 (Text-to-Text Transfer Transformer)** model to correct typos on the fly. Once the title is corrected, the system uses **content-based filtering** to find and recommend movies similar to the one the user intended to search for.

The project combines Natural Language Processing (NLP) with recommendation system techniques and offers a user-friendly web interface built with **Flask**.

## Key Features ✨

* **🧠 Automatic Error Correction:** Utilizes the T5 model to detect and fix misspelled movie titles.
* **🔍 Smart Search:** Allows users to input titles with typos; the system finds the closest match from the dataset.
* **🎬 Dynamic Recommendations:** Suggests movies similar to the found (corrected) movie based on content similarity.
* **💻 User-Friendly Web Interface:** A simple and intuitive interface built with Flask, HTML, and JavaScript.
* **⚡ Real-Time Results:** Dynamically fetches and displays relevant movie suggestions as the user types in the search bar.
* **➕ "Show More" Button:** Enables users to view additional recommendation options.
* **(Optional) Fetch Additional Information:** Potential integration with APIs (like TMDB) to retrieve posters, ratings, and descriptions (if implemented).

## Technology Stack 🛠️

* **Backend:** Python, Flask
* **NLP/ML:** T5 Model (likely via Hugging Face `transformers`)
* **Data Handling:** Pandas (likely)
* **Recommendation Logic:** Scikit-learn (potentially for TF-IDF/Cosine Similarity in content-based filtering)
* **Data Storage:** (Specify here how movie data is stored - e.g., CSV file, Database)
  
## How It Works 🤔

1.  **Input & Correction:** The user enters a movie title (potentially misspelled) into the web interface.
2.  **T5 Correction:** The input string is passed to the T5 model, which attempts to correct any spelling errors, outputting the most likely intended movie title.
3.  **Content-Based Filtering:** The corrected movie title is used to find its representation (e.g., genre, plot keywords, actors) in the dataset. The system then calculates the similarity (e.g., using cosine similarity on TF-IDF vectors) between this movie and others in the dataset.
4.  **Recommendation:** Movies with the highest similarity scores are returned as recommendations.
5.  **Display:** The recommendations are displayed to the user via the web interface.

