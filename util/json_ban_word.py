import json


def save_banned_words(banned_words):
    with open("banned_words.json", "w") as json_file:
        json.dump(banned_words, json_file)


def load_banned_words():
    try:
        with open("banned_words.json", "r") as json_file:
            words = json.load(json_file)
            return words
    except FileNotFoundError:
        save_banned_words([])
        return []
