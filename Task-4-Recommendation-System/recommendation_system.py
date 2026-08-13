"""CodSoft AI Internship - Task 4
Content-based movie recommendation system.
"""

import difflib
import math
import re

MOVIES = [
    {"title": "The Dark Knight", "genres": "action crime drama", "keywords": "batman joker hero vigilante"},
    {"title": "Batman Begins", "genres": "action crime drama", "keywords": "batman origin hero vigilante"},
    {"title": "The Dark Knight Rises", "genres": "action crime drama", "keywords": "batman bane hero gotham vigilante"},
    {"title": "Inception", "genres": "action sci-fi thriller", "keywords": "dream mind heist technology"},
    {"title": "Interstellar", "genres": "adventure drama sci-fi", "keywords": "space time science exploration future"},
    {"title": "The Martian", "genres": "adventure drama sci-fi", "keywords": "space mars survival science astronaut"},
    {"title": "The Prestige", "genres": "drama mystery thriller", "keywords": "magic rivalry mystery illusion obsession"},
    {"title": "Avengers: Endgame", "genres": "action adventure sci-fi", "keywords": "superhero marvel time travel heroes battle"},
    {"title": "Iron Man", "genres": "action adventure sci-fi", "keywords": "superhero technology marvel hero"},
    {"title": "Guardians of the Galaxy", "genres": "action adventure comedy sci-fi", "keywords": "superhero marvel space team comedy"},
    {"title": "Toy Story", "genres": "animation adventure comedy", "keywords": "toys friendship family adventure"},
    {"title": "Finding Nemo", "genres": "animation adventure family", "keywords": "ocean fish family friendship journey"},
    {"title": "The Lion King", "genres": "animation adventure drama", "keywords": "animals family friendship king journey"},
    {"title": "The Matrix", "genres": "action sci-fi thriller", "keywords": "technology virtual reality hero future"},
    {"title": "Jurassic Park", "genres": "adventure sci-fi thriller", "keywords": "dinosaurs science island survival"},
]


def tokenize(text):
    """Convert text into a set of normalized words."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def movie_profile(movie):
    """Create a searchable profile from a movie's genres and keywords."""
    return tokenize(f"{movie['genres']} {movie['keywords']}")


def similarity(profile_a, profile_b):
    """Calculate cosine similarity between two binary word profiles."""
    intersection = len(profile_a & profile_b)
    if not profile_a or not profile_b:
        return 0.0
    return intersection / math.sqrt(len(profile_a) * len(profile_b))


def find_movie(title):
    """Find an exact or close movie-title match."""
    titles = [movie["title"] for movie in MOVIES]
    normalized = title.strip().lower()

    for movie in MOVIES:
        if movie["title"].lower() == normalized:
            return movie

    matches = difflib.get_close_matches(title.strip(), titles, n=1, cutoff=0.55)
    if matches:
        return next(movie for movie in MOVIES if movie["title"] == matches[0])
    return None


def recommend(title, limit=5):
    """Return the most similar movies for the selected title."""
    selected = find_movie(title)
    if selected is None:
        return None, []

    selected_profile = movie_profile(selected)
    scored = []

    for movie in MOVIES:
        if movie["title"] == selected["title"]:
            continue
        score = similarity(selected_profile, movie_profile(movie))
        scored.append((score, movie["title"]))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return selected, scored[:limit]


def main():
    print("=" * 55)
    print("       CODSOFT - MOVIE RECOMMENDATION SYSTEM")
    print("=" * 55)
    print("This system uses content-based filtering.\n")
    print("Available movies:")
    for movie in MOVIES:
        print(f"- {movie['title']}")

    while True:
        title = input("\nEnter a movie title (or 'exit' to quit): ").strip()
        if title.lower() in {"exit", "quit", "bye"}:
            print("Goodbye!")
            break

        selected, recommendations = recommend(title)
        if selected is None:
            print("Movie not found. Please enter a title from the list or a similar spelling.")
            continue

        print(f"\nBecause you selected: {selected['title']}")
        print("Recommended movies:")
        for number, (score, movie_title) in enumerate(recommendations, start=1):
            print(f"{number}. {movie_title} (similarity: {score:.2f})")


if __name__ == "__main__":
    main()
