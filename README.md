# Movie-recommendation-system
The Movie Recommendation System is a web application designed to help users find movies even if they misspell the titles. By leveraging the T5 (Text-to-Text Transfer Transformer) model, the system automatically corrects errors in movie titles, enabling users to receive accurate recommendations regardless of typing mistakes. This project combines Natural Language Processing (NLP) with content-based filtering to suggest movies based on user input.

Key features include error correction, search functionality, dynamic results display, and the ability to fetch additional movie information in real time. The project was developed using Flask for the backend, with a focus on creating an easy-to-use and intuitive interface for users.

Features
Error Correction: The system automatically detects and corrects misspelled movie titles using the T5 model, ensuring that users can search for movies even with typos.

Search Functionality: Users can enter movie titles with spelling mistakes, and the system will suggest the closest match from the available dataset.

Dynamic Recommendations: The system provides movie recommendations based on the corrected title input, offering suggestions for similar movies to explore.

User-Friendly Web Interface: Built with Flask, the application features a simple and intuitive web interface. The frontend utilizes HTML and JavaScript to enhance user interaction.

Real-Time Search Results: As users type in the search bar, the system dynamically fetches and displays relevant movie suggestions, allowing users to view more options by clicking a "Show More" button.

