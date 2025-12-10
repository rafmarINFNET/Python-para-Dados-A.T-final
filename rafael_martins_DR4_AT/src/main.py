"""
Arquivo Principal - IMDb Top 250 Scraper
Executa o fluxo completo: scraping, classes, banco de dados e analise.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraping import (
    carregar_config,
    baixar_html,
    extrair_titulos,
    extrair_filmes_completos,
    exibir_primeiros_titulos,
    exibir_filmes_formatados,
    carregar_html_local,
    salvar_html_local
)
from classes import TV, Movie, Series
from database import DatabaseManager
from analysis import analise_completa


def executar_exercicio_1_2(config: dict) -> list:
    print("\n" + "="*60)
    print("EXERCICIOS 1 e 2: WEB SCRAPING")
    print("="*60)
    
    url = config.get("url", "https://www.imdb.com/chart/top/")
    n_filmes = config.get("n_filmes", 250)
    
    print(f"\nURL: {url}")
    print(f"Numero maximo de filmes: {n_filmes}")
    
    json_local = "filmes_extraidos.json"
    html_local = "imdb_top250.html"
    
    if os.path.exists(json_local):
        print(f"\nEncontrado arquivo '{json_local}' com dados ja extraidos.")
        resposta = input("Usar dados existentes? (s/n): ").strip().lower()
        if resposta == 's':
            with open(json_local, 'r', encoding='utf-8') as f:
                filmes = json.load(f)
            print(f"Carregados {len(filmes)} filmes do arquivo JSON.")
            titulos = [f['titulo'] for f in filmes]
            exibir_primeiros_titulos(titulos, 10)
            exibir_filmes_formatados(filmes, 5)
            return filmes
    
    try:
        if os.path.exists(html_local):
            print(f"\nCarregando HTML local de '{html_local}'...")
            html = carregar_html_local(html_local)
        else:
            print("\nBaixando pagina do IMDb Top 250...")
            html = baixar_html(url)
            salvar_html_local(html, html_local)
        
        print(f"HTML carregado com sucesso! ({len(html)} caracteres)")
        
        print("\n--- Exercicio 1: Extracao de titulos ---")
        titulos = extrair_titulos(html, n_filmes)
        print(f"Total de titulos extraidos: {len(titulos)}")
        exibir_primeiros_titulos(titulos, 10)
        
        print("\n--- Exercicio 2: Extracao de titulo, ano e nota ---")
        filmes = extrair_filmes_completos(html, n_filmes)
        print(f"Total de filmes com dados completos: {len(filmes)}")
        exibir_filmes_formatados(filmes, 5)
        
        with open(json_local, 'w', encoding='utf-8') as f:
            json.dump(filmes, f, ensure_ascii=False, indent=2)
        print(f"\nDados salvos em '{json_local}'")
        
        return filmes
        
    except Exception as e:
        print(f"\nERRO DURANTE O SCRAPING: {e}")
        print("\nSalve a pagina https://www.imdb.com/chart/top/ como 'imdb_top250.html'")
        
        input("\nPressione ENTER apos salvar o arquivo HTML...")
        
        if os.path.exists(html_local):
            html = carregar_html_local(html_local)
            titulos = extrair_titulos(html, n_filmes)
            filmes = extrair_filmes_completos(html, n_filmes)
            
            exibir_primeiros_titulos(titulos, 10)
            exibir_filmes_formatados(filmes, 5)
            
            with open(json_local, 'w', encoding='utf-8') as f:
                json.dump(filmes, f, ensure_ascii=False, indent=2)
            
            return filmes
        else:
            print(f"\nArquivo '{html_local}' nao encontrado.")
            sys.exit(1)


def executar_exercicio_3_4():
    print("\n" + "="*60)
    print("EXERCICIOS 3 e 4: CLASSES")
    print("="*60)
    
    print("\n--- Exercicio 3: Classe base TV ---")
    tv = TV("Exemplo de Midia", 2020)
    print(f"Objeto TV: {tv}")
    
    print("\n--- Exercicio 4: Classes Movie e Series ---")
    
    movie = Movie("The Shawshank Redemption", 1994, 9.3)
    print(f"Objeto Movie: {movie}")
    
    series = Series("Breaking Bad", 2008, 5, 62)
    print(f"Objeto Series: {series}")
    
    print("\nHeranca verificada:")
    print(f"  - Movie e subclasse de TV: {issubclass(Movie, TV)}")
    print(f"  - Series e subclasse de TV: {issubclass(Series, TV)}")


def executar_exercicio_5(filmes_dados: list) -> list:
    print("\n" + "="*60)
    print("EXERCICIO 5: LISTA DE OBJETOS")
    print("="*60)
    
    catalog = []
    
    print("\n--- Criando objetos Movie a partir do scraping ---")
    for filme in filmes_dados:
        titulo = filme.get('titulo', filme.get('title', ''))
        ano = filme.get('ano', filme.get('year'))
        nota = filme.get('nota', filme.get('rating'))
        
        if titulo and ano is not None and nota is not None:
            movie = Movie(titulo, ano, nota)
            catalog.append(movie)
    
    print(f"Objetos Movie criados: {len(catalog)}")
    
    print("\n--- Criando objetos Series ficticios ---")
    series_ficticias = [
        Series("Breaking Bad", 2008, 5, 62),
        Series("Game of Thrones", 2011, 8, 73),
        Series("The Wire", 2002, 5, 60)
    ]
    
    for serie in series_ficticias:
        catalog.append(serie)
        print(f"  Adicionado: {serie}")
    
    print(f"\n--- Catalogo completo ({len(catalog)} itens) ---")
    print("Primeiros 10 itens:")
    for i, item in enumerate(catalog[:10], 1):
        print(f"  {i}. {item}")
    
    if len(catalog) > 10:
        print(f"  ... e mais {len(catalog) - 10} itens")
    
    return catalog


def executar_exercicio_6(catalog: list, db_path: str):
    print("\n" + "="*60)
    print("EXERCICIO 6: BANCO DE DADOS")
    print("="*60)
    
    db = DatabaseManager(db_path)
    db.conectar()
    
    print("\n--- Inserindo filmes no banco ---")
    filmes_inseridos = 0
    for item in catalog:
        if isinstance(item, Movie) and not isinstance(item, Series):
            try:
                sucesso = db.inserir_filme(item.title, item.year, item.rating)
                if sucesso:
                    filmes_inseridos += 1
            except Exception as e:
                print(f"Erro ao inserir '{item.title}': {e}")
    
    print(f"Filmes inseridos: {filmes_inseridos}")
    
    print("\n--- Inserindo series no banco ---")
    series_inseridas = 0
    for item in catalog:
        if isinstance(item, Series):
            try:
                sucesso = db.inserir_serie(item.title, item.year, item.seasons, item.episodes)
                if sucesso:
                    series_inseridas += 1
            except Exception as e:
                print(f"Erro ao inserir '{item.title}': {e}")
    
    print(f"Series inseridas: {series_inseridas}")
    
    return db


def executar_exercicio_7_8_9_10(db_path: str, output_dir: str):
    print("\n" + "="*60)
    print("EXERCICIOS 7, 8, 9 e 10: ANALISE DE DADOS")
    print("="*60)
    
    df_filmes, df_series = analise_completa(db_path, output_dir)
    
    return df_filmes, df_series


def main():
    print("\n" + "#"*60)
    print("#" + "   IMDb Top 250 - Projeto AT".center(58) + "#")
    print("#"*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    config_path = os.path.join(project_dir, "config.json")
    db_path = os.path.join(project_dir, "data", "imdb.db")
    output_dir = os.path.join(project_dir, "data")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Remover banco antigo para recriar
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Banco de dados anterior removido.")
    
    print("\n--- Carregando configuracao ---")
    config = carregar_config(config_path)
    print(f"URL: {config.get('url')}")
    print(f"Numero de filmes: {config.get('n_filmes')}")
    
    filmes_dados = executar_exercicio_1_2(config)
    
    executar_exercicio_3_4()
    
    catalog = executar_exercicio_5(filmes_dados)
    
    executar_exercicio_6(catalog, db_path)
    
    executar_exercicio_7_8_9_10(db_path, output_dir)
    
    print("\n" + "="*60)
    print("EXECUCAO CONCLUIDA")
    print("="*60)
    print(f"\nArquivos gerados em: {output_dir}")
    print("  - imdb.db (banco de dados SQLite)")
    print("  - movies.csv")
    print("  - series.csv")
    print("  - movies.json")
    print("  - series.json")


if __name__ == "__main__":
    main()
