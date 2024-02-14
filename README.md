# 🎬 Movie Q&A Chatbot Repository 🤖

Welcome to the Movie Chatbot Repository! This repository contains a Streamlit application that allows users to search for movies, retrieve movie details, and get movie comments/reviews from IMDb. It also includes a chatbot that answers questions about the movie while considering the reviews written by users. 🎥🍿

## 📁 Files in this Repository

### 📄 app.py

This is the main application file. It uses the `imdb`, `streamlit`, `dotenv`, and a custom `chatbot` module to provide a user-friendly interface for movie search and interaction. It also uses the `logging` module from the Python Standard Library for logging important events and errors.

Here are some of the key functions in this file:

- `search_movie(query)`: Searches for a movie based on the query and returns a list of movie results.
- `get_movie_details(movie_id)`: Retrieves details of a movie by its ID and returns a tuple containing movie details (title, year, genres, plot, rating).
- `get_movie_comments(movie_id)`: Retrieves comments/reviews of a movie by its ID and returns a dictionary containing comments by author.
- `main()`: Main function for the Streamlit application. It handles user input, calls the other functions to retrieve movie details and comments, and manages the chatbot interaction.

### 📄 chatbot.py

This file contains the implementation of a chatbot using the RAG (Retrieval-Augmented Generation) model with OpenAI's GPT-3.5-turbo for question answering and document retrieval. It also includes classes for creating documents from a directory or a text file and saving them in a FAISS index for efficient searching.

Here are some of the key functions in this file:

- `CreateDocument.create_documents`: Creates and saves a FAISS index for a collection of documents using OpenAI embeddings and a text splitter.
- `CreateFile.create_documents`: Creates and saves a FAISS index for a collection of documents using OpenAI embeddings and a text splitter.
- `RAGChain.run_rag_chain`: Runs a RAG chain with a given query and returns the result of the RAG chain execution.

### 📄 data.txt

This file stores movie details, user reviews, and ratings for the movies. It is used as a temporary storage which is later used by the RAG.

## 🚀 Getting Started

To get started with this application, follow the following steps:

1.  Clone this repository and install the necessary dependencies using the command mentioned below.

    ```
    pip3 install -r requirements.txx
    ```

2.  Next create a `.env` file in the working directory(Same folder) and add an OpenAI API Key to it. You can get the OpenAI API key by visiting the website: https://platform.openai.com/api-keys
    Here’s how you store the OpenAI API key in the .env file:

    ```
    OPENAI_API_KEY=your_api_key
    ```

3.  Once you are done with the setup you are good to go and run the application. Here's the command required to run the app.

    ```
    streamlit run app.py
    ```

## 📚 Notes

- The application uses environment variables, which are loaded using `load_dotenv()`.
- Logging is set up at the beginning of the file to log important events and errors.
- The chatbot is initialized and used within the `main()` function.
- The application saves movie details and comments to a file named "data.txt" in the "data" directory.
- The application handles exceptions and logs any errors that occur during the movie analysis or chatbot interaction.

## 🎉 Conclusion

I hope you find this repository useful and enjoyable! If you have any questions or suggestions, feel free to open an issue or submit a pull request. Happy movie searching! 🎉🎬
