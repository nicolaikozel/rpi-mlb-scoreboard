from enum import Enum


class Base(Enum):
    FIRST = "1b"
    SECOND = "2b"
    THIRD = "3b"


class InningState(Enum):
    TOP = "Top"
    BOTTOM = "Bottom"


TEAM_ABBREVIATIONS = {
    "Diamondbacks": "ARI",
    "Braves": "ATL",
    "Orioles": "BAL",
    "Red Sox": "BOS",
    "Cubs": "CHC",
    "White Sox": "CWS",
    "Reds": "CIN",
    "Indians": "CLE",
    "Rockies": "COL",
    "Tigers": "DET",
    "Marlins": "FLA",
    "Astros": "HOU",
    "Royals": "KAN",
    "Angels": "LAA",
    "Dodgers": "LAD",
    "Brewers": "MIL",
    "Twins": "MIN",
    "Mets": "NYM",
    "Yankees": "NYY",
    "Athletics": "OAK",
    "Phillies": "PHI",
    "Pirates": "PIT",
    "Padres": "SD",
    "Giants": "SF",
    "Mariners": "SEA",
    "Cardinals": "STL",
    "Rays": "TB",
    "Rangers": "TEX",
    "Blue Jays": "TOR",
    "Nationals": "WAS",
}


TEAM_COLORS = {
    "Diamondbacks": {
        "text": {"r": 227, "g": 212, "b": 173},
        "accent": {"r": 167, "g": 25, "b": 48},
    },
    "Braves": {"accent": {"r": 206, "g": 17, "b": 65}},
    "Orioles": {
        "text": {"r": 0, "g": 0, "b": 0},
        "accent": {"r": 223, "g": 70, "b": 1},
    },
    "Red Sox": {"accent": {"r": 189, "g": 48, "b": 57}},
    "Cubs": {"accent": {"r": 204, "g": 52, "b": 51}},
    "White Sox": {"text": {"r": 196, "g": 206, "b": 212}},
    "Reds": {"accent": {"r": 198, "g": 1, "b": 31}},
    "Indians": {"accent": {"r": 227, "g": 25, "b": 55}},
    "Rockies": {
        "accent": {"r": 51, "g": 0, "b": 111},
        "text": {"r": 0, "g": 0, "b": 0},
    },
    "Tigers": {
        "text": {"r": 0, "g": 0, "b": 0},
        "accent": {"r": 250, "g": 70, "b": 22},
    },
    "Marlins": {
        "text": {"r": 0, "g": 163, "b": 224},
        "accent": {"r": 239, "g": 51, "b": 64},
    },
    "Astros": {"accent": {"r": 235, "g": 110, "b": 31}},
    "Royals": {
        "accent": {"r": 189, "g": 155, "b": 96},
        "text": {"r": 0, "g": 0, "b": 0},
    },
    "Angels": {"accent": {"r": 186, "g": 0, "b": 33}},
    "Dodgers": {
        "text": {"r": 191, "g": 192, "b": 191},
        "accent": {"r": 239, "g": 62, "b": 66},
    },
    "Brewers": {
        "accent": {"r": 182, "g": 146, "b": 46},
    },
    "Twins": {"accent": {"r": 211, "g": 17, "b": 69}},
    "Mets": {
        "accent": {"r": 252, "g": 89, "b": 16},
    },
    "Yankees": {},
    "Athletics": {
        "text": {"r": 0, "g": 0, "b": 0},
        "accent": {"r": 239, "g": 178, "b": 30},
    },
    "Phillies": {},
    "Pirates": {
        "text": {"r": 0, "g": 0, "b": 0},
        "accent": {"r": 253, "g": 184, "b": 39},
    },
    "Padres": {
        "text": {"r": 0, "g": 0, "b": 0},
        "accent": {"r": 255, "g": 196, "b": 37},
    },
    "Giants": {
        "text": {"r": 0, "g": 0, "b": 0},
        "accent": {"r": 239, "g": 209, "b": 159},
    },
    "Mariners": {
        "text": {"r": 0, "g": 0, "b": 0},
        "accent": {"r": 196, "g": 206, "b": 212},
    },
    "Cardinals": {
        "accent": {"r": 196, "g": 30, "b": 58},
    },
    "Rays": {
        "text": {"r": 0, "g": 0, "b": 0},
        "accent": {"r": 143, "g": 188, "b": 230},
    },
    "Rangers": {
        "accent": {"r": 192, "g": 17, "b": 31},
    },
    "Blue Jays": {
        "accent": {"r": 19, "g": 74, "b": 142},
    },
    "Nationals": {
        "accent": {"r": 171, "g": 0, "b": 3},
    },
}
