from playlist_lib import *

# daily_mixes = [1, 2, 3, 4, 5, 6]
# feel_mixes = ["Moody", "Chill", "Upbeat", "Happy", "Romantic"]
# genre_mixes = ["Rock", "Punk", "Indie", "Metal", "Blues", "Pop", "Folk & Acoustic"]
# year_mixes = [2010, 2000, 90, 80, 70, 60]
# playlist_names = ["queue"]

daily_mixes = [1, 2, 3, 4, 5, 6]
feel_mixes = ["Moody", "Chill", "Upbeat", "Happy"]
genre_mixes = ["Rock", "Punk", "Indie", "Metal", "Blues", "Folk & Acoustic"]
year_mixes = [2010, 2000, 90, 80, 70]
playlist_names = ["queue"]

all_names = generate_names(playlist_names, daily_mixes, feel_mixes, genre_mixes, year_mixes)

tracks = get_random_liked(300)
tracks.extend(get_from_playlists(all_names))
tracks.extend(remove_not_liked(get_from_playlists(["Romantic Mix"])))
tracks.extend(get_random_from_playlist("Southern Gothic", 100))
tracks.extend(get_random_from_playlist("Southern Gothic/Dark Western", 30))
tracks.extend(get_random_from_playlist("Discover Weekly", 10))
tracks.extend(get_random_from_playlist("Domaće", 100))
tracks = remove_duplicates(tracks)
tracks = shuffle_tracks(tracks)

create_playlist("Svaštoteka", tracks)
