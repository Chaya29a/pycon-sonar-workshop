import os
from flask import Flask, render_template, redirect, url_for, request, g
from pokedex import helper

app = Flask(__name__)
app.config["DATABASE"] = "../database.db"


@app.route("/")
def index():
    pokemon = [
        {"id": id, "pokemon_name": pokemon_name, "image_url": image_url}
        for (id, pokemon_name, image_url, _) in helper.fetch_all_pokemons(get_db())
    ]
    return render_template("index.html", pokemon=pokemon)


@app.route("/subscribe", methods=["POST"])
def subscribe():
    Email = request.form["email"]
    helper.register_subscriber(get_db(), Email)
    # TODO: add confirmation message
    return redirect(url_for("index"))


def get_db():
    if "db" not in g:
        g.db = helper.ConnectionWrapper(app.config["DATABASE"])
    return g.db


@app.teardown_appcontext
def close_db(error):
    if "db" in g:
        g.db.cleanup(True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True, port=port, debug=True)
