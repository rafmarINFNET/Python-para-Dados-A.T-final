"""
IMDb Top 250 Scraper - Pacote Principal
"""

from .classes import TV, Movie, Series
from .scraping import carregar_config, baixar_html, extrair_titulos, extrair_filmes_completos
from .database import DatabaseManager
from .analysis import analise_completa

__version__ = "1.0.0"
