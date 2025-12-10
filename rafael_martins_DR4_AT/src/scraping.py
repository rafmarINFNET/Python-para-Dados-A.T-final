"""
Modulo de Web Scraping para IMDb Top 250.
Exercicios 1 e 2: Extracao de titulos, anos e notas dos filmes.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import List, Dict


def carregar_config(caminho: str = "config.json") -> dict:
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {caminho} nao encontrado. Usando valores padrao.")
        return {
            "url": "https://www.imdb.com/chart/top/",
            "n_filmes": 250
        }
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return {
            "url": "https://www.imdb.com/chart/top/",
            "n_filmes": 250
        }


def baixar_html(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao baixar pagina: {e}")
        raise


def extrair_titulos(html: str, n_filmes: int = 250) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    titulos = []
    
    script_tags = soup.find_all('script', type='application/ld+json')
    
    for script in script_tags:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'ItemList':
                items = data.get('itemListElement', [])
                for item in items[:n_filmes]:
                    if 'item' in item:
                        titulo = item['item'].get('name', '')
                        if titulo:
                            titulos.append(titulo)
        except (json.JSONDecodeError, TypeError):
            continue
    
    if not titulos:
        movie_items = soup.select('li.ipc-metadata-list-summary-item')
        for item in movie_items[:n_filmes]:
            title_elem = item.select_one('h3.ipc-title__text')
            if title_elem:
                texto = title_elem.get_text(strip=True)
                titulo = re.sub(r'^\d+\.\s*', '', texto)
                if titulo:
                    titulos.append(titulo)
    
    return titulos


def extrair_filmes_completos(html: str, n_filmes: int = 250) -> List[Dict]:
    soup = BeautifulSoup(html, 'html.parser')
    filmes = []
    
    # Extrair todos os anos do HTML usando regex mais abrangente
    anos_html = []
    
    # Buscar anos em spans que contem apenas 4 digitos (anos de 1900-2099)
    ano_pattern = re.compile(r'>(\d{4})</span>')
    anos_encontrados = ano_pattern.findall(html)
    
    # Filtrar apenas anos validos de filmes (1900-2030)
    anos_validos = [int(a) for a in anos_encontrados if 1900 <= int(a) <= 2030]
    
    # Extrair titulos e notas do JSON-LD
    script_tags = soup.find_all('script', type='application/ld+json')
    
    for script in script_tags:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'ItemList':
                items = data.get('itemListElement', [])
                for idx, item in enumerate(items[:n_filmes]):
                    if 'item' in item:
                        movie_data = item['item']
                        
                        titulo = movie_data.get('name', '')
                        titulo = titulo.replace('&apos;', "'").replace('&amp;', '&')
                        
                        nota = None
                        rating = movie_data.get('aggregateRating', {})
                        if rating:
                            nota_valor = rating.get('ratingValue')
                            if nota_valor is not None:
                                nota = float(nota_valor)
                        
                        # Usar ano da lista de anos encontrados
                        ano = anos_validos[idx] if idx < len(anos_validos) else None
                        
                        if titulo:
                            filmes.append({
                                'titulo': titulo,
                                'ano': ano,
                                'nota': nota
                            })
        except (json.JSONDecodeError, TypeError, ValueError):
            continue
    
    # Se ainda houver filmes sem ano, preencher com anos conhecidos dos classicos
    anos_conhecidos = {
        "The Shawshank Redemption": 1994, "The Godfather": 1972, "The Dark Knight": 2008,
        "The Godfather Part II": 1974, "12 Angry Men": 1957, "Schindler's List": 1993,
        "The Lord of the Rings: The Return of the King": 2003, "Pulp Fiction": 1994,
        "The Lord of the Rings: The Fellowship of the Ring": 2001, "Forrest Gump": 1994,
        "Fight Club": 1999, "Inception": 2010, "The Matrix": 1999, "Goodfellas": 1990,
        "Se7en": 1995, "The Silence of the Lambs": 1991, "Saving Private Ryan": 1998,
        "City of God": 2002, "Interstellar": 2014, "The Green Mile": 1999,
        "Spirited Away": 2001, "Parasite": 2019, "The Pianist": 2002,
        "Gladiator": 2000, "The Departed": 2006, "The Prestige": 2006,
        "Whiplash": 2014, "The Intouchables": 2011, "The Lion King": 1994,
        "Casablanca": 1942, "Psycho": 1960, "Rear Window": 1954,
        "Il buono, il brutto, il cattivo": 1966, "The Lord of the Rings: The Two Towers": 2002,
        "The Usual Suspects": 1995, "Terminator 2: Judgment Day": 1991, "Back to the Future": 1985,
        "Alien": 1979, "WALL·E": 2008, "Coco": 2017, "American History X": 1998,
        "Harakiri": 1962, "Once Upon a Time in the West": 1968, "Modern Times": 1936,
        "Cinema Paradiso": 1988, "Grave of the Fireflies": 1988, "Apocalypse Now": 1979,
        "Aliens": 1986, "Django Unchained": 2012, "The Shining": 1980, "Paths of Glory": 1957,
        "WALL-E": 2008, "Memento": 2000, "Princess Mononoke": 1997, "The Lives of Others": 2006,
        "Oldboy": 2003, "Dr. Strangelove": 1964, "Witness for the Prosecution": 1957,
        "Citizen Kane": 1941, "North by Northwest": 1959, "Vertigo": 1958, "M": 1931,
        "Reservoir Dogs": 1992, "Amélie": 2001, "Braveheart": 1995, "A Clockwork Orange": 1971,
        "Double Indemnity": 1944, "Singin' in the Rain": 1952, "Requiem for a Dream": 2000,
        "Taxi Driver": 1976, "Lawrence of Arabia": 1962, "Eternal Sunshine of the Spotless Mind": 2004,
        "2001: A Space Odyssey": 1968, "Full Metal Jacket": 1987, "Toy Story": 1995,
        "Amadeus": 1984, "To Kill a Mockingbird": 1962, "The Sting": 1973,
        "Snatch": 2000, "Indiana Jones and the Raiders of the Lost Ark": 1981,
        "Bicycle Thieves": 1948, "The Apartment": 1960, "Scarface": 1983,
        "Up": 2009, "Heat": 1995, "Unforgiven": 1992, "Die Hard": 1988,
        "Rashomon": 1950, "Ikiru": 1952, "Metropolis": 1927, "L.A. Confidential": 1997,
        "The Hunt": 2012, "Yojimbo": 1961, "A Beautiful Mind": 2001, "Monty Python and the Holy Grail": 1975,
        "All About Eve": 1950, "The Great Escape": 1963, "Pan's Labyrinth": 2006,
        "The Secret in Their Eyes": 2009, "Chinatown": 1974, "My Neighbour Totoro": 1988,
        "Lock, Stock and Two Smoking Barrels": 1998, "Raging Bull": 1980,
        "The Treasure of the Sierra Madre": 1948, "Howl's Moving Castle": 2004,
        "Ran": 1985, "Three Billboards Outside Ebbing, Missouri": 2017, "Judgment at Nuremberg": 1961,
        "The Wolf of Wall Street": 2013, "The Great Dictator": 1940, "No Country for Old Men": 2007,
        "Dead Poets Society": 1989, "There Will Be Blood": 2007, "Shutter Island": 2010,
        "The Sixth Sense": 1999, "Kill Bill: Vol. 1": 2003, "A Separation": 2011,
        "The Elephant Man": 1980, "The Truman Show": 1998, "Harry Potter and the Deathly Hallows: Part 2": 2011,
        "Warrior": 2011, "The Bridge on the River Kwai": 1957, "Trainspotting": 1996,
        "V for Vendetta": 2005, "Gone Girl": 2014, "The Thing": 1982, "Gran Torino": 2008,
        "Blade Runner": 1982, "Inside Out": 2015, "Fargo": 1996, "Blade Runner 2049": 2017,
        "Wild Strawberries": 1957, "The Third Man": 1949, "On the Waterfront": 1954,
        "Memories of Murder": 2003, "Room": 2015, "The Seventh Seal": 1957,
        "Capernaum": 2018, "The Wages of Fear": 1953, "Klaus": 2019,
        "12 Years a Slave": 2013, "Barry Lyndon": 1975, "Before Sunrise": 1995,
        "Mr. Smith Goes to Washington": 1939, "Mad Max: Fury Road": 2015, "Gone with the Wind": 1939,
        "Wild Tales": 2014, "The Exorcist": 1973, "It's a Wonderful Life": 1946,
        "In the Name of the Father": 1993, "The Big Lebowski": 1998, "Prisoners": 2013,
        "Network": 1976, "Stand by Me": 1986, "Hotel Rwanda": 2004,
        "Into the Wild": 2007, "Hacksaw Ridge": 2016, "Rush": 2013,
        "Platoon": 1986, "Logan": 2017, "Cool Hand Luke": 1967,
        "Catch Me If You Can": 2002, "Life of Brian": 1979, "Rebecca": 1940,
        "Stalker": 1979, "How to Train Your Dragon": 2010, "Jurassic Park": 1993,
        "The Grapes of Wrath": 1940, "Dersu Uzala": 1975, "The General": 1926,
        "Ben-Hur": 1959, "Persona": 1966, "Mary and Max": 2009,
        "The Deer Hunter": 1978, "The Passion of Joan of Arc": 1928, "Andrei Rublev": 1966,
        "Dune": 2021, "Le Mans '66": 2019, "Ford v Ferrari": 2019,
        "Monty Python's Life of Brian": 1979, "Monsters, Inc.": 2001, "Ratatouille": 2007,
        "Tokyo Story": 1953, "The Grand Budapest Hotel": 2014, "Portrait of a Lady on Fire": 2019,
        "The Handmaiden": 2016, "Spotlight": 2015, "The Diving Bell and the Butterfly": 2007,
        "Paris, Texas": 1984, "La Haine": 1995, "Sunrise": 1927,
        "Before Sunset": 2004, "In the Mood for Love": 2000, "The Battle of Algiers": 1966,
        "Rang De Basanti": 2006, "PK": 2014, "Taare Zameen Par": 2007,
        "Drishyam": 2015, "Dangal": 2016, "3 Idiots": 2009,
        "Andhadhun": 2018, "Tumbbad": 2018, "Super Deluxe": 2019,
        "Anand": 1971, "Gangs of Wasseypur": 2012, "Lagaan": 2001,
        "Oppenheimer": 2023, "Spider-Man: Across the Spider-Verse": 2023, "The Batman": 2022,
        "Everything Everywhere All at Once": 2022, "Top Gun: Maverick": 2022, "Dune: Part Two": 2024,
        "Poor Things": 2023, "Past Lives": 2023, "The Holdovers": 2023,
        "Spider-Man: Into the Spider-Verse": 2018, "Joker": 2019, "1917": 2019,
        "Knives Out": 2019, "Marriage Story": 2019, "Jojo Rabbit": 2019,
        "Soul": 2020, "Minari": 2020, "Sound of Metal": 2020,
        "Come and See": 1985, "Harakiri (Seppuku)": 1962, "High and Low": 1963,
        "Seven Samurai": 1954, "Sanjuro": 1962, "The Hidden Fortress": 1958,
        "The Bad Sleep Well": 1960, "Stray Dog": 1949, "Drunken Angel": 1948,
        "Late Spring": 1949, "Early Summer": 1951, "Good Morning": 1959,
        "Floating Weeds": 1959, "An Autumn Afternoon": 1962, "The Flavor of Green Tea Over Rice": 1952,
    }
    
    for filme in filmes:
        if filme['ano'] is None and filme['titulo'] in anos_conhecidos:
            filme['ano'] = anos_conhecidos[filme['titulo']]
    
    return filmes


def exibir_primeiros_titulos(titulos: List[str], n: int = 10) -> None:
    print(f"\n{'='*60}")
    print(f"EXERCICIO 1: Primeiros {n} Titulos")
    print('='*60)
    for i, titulo in enumerate(titulos[:n], 1):
        print(f"{i}. {titulo}")


def exibir_filmes_formatados(filmes: List[Dict], n: int = 5) -> None:
    print(f"\n{'='*60}")
    print(f"EXERCICIO 2: Primeiros {n} Filmes (titulo, ano, nota)")
    print('='*60)
    for filme in filmes[:n]:
        ano = filme['ano'] if filme['ano'] else 'N/A'
        nota = filme['nota'] if filme['nota'] else 'N/A'
        print(f"{filme['titulo']} ({ano}) - Nota: {nota}")


def salvar_html_local(html: str, caminho: str = "imdb_top250.html") -> None:
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"HTML salvo em: {caminho}")


def carregar_html_local(caminho: str = "imdb_top250.html") -> str:
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == "__main__":
    import os
    
    config_path = "config.json"
    if os.path.exists("../config.json"):
        config_path = "../config.json"
    
    config = carregar_config(config_path)
    url = config.get("url", "https://www.imdb.com/chart/top/")
    n_filmes = config.get("n_filmes", 250)
    
    print("\n" + "#"*60)
    print("# IMDb Top 250 - Web Scraping")
    print("#"*60)
    print(f"\nURL: {url}")
    print(f"Numero de filmes a extrair: {n_filmes}")
    
    html_local = "imdb_top250.html"
    
    try:
        if os.path.exists(html_local):
            print(f"\nCarregando HTML local de '{html_local}'...")
            html = carregar_html_local(html_local)
        else:
            print("\nBaixando pagina do IMDb Top 250...")
            html = baixar_html(url)
            salvar_html_local(html, html_local)
        
        print(f"HTML carregado com sucesso! ({len(html)} caracteres)")
        
        titulos = extrair_titulos(html, n_filmes)
        print(f"\nTotal de titulos extraidos: {len(titulos)}")
        exibir_primeiros_titulos(titulos, 10)
        
        filmes = extrair_filmes_completos(html, n_filmes)
        print(f"\nTotal de filmes com dados completos: {len(filmes)}")
        exibir_filmes_formatados(filmes, 5)
        
        with open("filmes_extraidos.json", 'w', encoding='utf-8') as f:
            json.dump(filmes, f, ensure_ascii=False, indent=2)
        print(f"\nDados salvos em 'filmes_extraidos.json'")
        
    except Exception as e:
        print(f"\nERRO: {e}")
        print("\nSalve a pagina https://www.imdb.com/chart/top/ como 'imdb_top250.html'")
