import imdb
import streamlit as st
from dotenv import load_dotenv
import chatbot  # Import your chatbot module
import logging

load_dotenv()
ia = imdb.IMDb()

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
history = " "
chat_history = []


def search_movie(query):
    """Search for a movie based on the query.

    Args:
        query (str): The movie title to search for.

    Returns:
        list: A list of movie results.
    """
    results = ia.search_movie(query)
    logging.info(f"Searching for movie with query: {query}")
    return results if results else []


def get_movie_details(movie_id):
    """Retrieve details of a movie by its ID.

    Args:
        movie_id (str): The IMDb movie ID.

    Returns:
        tuple: A tuple containing movie details (title, year, genres, plot, rating).
    """
    movie = ia.get_movie(movie_id)
    title = movie.get("title", "N/A")
    year = movie.get("year", "N/A")
    genres = ", ".join(movie.get("genres", ["N/A"]))
    plot = movie.get("plot", ["N/A"])[0]
    rating = movie.get("rating", "N/A")
    logging.info(f"Retrieving details for movie ID: {movie_id}")
    return title, year, genres, plot, rating


def get_movie_comments(movie_id):
    """Retrieve comments/reviews of a movie by its ID.

    Args:
        movie_id (str): The IMDb movie ID.

    Returns:
        dict: A dictionary containing comments by author.
    """
    movie = ia.get_movie(movie_id)
    reviews = ia.get_movie_reviews(movie_id)
    comments_dict = {}
    if reviews:
        for review in reviews["data"]["reviews"]:
            author = review["author"]
            comment = review["content"]
            comments_dict.setdefault(author, []).append(comment)
    logging.info(f"Retrieving comments for movie ID: {movie_id}")
    return comments_dict


def main():
    """Main function for the Streamlit application."""
    global history
    global chat_history
    st.title("Movie Q&A Bot")
    chat_history = st.session_state.get("chat_history", [])
    st.session_state.submit_button_state = st.session_state.get(
        "submit_button_state", False
    )

    # Initialize bot and document if not present in session state
    if "bot" not in st.session_state or "doc" not in st.session_state:
        st.session_state.bot = None
        st.session_state.doc = None

    with st.sidebar:
        search_query = st.text_input("Enter a movie title:")
        submit_button = st.button(
            "Submit",
            key="submit_button",
            on_click=lambda: setattr(st.session_state, "submit_button_state", True),
        )

    if st.session_state.submit_button_state:
        message = "Results: \n"
        results = search_movie(search_query)

        if results:
            for i, movie in enumerate(results, 1):
                title = movie.get("title", "N/A")
                year = movie.get("year", "N/A")
                message += f"{i}. {title} ({year})\n"

            with st.chat_message("assistant"):
                st.write(message)

            chosen_movie_index = st.number_input(
                "Enter the index of the movie you want to get details for:",
                min_value=1,
                max_value=len(results),
            )
            if st.button("Analyze the movie"):
                chosen_movie_id = results[chosen_movie_index - 1].movieID
                title, year, genres, plot, rating = get_movie_details(chosen_movie_id)
                message = f"\nTitle: {title}\n\nYear: {year}\n\nGenres: {genres}\n\nPlot: {plot}\n\nRating: {rating}\n"
                chat_history.append((message, "assistant"))
                logging.info("Movie details retrieved.")

                try:
                    # Retrieve comments and save to a file
                    comments = get_movie_comments(chosen_movie_id)
                    details = {
                        "Title": title,
                        "Year": year,
                        "Genres": genres,
                        "Plot": plot,
                        "Rating": rating,
                    }
                    with open("data/data.txt", "w") as f:
                        f.write("Movie Details:\n")
                        for key, value in details.items():
                            f.write(f"{key}: {value}\n")
                        f.write("\n")
                        f.write("Comments:\n")
                        for author, comment_list in comments.items():
                            f.write(f"Author: {author}\n")
                            for comment in comment_list:
                                f.write(f"Comment: {comment}\n")
                            f.write("---\n")
                    # Initialize chatbot
                    if st.session_state.doc is None:
                        st.session_state.doc = chatbot.CreateDocument()
                        st.session_state.doc = st.session_state.doc.create_documents()
                    st.session_state.bot = chatbot.RAGChain()
                    chat_history.append(
                        ("Enter any questions you have about the movie", "assistant")
                    )
                    logging.info("Document and bot initialized.")
                except Exception as e:
                    details = {
                        "Title": title,
                        "Year": year,
                        "Genres": genres,
                        "Plot": plot,
                        "Rating": rating,
                    }
                    with open("data/data.txt", "w") as f:
                        f.write("Movie Details:\n")
                        for key, value in details.items():
                            f.write(f"{key}: {value}\n")
                        f.write("\n")
                        f.write("Comments: No comments for found for this movie\n")
                        f.write("---\n")
                    logging.error(f"Error analyzing movie: {e}")
                    chat_history.append(
                        ("Enter any questions you have about the movie", "assistant")
                    )
                    if st.session_state.doc is None:
                        st.session_state.doc = chatbot.CreateDocument()
                        st.session_state.doc = st.session_state.doc.create_documents()
                    st.session_state.bot = chatbot.RAGChain()

            prompt = st.chat_input("Enter questions about the movie:")
            try:
                if prompt:
                    print(prompt)
                    chat_history.append((prompt, "user"))
                    bot_response = st.session_state.bot.run_rag_chain(prompt, history)
                    chat_history.append((bot_response, "assistant"))
                    history += (
                        "User Input: "
                        + prompt
                        + "; Bot response: "
                        + bot_response
                        + "\n"
                    )
                    st.session_state.chat_history = chat_history
                    logging.info("Bot response generated.")
            except Exception as e:
                logging.error(f"Error generating bot response: {e}")

            # Display chat history
            for message, sender in chat_history:
                with st.chat_message(sender):
                    st.write(message)
    else:
        with st.chat_message("assistant"):
            st.write("Please enter a movie title before continuing.\n")

if __name__ == "__main__":
    main()
