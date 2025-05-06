locations = {
    "wordlist": [
        "australia",
        "aus",
        "aussie",
        "sydney",
        "syd",
        "melbourne",
        "melb",
        "brisbane",
        "perth",
        "darwin",
        "adelaide",
        "hobart",
        "canberra",
        "victoria",
        "queensland",
        "tasmania",
        "nsw",
        "qld",
        "vic",
        "sa",
        "wa",
        "nt",
        "tas",
        "act"
    ],
    "phraselist": [
        "down under",
        "new south wales",
        "northern territory",
        "western australia",
        "south australia"
    ]
}

def is_australian_location(location):
    location = location.lower()
    words = location.split(" ")
    for word in words:
        if word in locations["wordlist"]:
            return True
    for phrase in locations["phraselist"]:
        if phrase in location:
            return True
    return False