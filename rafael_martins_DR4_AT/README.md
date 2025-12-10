# IMDb Top 250 Scraper

Projeto de Web Scraping, Orientacao a Objetos, Banco de Dados e Analise de Dados.

## Estrutura do Projeto

```
imdb_project/
├── config.json
├── requirements.txt
├── src/
│   ├── main.py          # Arquivo principal
│   ├── scraping.py      # Web scraping (Ex. 1-2)
│   ├── classes.py       # Classes (Ex. 3-4)
│   ├── database.py      # Banco de dados (Ex. 6)
│   └── analysis.py      # Analise Pandas (Ex. 7-10)
└── data/
    ├── imdb.db          # Banco SQLite
    ├── movies.csv
    ├── movies.json
    ├── series.csv
    └── series.json
```

## Instalacao

```bash
pip install -r requirements.txt
```

## Execucao

```bash
cd src
python main.py
```

Se o scraping falhar, salve a pagina https://www.imdb.com/chart/top/ como `imdb_top250.html` na pasta `src/`.

## Tecnologias

- Python 3
- BeautifulSoup4
- SQLAlchemy
- Pandas
