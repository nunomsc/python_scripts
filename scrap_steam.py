import requests
from bs4 import BeautifulSoup
import os

def get_steam_game_data(appid, cc="us", lang="english"):
    """Busca info geral do jogo pela API da Steam Store"""
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc={cc}&l={lang}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data[str(appid)]["data"]

def get_steam_game_reviews(appid, lang="english"):
    """Busca reviews de um jogo pela API de reviews"""
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&language={lang}&filter=all"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def clean_html(raw_html: str) -> str:
    """Remove tags HTML e devolve apenas texto limpo"""
    if not raw_html:
        return "N/A"
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator="\n").strip()

def download_image(url, folder="images"):
    """Descarrega imagem para pasta local"""
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, url.split("/")[-1].split("?")[0])
    if not os.path.exists(filename):  # só baixa se não existir
        resp = requests.get(url, stream=True)
        if resp.status_code == 200:
            with open(filename, "wb") as f:
                f.write(resp.content)
    return filename

def main():
    print("APPID: ")
    appid = input()

    # Dados gerais
    game_data = get_steam_game_data(appid)
    title = game_data["name"]
    developer = ", ".join(game_data["developers"])
    publisher = ", ".join(game_data["publishers"])
    release_date = game_data["release_date"]["date"]
    price = game_data.get("price_overview", {}).get("final_formatted", "Free or not available")
    genres = ", ".join([g["description"] for g in game_data.get("genres", [])])

    # About this game
    about = clean_html(game_data.get("about_the_game", "N/A"))

    # Imagens (header + screenshots)
    header_img_url = game_data.get("header_image")
    capsule_img_url = game_data.get("capsule_image")
    screenshots = [s["path_full"] for s in game_data.get("screenshots", [])[:4]]  # até 4 imagens

    header_img_local = download_image(header_img_url) if header_img_url else None
    capsule_img_local = download_image(capsule_img_url) if capsule_img_url else None
    screenshots_local = [download_image(url) for url in screenshots]

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
        if "minimum" in game_data["pc_requirements"]:
            min_req = clean_html(game_data["pc_requirements"]["minimum"])
        if "recommended" in game_data["pc_requirements"]:
            rec_req = clean_html(game_data["pc_requirements"]["recommended"])

    # Criar HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title} - Steam Info</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #1b2838;
                color: #c7d5e0;
            }}
            h1, h2 {{
                color: #66c0f4;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 20px;
                border-radius: 8px;
                background-color: #2a475e;
                box-shadow: 0px 0px 8px rgba(0,0,0,0.5);
            }}
            .reqs {{
                white-space: pre-line;
                background: #0e141b;
                padding: 15px;
                border-radius: 6px;
                color: #e5e5e5;
                font-size: 14px;
            }}
            .screenshots img {{
                width: 48%;
                margin: 1%;
                border-radius: 8px;
                box-shadow: 0px 0px 5px rgba(0,0,0,0.6);
            }}
            .header {{
                text-align: center;
            }}
            .header img {{
                max-width: 100%;
                border-radius: 12px;
                margin-bottom: 20px;
            }}
            .about {{
                white-space: pre-line;
                font-size: 15px;
                line-height: 1.5em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{title}</h1>
            {'<img src="' + header_img_local + '" alt="Header Image">' if header_img_local else ""}
        </div>

        <div class="section">
            <h2>🎮 Game Info</h2>
            <p><strong>Developer:</strong> {developer}</p>
            <p><strong>Publisher:</strong> {publisher}</p>
            <p><strong>Release Date:</strong> {release_date}</p>
            <p><strong>Price:</strong> {price}</p>
            <p><strong>Genres:</strong> {genres}</p>
            {('<img src="' + capsule_img_local + '" alt="Capsule Image">') if capsule_img_local else ""}
        </div>

        <div class="section">
            <h2>📖 About this game</h2>
            <div class="about">{about}</div>
        </div>

        <div class="section">
            <h2>⭐ Reviews</h2>
            <p><strong>Review Score:</strong> {review_score}</p>
            <p><strong>Total Reviews:</strong> {total_reviews}</p>
            <p><strong>Positive:</strong> {positive}</p>
            <p><strong>Negative:</strong> {negative}</p>
        </div>

        <div class="section">
            <h2>🖥 System Requirements</h2>
            <h3>Minimum</h3>
            <div class="reqs">{min_req}</div>
            <h3>Recommended</h3>
            <div class="reqs">{rec_req}</div>
        </div>

        <div class="section screenshots">
            <h2>📸 Screenshots</h2>
            {"".join([f'<img src="{img}" alt="Screenshot">' for img in screenshots_local])}
        </div>
    </body>
    </html>
    """

    # Gravar em ficheiro HTML
    with open(f"{appid}-steam_game.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("✅ Ficheiro criado com sucesso com imagens e About this game!")

if __name__ == "__main__":
    main()
