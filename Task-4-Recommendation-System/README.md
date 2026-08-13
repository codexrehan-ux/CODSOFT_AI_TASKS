# Task 4 — Movie Recommendation System

## CodSoft Artificial Intelligence Internship

### Objective

Create a recommendation system that suggests movies based on the characteristics of a movie selected by the user. This project uses a simple content-based filtering approach.

### Features

- Movie title search
- Close title matching for minor spelling differences
- Content-based recommendations
- Genre and keyword profiles
- Similarity scoring
- Top 5 recommendations
- Interactive terminal interface

### Technology

- Python 3
- Standard Python library only

### How It Works

Each movie has a profile containing genres and descriptive keywords. The system converts these terms into normalized word sets and compares the selected movie with every other movie.

A cosine-style similarity score is calculated from the overlap between the two profiles. Movies with higher similarity scores are ranked first.

### How to Run

Make sure Python 3 is installed, then run:

```bash
python recommendation_system.py
```

Choose a movie from the displayed list. For example:

```text
Enter a movie title (or 'exit' to quit): Inception
```

The system then displays the most similar movies and their similarity scores.

### Project Requirement

This project is completed as Task 4 (Recommendation System) of the CodSoft Artificial Intelligence internship.
