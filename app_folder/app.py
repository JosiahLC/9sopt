import os
from flask import Flask, render_template, request
from .spotify_api_calls import *
from .model import *
import pandas as pd

"""Create and configure an instance of the flask application"""
app = Flask(__name__)


# configure app
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize database
DB.init_app(app)

# create table(s)
with app.app_context():
    DB.create_all()

# ROOT ROUTE
@app.route("/", methods=["GET", "POST"])
def root():

    """Base view"""

    return render_template("home.html")


@app.route("/recommendations", methods=["GET", "POST"])
def recommendations_page():
    if request.method == "POST":
        song_name = request.form["song_name"]
        artist_name = request.form["artist_name"]

        try:
            song_id, artist_id = retrieve_spotify_ids(song_name, artist_name)
        except:
            message = "There was an error finding your song. Please go back and enter another song."
            return render_template("recommendations.html", message=message)

        audio_features_dict = retrieve_audio_features(song_id)

        danceability = audio_features_dict[0]["danceability"]
        energy = audio_features_dict[0]["energy"]
        key = audio_features_dict[0]["key"]
        loudness = audio_features_dict[0]["loudness"]
        mode = audio_features_dict[0]["mode"]
        speechiness = audio_features_dict[0]["speechiness"]
        acousticness = audio_features_dict[0]["acousticness"]
        instrumentalness = audio_features_dict[0]["instrumentalness"]
        liveness = audio_features_dict[0]["liveness"]
        valence = audio_features_dict[0]["valence"]
        tempo = audio_features_dict[0]["tempo"]
        duration_ms = audio_features_dict[0]["duration_ms"]
        time_signature = audio_features_dict[0]["time_signature"]

        user_song_features = [
            danceability,
            energy,
            key,
            loudness,
            mode,
            speechiness,
            acousticness,
            instrumentalness,
            liveness,
            valence,
            tempo,
            duration_ms,
            time_signature,
        ]

        # Use function from model.py to get recommendations
        recommendations = find_recommendations(user_song_features)

        return render_template("recommendations.html", recommendations=recommendations)


if __name__ == "__main__":
    app.run()
