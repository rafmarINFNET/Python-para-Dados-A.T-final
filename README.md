# Python-para-Dados-A.T

 IMDb Top 250 Scraper

Projeto de Web Scraping, Orientação a Objetos, Banco de Dados e Análise de Dados utilizando a página do IMDb Top 250.

## Descrição do Projeto

Este projeto implementa um sistema completo que:

1. **Web Scraping**: Extrai dados dos 250 melhores filmes do IMDb (título, ano, nota)
2. **Orientação a Objetos**: Utiliza hierarquia de classes (TV → Movie, Series)
3. **Banco de Dados**: Armazena os dados em SQLite usando SQLAlchemy
4. **Análise de Dados**: Processa e analisa os dados usando Pandas
5. **Exportação**: Gera arquivos CSV e JSON com os resultados

## Estrutura do Projeto

```
imdb_project/
├── config.json           # Configurações (URL, número de filmes)
├── requirements.txt      # Dependências do projeto
├── README.md            # Este arquivo
├── .gitignore           # Arquivos a ignorar no Git
├── src/
│   ├── __init__.py      # Inicialização do pacote
│   ├── main.py          # Arquivo principal
│   ├── scraping.py      # Módulo de web scraping
│   ├── classes.py       # Classes TV, Movie, Series
│   ├── database.py      # Gerenciamento do banco de dados
│   └── analysis.py      # Análise de dados com Pandas
└── data/
    ├── imdb.db          # Banco de dados SQLite
    ├── movies.csv       # Exportação de filmes em CSV
    ├── series.csv       # Exportação de séries em CSV
    ├── movies.json      # Exportação de filmes em JSON
    └── series.json      # Exportação de séries em JSON
```

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/rafmarINFNET/Python-para-Dados-A.T-final.git

cd imdb-scraper
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## Como Executar

### Executar o fluxo completo

```bash
cd src
python main.py
```

### Executar módulos individuais

```bash
# Testar as classes
python src/classes.py

# Testar o scraping
python src/scraping.py

# Testar o banco de dados
python src/database.py

# Testar a análise de dados
python src/analysis.py
```

## Configuração

O arquivo `config.json` permite configurar:

- `url`: URL da página do IMDb Top 250
- `n_filmes`: Número máximo de filmes a extrair (padrão: 250)

```json
{
    "url": "https://www.imdb.com/chart/top/",
    "n_filmes": 250
}
```

## Exercícios Implementados

| Exercício | Descrição | Arquivo |
|-----------|-----------|---------|
| 1 | Scraping básico - títulos | `scraping.py` |
| 2 | Título, ano e nota | `scraping.py` |
| 3 | Classe base TV | `classes.py` |
| 4 | Classes Movie e Series | `classes.py` |
| 5 | Lista de objetos | `main.py` |
| 6 | Banco de dados SQLAlchemy | `database.py` |
| 7 | Leitura com Pandas | `analysis.py` |
| 8 | Análise e exportação | `analysis.py` |
| 9 | Classificação textual | `analysis.py` |
| 10 | Resumo por categoria | `analysis.py` |
| 11 | Modularização | Estrutura do projeto |
| 12 | Repositório GitHub | Este repositório |

## Tecnologias Utilizadas

- **Python 3.8+**
- **BeautifulSoup4**: Parsing de HTML
- **Requests**: Requisições HTTP
- **SQLAlchemy**: ORM para banco de dados
- **Pandas**: Análise de dados
- **SQLite**: Banco de dados

## Licença

Este projeto foi desenvolvido para fins educacionais.

## Autor

Desenvolvido como trabalho acadêmico.
