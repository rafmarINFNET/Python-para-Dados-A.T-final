"""
Modulo de Classes para representacao de midias de TV/Cinema.
Exercicios 3 e 4: Classe base TV e classes especializadas Movie e Series.
"""


class TV:
    def __init__(self, title: str, year: int):
        self.title = title
        self.year = year
    
    def __str__(self) -> str:
        return f"{self.title} ({self.year})"
    
    def __repr__(self) -> str:
        return f"TV(title='{self.title}', year={self.year})"


class Movie(TV):
    def __init__(self, title: str, year: int, rating: float):
        super().__init__(title, year)
        self.rating = rating
    
    def __str__(self) -> str:
        return f"{self.title} ({self.year}) - Nota: {self.rating}"
    
    def __repr__(self) -> str:
        return f"Movie(title='{self.title}', year={self.year}, rating={self.rating})"


class Series(TV):
    def __init__(self, title: str, year: int, seasons: int, episodes: int):
        super().__init__(title, year)
        self.seasons = seasons
        self.episodes = episodes
    
    def __str__(self) -> str:
        return f"{self.title} ({self.year}) - Temporadas: {self.seasons}, Episodios: {self.episodes}"
    
    def __repr__(self) -> str:
        return f"Series(title='{self.title}', year={self.year}, seasons={self.seasons}, episodes={self.episodes})"


if __name__ == "__main__":
    print("=== Teste das Classes ===\n")
    
    tv = TV("Exemplo TV", 2020)
    print(f"TV: {tv}")
    
    movie = Movie("The Shawshank Redemption", 1994, 9.3)
    print(f"Movie: {movie}")
    
    series = Series("Breaking Bad", 2008, 5, 62)
    print(f"Series: {series}")
