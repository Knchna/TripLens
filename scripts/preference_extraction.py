"""
TripLens - NLP Preference Extraction
Deterministic first pass (regex-based). Never invents values it can't find —
missing fields stay None so the UI can ask the user to confirm/edit, per the
project's "never invent information" rule.
"""
import re

REGION_KEYWORDS = {
    "Kerala": [
        "kerala", "munnar", "alleppey", "alappuzha", "wayanad", "wayyanad",
        "kovalam", "thekkady", "kochi", "cochin", "varkala", "kumarakom",
        "thrissur", "kozhikode", "calicut",
    ],
    "Himachal Pradesh": [
        "himachal", "shimla", "manali", "kasol", "manikaran", "dalhousie",
        "dharamshala", "mcleod", "mcleodganj", "solang", "rohtang",
        "spiti", "kufri", "chail", "naldehra", "jibhi", "tirthan",
    ],
    "Goa": ["goa", "panaji", "panjim", "calangute", "baga", "anjuna", "vagator"],
    "Kashmir": [
        "kashmir", "srinagar", "gulmarg", "pahalgam", "sonamarg",
        "dal lake", "betab valley",
    ],
    "Andaman": ["andaman", "port blair", "havelock", "neil island", "radhanagar"],
    "Sikkim": ["sikkim", "gangtok", "pelling", "lachung", "lachen", "yuksom"],
    "North East": [
        "north east", "shillong", "meghalaya", "assam", "cherrapunji",
        "kaziranga", "mawlynnong", "dawki",
    ],
    "Rajasthan": [
        "rajasthan", "jaipur", "udaipur", "jodhpur", "jaisalmer",
        "pushkar", "mount abu", "bikaner",
    ],
}

THEME_KEYWORDS = {
    "nature": ["nature", "greenery", "waterfalls", "hills", "scenic", "forest", "wildlife"],
    "beach": ["beach", "coast", "island", "sea", "shores"],
    "backwaters": ["backwater", "houseboat", "lagoon"],
    "adventure": ["adventure", "trek", "trekking", "rafting", "paragliding", "camping"],
    "heritage": ["heritage", "temple", "fort", "culture", "historic", "palace"],
    "pilgrimage": ["pilgrimage", "spiritual", "temple visit", "shrine"],
    "hill-station": ["hill station", "mountains", "snow", "valley", "snowfall"],
    "honeymoon/romance": ["honeymoon", "romantic", "couple", "anniversary"],
    "family": ["family", "kids", "children", "parents"],
    "sightseeing": ["sightseeing", "points", "viewpoint", "tourist spots"],
}

PACE_KEYWORDS = {
    "Relaxed": ["relaxed", "leisure", "slow", "peaceful", "unrushed", "easy"],
    "Active": ["active", "packed", "fast-paced", "full circuit", "express", "intensive"],
}

# Origin cities to scan in the full prompt text
ORIGIN_CITIES = [
    "delhi", "new delhi", "chandigarh", "kochi", "cochin", "bangalore", "bengaluru",
    "mumbai", "bombay", "chennai", "madras", "kolkata", "calcutta", "hyderabad",
    "pune", "ahmedabad", "surat", "jaipur", "lucknow", "bhopal", "nagpur",
    "coimbatore", "trivandrum", "thiruvananthapuram", "kozhikode", "calicut",
    "amritsar", "ludhiana", "dehradun",
]


def _find_first_keyword_match(text: str, keyword_map: dict):
    for label, keywords in keyword_map.items():
        for kw in keywords:
            if kw in text:
                return label
    return None


def _parse_amount(raw: str) -> int | None:
    """Convert budget string to integer rupees.
    Handles: 20000, 20,000, 20k, 20.5k, \u20b920000, rs20000
    """
    raw = raw.strip().lower()
    # Strip currency prefixes
    raw = re.sub(r"^(\u20b9|rs\.?\s*|inr\s*)", "", raw).strip()
    if not raw:
        return None
    try:
        if raw.endswith("k"):
            return int(float(raw[:-1]) * 1000)
        # Remove commas and parse
        return int(raw.replace(",", ""))
    except ValueError:
        return None


def extract_preferences(prompt_text: str) -> dict:
    text = prompt_text.lower()
    prefs = {
        "destination_region": None,
        "start_location": None,
        "duration_days": None,
        "budget_min": None,
        "budget_max": None,
        "travelers": None,
        "pace": None,
        "interests": [],
    }

    # ------------------------------------------------------------------ #
    # BUDGET — range or single upper-bound
    # Handles: 20000 / 20,000 / 20k / Rs 20000 / under 20000
    # Amount pattern: currency-optional + (comma-thousands OR 4-7 plain digits OR Nk)
    # ------------------------------------------------------------------ #
    _cur = r"(?:\u20b9|rs\.?\s*|inr\s*)?"
    # A single amount token: optional currency + (comma-formatted | 4-7 bare digits | Nk)
    _amt = rf"{_cur}((?:\d{{1,3}}(?:,\d{{3}})+)|(?:\d{{4,7}})|(?:\d+\.?\d*k))"

    range_match = re.search(
        rf"{_amt}\s*(?:and|to|-)\s*{_amt}",
        text,
    )
    if range_match:
        a = _parse_amount(range_match.group(1))
        b = _parse_amount(range_match.group(2))
        if a is not None and b is not None:
            prefs["budget_min"] = min(a, b)
            prefs["budget_max"] = max(a, b)
    else:
        single_match = re.search(
            rf"(?:under|below|within|max(?:imum)?|budget(?:\s+of)?)\s*{_amt}",
            text,
        )
        if single_match:
            val = _parse_amount(single_match.group(1))
            if val is not None:
                prefs["budget_max"] = val


    # ------------------------------------------------------------------ #
    # DURATION — "5 days", "5-day", "a week", "10 nights"
    # ------------------------------------------------------------------ #
    duration_match = re.search(r"(\d+)\s*[-\s]?day", text)
    if duration_match:
        prefs["duration_days"] = int(duration_match.group(1))
    else:
        night_match = re.search(r"(\d+)\s*night", text)
        if night_match:
            prefs["duration_days"] = int(night_match.group(1)) + 1
        elif "week" in text:
            prefs["duration_days"] = 7

    # ------------------------------------------------------------------ #
    # TRAVELERS — "2 people", "for 2", "couple", "solo"
    # ------------------------------------------------------------------ #
    travelers_match = re.search(
        r"(\d+)\s*(?:people|travelers?|travellers?|persons?|pax)", text
    )
    if travelers_match:
        prefs["travelers"] = int(travelers_match.group(1))
    else:
        # "for 2" pattern (common shorthand)
        for_n = re.search(r"\bfor\s+(\d+)\b", text)
        if for_n and int(for_n.group(1)) <= 20:
            prefs["travelers"] = int(for_n.group(1))
        elif "couple" in text or "honeymoon" in text:
            prefs["travelers"] = 2
        elif "solo" in text:
            prefs["travelers"] = 1

    # ------------------------------------------------------------------ #
    # DESTINATION REGION
    # ------------------------------------------------------------------ #
    prefs["destination_region"] = _find_first_keyword_match(text, REGION_KEYWORDS)

    # ------------------------------------------------------------------ #
    # START LOCATION
    # "from Delhi to Shimla" → start = Delhi, dest handled above
    # "from Kochi" → start = Kochi
    # We must NOT pick up destination words as the start city.
    # ------------------------------------------------------------------ #
    destination_words = set()
    for keywords in REGION_KEYWORDS.values():
        destination_words.update(keywords)

    # Try "from <city>" pattern — capture word immediately after "from"
    from_match = re.search(r"\bfrom\s+([a-z][a-z\s]{1,20}?)(?:\s+to\b|\s+for\b|,|\.|$)", text)
    if from_match:
        candidate = from_match.group(1).strip()
        # Accept known origin cities — even if they overlap with destination keywords
        # (e.g. Kochi is both a Kerala keyword AND a valid departure city)
        if candidate in ORIGIN_CITIES:
            prefs["start_location"] = candidate.title()

    # Fallback: scan full text for any known origin city
    if prefs["start_location"] is None:
        for city in ORIGIN_CITIES:
            if re.search(rf"\b{re.escape(city)}\b", text):
                prefs["start_location"] = city.title()
                break


    # ------------------------------------------------------------------ #
    # PACE
    # ------------------------------------------------------------------ #
    prefs["pace"] = _find_first_keyword_match(text, PACE_KEYWORDS) or "Moderate"

    # ------------------------------------------------------------------ #
    # INTERESTS / THEMES (multi-match)
    # ------------------------------------------------------------------ #
    matched_interests = []
    for theme, keywords in THEME_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            matched_interests.append(theme)
    prefs["interests"] = matched_interests

    return prefs


if __name__ == "__main__":
    samples = [
        "I want a 6-day Shimla and Manali trip from Delhi for 2 people under 20000",
        "I want a relaxed 5-day Kerala trip from Kochi for 2 people under Rs 30,000 with beaches",
        "Plan a 7 day trip from Delhi to Goa for 4 people budget between 15000 to 25000",
        "I want to visit Manali from Delhi for 5 days within 15k budget for 2 travelers",
        "Trip from Delhi to Shimla for 3 days budget 12000 to 18000 for 2 people",
        "6 day Shimla & Manali trip from Delhi for 2 people under ₹20,000 with Solang Valley, snow points, relaxed pace",
    ]
    for s in samples:
        r = extract_preferences(s)
        print(f"PROMPT : {s[:70]}")
        print(f"  dest={r['destination_region']}  from={r['start_location']}  "
              f"days={r['duration_days']}  travelers={r['travelers']}  "
              f"budget={r['budget_min']}-{r['budget_max']}  pace={r['pace']}")
        print()
