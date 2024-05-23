from random import randint, randrange, shuffle
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
import logging
import spotipy


_scope = "playlist-read-private, playlist-modify-private, user-library-read"
client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=_scope))
logging.basicConfig(level=logging.CRITICAL)


def _is_available(track):
    return not track["available_markets"] or "RS" in track["available_markets"]


def _print_percent(percent: float, length=30):
    print(f"[{(min(round(length * percent), length) * '=').ljust(length)}] {min(percent*100, 100):4.2f}%", end="\r")


def get_random_liked(n):
    print(f"Downloading {n} random liked songs:")
    total = client.current_user_saved_tracks()["total"] - 50
    random_liked, offsets = [], set()
    while len(offsets) != n:
        offsets.add(randrange(200, total, 50))

    for offset in offsets:
        liked = None
        while not liked:
            try:
                sleep(2)
                liked = client.current_user_saved_tracks(50, offset)["items"]
                liked = [liked[i]["track"] for i in range(1, 49, int(49 / randint(3, 8)))]
            except:
                _print_percent(0)
                sleep(10)

        while liked:
            track = liked.pop()
            if all([track["artists"][0]["name"] != other["artists"][0]["name"] for other in liked]) and _is_available(track):
                random_liked.append(track)

        _print_percent(len(random_liked) / n)
        if len(random_liked) >= n:
            print("\n")
            return random_liked[:n]


def get_from_playlists(names):
    playlists = client.current_user_playlists()
    all_tracks = []

    while playlists:
        for playlist in [playlist for playlist in playlists["items"] if playlist["name"] in names]:
            print(f"Downloading songs from playlist {playlist["name"]}:")
            tracks = client.playlist_tracks(playlist["uri"])
            while tracks:
                _print_percent(tracks["offset"] / tracks["total"])
                all_tracks.extend([track["track"] for track in tracks["items"] if _is_available(track["track"])])
                tracks = client.next(tracks) if tracks["next"] else None
            _print_percent(1)
            print("\n")
        playlists = client.next(playlists) if playlists["next"] else None
        
    return all_tracks


def get_random_from_playlist(name, n):
    print(f"Downloading songs from playlist {name}:")
    playlists = client.current_user_playlists()
    all_tracks = []

    while playlists:
        for playlist_uri in [playlist["uri"] for playlist in playlists["items"] if playlist["name"] == name]:
            tracks = client.playlist_tracks(playlist_uri)
            while tracks:
                all_tracks.extend([track["track"] for track in tracks["items"] if _is_available(track["track"])])
                _print_percent(tracks["offset"] / tracks["total"])
                tracks = client.next(tracks) if tracks["next"] else None
            _print_percent(1)
            print("\n")
            return shuffle_tracks(all_tracks)[:n]
        playlists = client.next(playlists) if playlists["next"] else None

    print("Playlist not found!")
    return None


def remove_not_liked(tracks):
    return [track for track in tracks if client.current_user_saved_tracks_contains([track["id"]])[0]]


def _different_artists(track1, track2):
    return all(artist1["name"] not in [artist2["name"] for artist2 in track2["artists"]] for artist1 in track1["artists"])


def remove_duplicates(tracks):
    unique = []
    while tracks:
        track = tracks.pop()
        if all([track["name"] != added["name"] or _different_artists(track, added) for added in unique]):
            unique.append(track)
    return unique


def shuffle_tracks(tracks):
    shuffle(tracks)
    return tracks


def create_playlist(name, tracks):
    print(f"Uploading tracks to the {name}:")
    playlist = client.user_playlist_create(client.current_user()["id"], name, False)
    uris = [track["uri"] for track in tracks]
    chunks = [uris[i : i + 100] for i in range(0, len(uris), 100)]
    for i, chunk in enumerate(chunks):
        _print_percent(i / len(chunks))
        client.playlist_add_items(playlist["id"], chunk)
    _print_percent(1)
    print("\n")

def generate_names(playlist_names: list[str], daily_mixes, feel_mixes, genre_mixes, year_mixes):
    names = playlist_names.copy()
    names += [f"Daily Mix {day}" for day in daily_mixes]
    names += [f"{feel} Mix" for feel in feel_mixes]
    names += [f"{genre} Mix" for genre in genre_mixes]
    names += [f"{year}s Mix" for year in year_mixes]
    return names
