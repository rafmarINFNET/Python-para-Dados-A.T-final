"""
Modulo de Analise de Dados com Pandas.
Exercicios 7, 8, 9 e 10: Leitura do banco, analise e exportacao.
"""

import pandas as pd
from sqlalchemy import create_engine
from typing import Tuple
import os


def criar_conexao(db_path: str = "data/imdb.db"):
    try:
        engine = create_engine(f'sqlite:///{db_path}')
        return engine
    except Exception as e:
        print(f"Erro ao criar conexao: {e}")
        raise


def carregar_filmes(engine) -> pd.DataFrame:
    try:
        df = pd.read_sql_table('movies', engine)
        return df
    except Exception as e:
        print(f"Erro ao carregar filmes: {e}")
        return pd.DataFrame()


def carregar_series(engine) -> pd.DataFrame:
    try:
        df = pd.read_sql_table('series', engine)
        return df
    except Exception as e:
        print(f"Erro ao carregar series: {e}")
        return pd.DataFrame()


def exibir_primeiras_linhas(df: pd.DataFrame, nome: str, n: int = 5) -> None:
    print(f"\n=== {nome} - Primeiras {n} linhas ===")
    print(df.head(n).to_string(index=False))


def ordenar_por_nota(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(by='rating', ascending=False)


def filtrar_nota_maior_que(df: pd.DataFrame, nota_minima: float = 9.0) -> pd.DataFrame:
    return df[df['rating'] > nota_minima]


def exportar_csv(df: pd.DataFrame, caminho: str) -> bool:
    try:
        diretorio = os.path.dirname(caminho)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        df.to_csv(caminho, index=False, encoding='utf-8')
        print(f"Arquivo CSV exportado: {caminho}")
        return True
    except Exception as e:
        print(f"Erro ao exportar CSV '{caminho}': {e}")
        return False


def exportar_json(df: pd.DataFrame, caminho: str) -> bool:
    try:
        diretorio = os.path.dirname(caminho)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        df.to_json(caminho, orient='records', indent=2, force_ascii=False)
        print(f"Arquivo JSON exportado: {caminho}")
        return True
    except Exception as e:
        print(f"Erro ao exportar JSON '{caminho}': {e}")
        return False


def classificar_nota(nota: float) -> str:
    if nota is None or pd.isna(nota):
        return "Sem classificacao"
    elif nota >= 9.0:
        return "Obra-prima"
    elif nota >= 8.0:
        return "Excelente"
    elif nota >= 7.0:
        return "Bom"
    else:
        return "Mediano"


def adicionar_coluna_categoria(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['categoria'] = df['rating'].apply(classificar_nota)
    return df


def exibir_titulo_rating_categoria(df: pd.DataFrame, n: int = 10) -> None:
    colunas = ['title', 'rating', 'categoria']
    colunas_existentes = [c for c in colunas if c in df.columns]
    
    print(f"\n=== Primeiros {n} filmes (titulo, nota, categoria) ===")
    print(df[colunas_existentes].head(n).to_string(index=False))


def criar_resumo_categoria_ano(df: pd.DataFrame) -> pd.DataFrame:
    if 'categoria' not in df.columns:
        df = adicionar_coluna_categoria(df)
    
    resumo = pd.crosstab(
        df['year'], 
        df['categoria'],
        margins=True,
        margins_name='Total'
    )
    
    return resumo


def analise_completa(db_path: str = "data/imdb.db", output_dir: str = "data/") -> Tuple[pd.DataFrame, pd.DataFrame]:
    print("\n" + "="*60)
    print("ANALISE DE DADOS - IMDb Top 250")
    print("="*60)
    
    print("\n--- Exercicio 7: Carregando dados do banco ---")
    try:
        engine = criar_conexao(db_path)
        df_filmes = carregar_filmes(engine)
        df_series = carregar_series(engine)
        
        exibir_primeiras_linhas(df_filmes, "Filmes", 5)
        exibir_primeiras_linhas(df_series, "Series", 5)
    except Exception as e:
        print(f"Erro ao acessar o banco: {e}")
        return pd.DataFrame(), pd.DataFrame()
    
    print("\n--- Exercicio 8: Analise e exportacao ---")
    
    df_filmes_ordenado = ordenar_por_nota(df_filmes)
    print("\nFilmes ordenados por nota (top 5):")
    print(df_filmes_ordenado.head().to_string(index=False))
    
    df_filmes_filtrado = filtrar_nota_maior_que(df_filmes_ordenado, 9.0)
    print(f"\nFilmes com nota > 9.0: {len(df_filmes_filtrado)} encontrados")
    if len(df_filmes_filtrado) > 0:
        print(df_filmes_filtrado.head().to_string(index=False))
    
    try:
        exportar_csv(df_filmes, os.path.join(output_dir, "movies.csv"))
        exportar_csv(df_series, os.path.join(output_dir, "series.csv"))
    except Exception as e:
        print(f"Erro ao exportar CSV: {e}")
    
    try:
        exportar_json(df_filmes, os.path.join(output_dir, "movies.json"))
        exportar_json(df_series, os.path.join(output_dir, "series.json"))
    except Exception as e:
        print(f"Erro ao exportar JSON: {e}")
    
    print("\n--- Exercicio 9: Classificacao textual das notas ---")
    df_filmes = adicionar_coluna_categoria(df_filmes)
    exibir_titulo_rating_categoria(df_filmes, 10)
    
    print("\n--- Exercicio 10: Resumo de filmes por categoria e ano ---")
    resumo = criar_resumo_categoria_ano(df_filmes)
    print("\nResumo de filmes por categoria e ano de lancamento:")
    print(resumo.to_string())
    
    return df_filmes, df_series


if __name__ == "__main__":
    df_filmes, df_series = analise_completa("../data/imdb.db", "../data/")
