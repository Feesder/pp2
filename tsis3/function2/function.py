movies = [
{
"name": "Usual Suspects",
"imdb": 7.0,
"category": "Thriller"
},
{
"name": "Hitman",
"imdb": 6.3,
"category": "Action"
},
{
"name": "Dark Knight",
"imdb": 9.0,
"category": "Adventure"
},
{
"name": "The Help",
"imdb": 8.0,
"category": "Drama"
},
{
"name": "The Choice",
"imdb": 6.2,
"category": "Romance"
},
{
"name": "Colonia",
"imdb": 7.4,
"category": "Romance"
},
{
"name": "Love",
"imdb": 6.0,
"category": "Romance"
},
{
"name": "Bride Wars",
"imdb": 5.4,
"category": "Romance"
},
{
"name": "AlphaJet",
"imdb": 3.2,
"category": "War"
},
{
"name": "Ringing Crime",
"imdb": 4.0,
"category": "Crime"
},
{
"name": "Joking muck",
"imdb": 7.2,
"category": "Comedy"
},
{
"name": "What is the name",
"imdb": 9.2,
"category": "Suspense"
},
{
"name": "Detective",
"imdb": 7.0,
"category": "Suspense"
},
{
"name": "Exam",
"imdb": 4.2,
"category": "Thriller"
},
{
"name": "We Two",
"imdb": 7.2,
"category": "Romance"
}
]


def rating(movie: dict, score: float) -> bool:
    if movie["imdb"] > score:
        return True

    return False


def ratingList(movies: list[dict], score: float) -> list[dict]:
    res = []
    for i in range(len(movies)):
        if movies[i]['imdb'] > score:
            res.append(movies[i])

    return res


def moviesByCategory(movies: list[dict], category: str) -> list[dict]:
    res = []
    for i in range(len(movies)):
        if movies[i]['category'] == category:
            res.append(movies[i])

    return res


def averageScore(movies: list[dict]) -> float:
    numbers = 0
    scores = 0
    for i in range(len(movies)):
        scores += movies[i]['imdb']
        numbers += 1

    return scores / numbers


def averageScoreByCategory(movies: list[dict], category: str) -> float:
    numbers = 0
    scores = 0
    for i in range(len(movies)):
        if movies[i]['category'] == category:
            scores += movies[i]['imdb']
            numbers += 1

    return scores / numbers


print(rating(movies[0], 5.5))
print(ratingList(movies, 5.5))
print(moviesByCategory(movies, "Thriller"))
print(averageScore(movies))
print(averageScoreByCategory(movies, "Thriller"))