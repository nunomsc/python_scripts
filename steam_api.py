from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import os
import json

app = FastAPI(title="Steam Game API with Cache")

# -----------------------
# Funções auxiliares
# -----------------------

def get_steam_game_data(appid, cc="us", lang="english"):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc={cc}&l={lang}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[str(appid)]["data"]

def get_steam_game_reviews(appid, lang="english"):
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language={lang}&filter=all"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def clean_html(raw_html: str) -> str:
    if not raw_html:
        return "N/A"
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator="\n").strip()

# -----------------------
# Funções de cache
# -----------------------

CACHE_FOLDER = "cache"
os.makedirs(CACHE_FOLDER, exist_ok=True)

def save_game_cache(appid, data):
    path = os.path.join(CACHE_FOLDER, f"{appid}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_game_cache(appid):
    path = os.path.join(CACHE_FOLDER, f"{appid}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# -----------------------
# Modelo de resposta
# -----------------------

class GameInfo(BaseModel):
    appid: int
    title: str
    developer: str
    publisher: str
    release_date: str
    price: str
    genres: str
    about: str
    review_score: str
    total_reviews: int
    positive: int
    negative: int
    system_requirements: dict
    header_image: str
    screenshots: list

# -----------------------
# Endpoint principal
# -----------------------

@app.get("/game/{appid}", response_model=GameInfo)
def get_game_info(appid: int):
    # 1️⃣ Tenta carregar do cache
    cached = load_game_cache(appid)
    if cached:
        return cached

    # 2️⃣ Busca dados da Steam
    game_data = get_steam_game_data(appid)
    
    title = game_data["name"]
    developer = ", ".join(game_data.get("developers", []))
    publisher = ", ".join(game_data.get("publishers", []))
    release_date = game_data["release_date"]["date"]
    price_info = game_data.get("price_overview")
    if price_info:
        price = price_info.get("final_formatted", "N/A")
        original_price = price_info.get("initial_formatted", "")
        discount = price_info.get("discount_percent", 0)
        if discount > 0:
            price = f"{price} (Discount {discount}%, was {original_price})"
    else:
        price = "Free or not available"
    genres = ", ".join([g["description"] for g in game_data.get("genres", [])])
    about = clean_html(game_data.get("about_the_game", "N/A"))

    # Reviews
    reviews_data = get_steam_game_reviews(appid, lang="english")
    review_score = total_reviews = positive = negative = "N/A"
    if "query_summary" in reviews_data:
        summary = reviews_data["query_summary"]
        review_score = summary.get("review_score_desc", "N/A")
        total_reviews = summary.get("total_reviews", 0)
        positive = summary.get("total_positive", 0)
        negative = summary.get("total_negative", 0)

    # System Requirements
    min_req = rec_req = "N/A"
    if "pc_requirements" in game_data:
        min_req = clean_html(game_data["pc_requirements"].get("minimum", ""))
        rec_req = clean_html(game_data["pc_requirements"].get("recommended", ""))

    # Imagens
    header_img = game_data.get("header_image", "")
    screenshots = [s["path_full"] for s in game_data.get("screenshots", [])]

    # Montar resultado final
    result = GameInfo(
        appid=appid,
        title=title,
        developer=developer,
        publisher=publisher,
        release_date=release_date,
        price=price,
        genres=genres,
        about=about,
        review_score=review_score,
        total_reviews=total_reviews,
        positive=positive,
        negative=negative,
        system_requirements={
            "minimum": min_req,
            "recommended": rec_req
        },
        header_image=header_img,
        screenshots=screenshots
    ).dict()

    # 3️⃣ Salvar no cache para uso futuro
    save_game_cache(appid, result)

    return result
