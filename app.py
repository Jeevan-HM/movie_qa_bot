import imdb
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
# Create an instance of the IMDb class
ia = imdb.IMDb()


def search_movie(query):
    # Search for the movie
    results = ia.search_movie(query)
    if results:
        return results
    else:
        return []


def get_movie_details(movie_id):
    # Retrieve movie details by movie ID
    movie = ia.get_movie(movie_id)
    title = movie.get("title", "N/A")
    year = movie.get("year", "N/A")
    genres = ", ".join(movie.get("genres", ["N/A"]))
    plot = movie.get("plot", ["N/A"])[0]
    rating = movie.get("rating", "N/A")

    return title, year, genres, plot, rating


def get_movie_comments(movie_id):
    # Retrieve movie reviews by movie ID
    movie = ia.get_movie(movie_id)
    reviews = ia.get_movie_reviews(movie_id)

    comments_dict = {}  # Dictionary to store comments

    if reviews:
        for review in reviews["data"]["reviews"]:
            author = review["author"]
            comment = review["content"]

            # Add comment to dictionary
            if author in comments_dict:
                comments_dict[author].append(comment)
            else:
                comments_dict[author] = [comment]

    return comments_dict


# Streamlit app
st.title("Movie Analyzer")

search_query = st.text_input("Enter a movie title:")
if search_query:
    results = search_movie(search_query)
    if results:
        st.write("Search Results:")
        for i, movie in enumerate(results, 1):
            print(movie.get("rating"))
            title = movie.get("title", "N/A")
            year = movie.get("year", "N/A")
            st.write(f"{i}. {title} ({year})")

        chosen_movie_index = st.number_input(
            "Enter the index of the movie you want to get details for:",
            min_value=1,
            max_value=len(results),
        )
        if st.button("Get Details and Comments"):
            chosen_movie_id = results[chosen_movie_index - 1].movieID
            title, year, genres, plot, rating = get_movie_details(chosen_movie_id)
            st.write(f"**Title:** {title}")
            st.write(f"**Year:** {year}")
            st.write(f"**Genres:** {genres}")
            st.write(f"**Plot:** {plot}")
            st.write(f"**Rating:** {rating}")

            comments = get_movie_comments(chosen_movie_id)
            st.write("Comments for the selected movie:")
            for author, comment_list in comments.items():
                st.write(f"Author: {author}")
                for comment in comment_list:
                    st.write(f"Comment: {comment}")
                st.write("---")
    else:
        st.write("No results found for the query.")
