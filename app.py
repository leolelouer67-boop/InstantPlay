from flask import Flask, render_template, request, redirect, url_for
import random
import json
import os

app = Flask(__name__)

# Load games from JSON
GAMES_FILE = os.path.join(os.path.dirname(__file__), "data", "games.json")

def load_games():
    with open(GAMES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

GAMES = load_games()

CATEGORIES = {
    "rpg": {"name": "RPG", "icon": "⚔️", "description": "Role-playing adventures, level up, explore worlds"},
    "horror": {"name": "Horror", "icon": "👻", "description": "Jump scares, atmosphere, survival horror"},
    "multiplayer": {"name": "Multiplayer", "icon": "👥", "description": "Play with friends or strangers online"},
    "rage": {"name": "Rage Games", "icon": "🔥", "description": "Hardcore, frustrating, rage-quit inducing games"}
}

@app.route("/")
def index():
    featured = random.sample(GAMES, min(6, len(GAMES)))
    random_game = random.choice(GAMES)
    return render_template(
        "index.html",
        featured=featured,
        random_game=random_game,
        categories=CATEGORIES,
        total_games=len(GAMES)
    )

@app.route("/category/<cat_id>")
def category(cat_id):
    if cat_id not in CATEGORIES:
        return redirect(url_for("index"))

    filtered = [g for g in GAMES if cat_id in g.get("categories", [])]
    return render_template(
        "category.html",
        category=CATEGORIES[cat_id],
        cat_id=cat_id,
        games=filtered,
        categories=CATEGORIES
    )

@app.route("/game/<int:game_id>")
def game(game_id):
    game = next((g for g in GAMES if g["id"] == game_id), None)
    if not game:
        return redirect(url_for("index"))
    return render_template("game.html", game=game, categories=CATEGORIES)

@app.route("/random")
def random_game():
    game = random.choice(GAMES)
    return redirect(url_for("game", game_id=game["id"]))

@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return redirect(url_for("index"))

    results = [
        g for g in GAMES
        if query in g["title"].lower()
        or query in g.get("description", "").lower()
        or any(query in c for c in g.get("categories", []))
    ]
    return render_template(
        "search.html",
        query=query,
        results=results,
        categories=CATEGORIES
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)