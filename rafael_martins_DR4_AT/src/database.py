"""
Modulo de Banco de Dados com SQLAlchemy.
Exercicio 6: Criacao do banco imdb.db com tabelas movies e series.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
import os

Base = declarative_base()


class MovieDB(Base):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False, unique=True)
    year = Column(Integer)
    rating = Column(Float)
    
    def __repr__(self):
        return f"<MovieDB(id={self.id}, title='{self.title}', year={self.year}, rating={self.rating})>"


class SeriesDB(Base):
    __tablename__ = 'series'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False, unique=True)
    year = Column(Integer)
    seasons = Column(Integer)
    episodes = Column(Integer)
    
    def __repr__(self):
        return f"<SeriesDB(id={self.id}, title='{self.title}', year={self.year}, seasons={self.seasons}, episodes={self.episodes})>"


class DatabaseManager:
    def __init__(self, db_path: str = "data/imdb.db"):
        self.db_path = db_path
        self.engine = None
        self.Session = None
        
    def conectar(self) -> None:
        try:
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            self.engine = create_engine(f'sqlite:///{self.db_path}', echo=False)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            
            print(f"Banco de dados '{self.db_path}' conectado com sucesso.")
            
        except SQLAlchemyError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise
    
    def inserir_filme(self, title: str, year: int, rating: float) -> bool:
        try:
            session = self.Session()
            filme = MovieDB(title=title, year=year, rating=rating)
            session.add(filme)
            session.commit()
            session.close()
            return True
            
        except IntegrityError:
            session.rollback()
            session.close()
            return False
            
        except SQLAlchemyError as e:
            session.rollback()
            session.close()
            print(f"Erro ao inserir filme '{title}': {e}")
            return False
    
    def inserir_filmes_em_lote(self, filmes: List[dict]) -> int:
        inseridos = 0
        for filme in filmes:
            try:
                titulo = filme.get('titulo', filme.get('title', ''))
                ano = filme.get('ano', filme.get('year'))
                nota = filme.get('nota', filme.get('rating'))
                
                if titulo and ano is not None and nota is not None:
                    sucesso = self.inserir_filme(title=titulo, year=ano, rating=nota)
                    if sucesso:
                        inseridos += 1
            except Exception as e:
                print(f"Erro ao inserir filme: {e}")
                continue
        
        print(f"Total de filmes inseridos: {inseridos}/{len(filmes)}")
        return inseridos
    
    def inserir_serie(self, title: str, year: int, seasons: int, episodes: int) -> bool:
        try:
            session = self.Session()
            serie = SeriesDB(title=title, year=year, seasons=seasons, episodes=episodes)
            session.add(serie)
            session.commit()
            session.close()
            return True
            
        except IntegrityError:
            session.rollback()
            session.close()
            return False
            
        except SQLAlchemyError as e:
            session.rollback()
            session.close()
            print(f"Erro ao inserir serie '{title}': {e}")
            return False
    
    def consultar_filmes(self) -> List[MovieDB]:
        try:
            session = self.Session()
            filmes = session.query(MovieDB).all()
            session.close()
            return filmes
        except SQLAlchemyError as e:
            print(f"Erro ao consultar filmes: {e}")
            return []
    
    def consultar_series(self) -> List[SeriesDB]:
        try:
            session = self.Session()
            series = session.query(SeriesDB).all()
            session.close()
            return series
        except SQLAlchemyError as e:
            print(f"Erro ao consultar series: {e}")
            return []
    
    def get_engine(self):
        return self.engine


if __name__ == "__main__":
    print("=== Teste do Modulo de Banco de Dados ===\n")
    
    db = DatabaseManager("../data/imdb.db")
    db.conectar()
    
    filmes_teste = [
        {"titulo": "The Shawshank Redemption", "ano": 1994, "nota": 9.3},
        {"titulo": "The Godfather", "ano": 1972, "nota": 9.2},
    ]
    
    db.inserir_filmes_em_lote(filmes_teste)
    db.inserir_serie("Breaking Bad", 2008, 5, 62)
    
    print("\n=== Filmes no Banco ===")
    for filme in db.consultar_filmes():
        print(filme)
    
    print("\n=== Series no Banco ===")
    for serie in db.consultar_series():
        print(serie)
