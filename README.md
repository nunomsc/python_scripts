# Image Downloader - fapello_image_download.py

Este script Python permite fazer o download automático de imagens sequenciais de uma coleção específica da internet.

## Funcionalidades

- Faz download de imagens de URLs sequenciais.
- Salva as imagens em uma pasta local especificada.
- Garante que os arquivos sejam nomeados de forma consistente.
- Trata erros e status HTTP, informando se algum download falhar.

## Pré-requisitos

- Python 3.x
- Biblioteca `requests`

Instale a biblioteca `requests` (se ainda não tiver):

```bash
pip install requests
```
--------------------------------------------------------------------------------------------------------------------------

# GOG Product Titles Scraper - scrap-gog.py

Este script Python permite extrair títulos de jogos do site [GOG.com](https://www.gog.com/) e salvá-los em um arquivo CSV.

## Funcionalidades

- Faz scraping de páginas sequenciais de jogos no GOG.
- Extrai apenas os títulos dos produtos.
- Salva os dados em um arquivo CSV.
- Adiciona um atraso aleatório entre as requisições para evitar bloqueios.

## Pré-requisitos

- Python 3.x
- Bibliotecas:
  - `requests`
  - `beautifulsoup4`

Instale as dependências usando:

```bash
pip install requests beautifulsoup4
```
--------------------------------------------------------------------------------------------------------------------------

# Steam Game Info Scraper - scrap_steam.py

Este script Python permite buscar informações detalhadas de qualquer jogo na Steam usando seu **AppID** e gerar um ficheiro HTML com os dados e imagens.

## Funcionalidades

- Busca dados gerais do jogo (título, desenvolvedor, publisher, preço, gêneros, data de lançamento).
- Busca e limpa o conteúdo de "About this game".
- Faz download de imagens do jogo (header, capsule e screenshots).
- Busca resumos de reviews (pontuação, total de reviews, positivos e negativos).
- Extrai requisitos mínimos e recomendados do sistema.
- Gera um ficheiro HTML estilizado com todas as informações.

## Pré-requisitos

- Python 3.x
- Bibliotecas:
  - `requests`
  - `beautifulsoup4`

Instale as dependências:

```bash
pip install requests beautifulsoup4
```
--------------------------------------------------------------------------------------------------------------------------

# Video Downloader Script - video_downloader.py

Este script Python permite baixar vídeos de uma página web usando Selenium e BeautifulSoup.

## Funcionalidades

- Abre a página em um navegador headless usando SeleniumBase.
- Procura elementos `<video>` e captura o URL do vídeo.
- Ignora vídeos do tipo `blob` ou galerias.
- Salva o vídeo localmente com um nome limpo baseado na URL.

## Pré-requisitos

- Python 3.x
- Bibliotecas:
  - `requests`
  - `beautifulsoup4`
  - `seleniumbase`
  - `rich`

Instale as dependências:

```bash
pip install requests beautifulsoup4 seleniumbase rich
```
--------------------------------------------------------------------------------------------------------------------------

# Steam Game API with Cache - steam_api.py

Esta API em **FastAPI** permite buscar informações detalhadas de jogos na Steam usando o **AppID** e retorna os dados em formato JSON. Possui sistema de **cache local** para reduzir requisições repetidas à API da Steam.

## Funcionalidades

- Busca dados gerais do jogo (título, desenvolvedor, publisher, preço, gêneros, data de lançamento).
- Busca reviews resumidos (pontuação, total de reviews, positivos e negativos).
- Retorna requisitos do sistema (mínimos e recomendados).
- Retorna URLs de imagens (header e screenshots).
- Cache local para acelerar respostas e reduzir chamadas à API.

## Pré-requisitos

- Python 3.9+
- Bibliotecas:
  - `fastapi`
  - `uvicorn`
  - `requests`
  - `beautifulsoup4`
  - `pydantic`

Instale as dependências:

```bash
pip install fastapi uvicorn requests beautifulsoup4 pydantic
```
-------------------------------------------------------------------------------------------------------------------------

# Image Renamer Script - image_rename.py

Este script Python permite renomear automaticamente todas as imagens em uma pasta com um nome base e numeração sequencial.

## Funcionalidades

- Renomeia imagens em uma pasta para um padrão: `base_name-01.jpg`, `base_name-02.png`, etc.
- Suporta extensões comuns: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`.
- Ordena os arquivos antes de renomear para manter consistência.
- Mostra mensagem informando quantas imagens foram renomeadas.

## Pré-requisitos

- Python 3.x
- Bibliotecas padrão (`os`, `glob`) – não é necessário instalar nada adicional.

## Como usar

1. Clone ou baixe este repositório.
2. Execute o script:

```bash
python rename_images.py
```
-------------------------------------------------------------------------------------------------------------------------

# MySQL Image Storage Script - mysql_storage_script.py

Este script Python permite **inserir e recuperar imagens** de uma base de dados MySQL.

## Funcionalidades

- Conecta-se a uma base de dados MySQL.
- Insere imagens de uma pasta na tabela `images`.
- Armazena informações: nome do arquivo, dados binários, data de criação e `site_id`.
- Recupera imagens do banco de dados para salvar localmente.
- Suporta formatos comuns de imagens: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`.

## Pré-requisitos

- Python 3.x
- Biblioteca `mysql-connector-python`

Instale a dependência:

```bash
pip install mysql-connector-python
```
