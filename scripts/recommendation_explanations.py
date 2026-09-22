"""
TripLens - Structured Evidence Generator for Recommendations
Generates evidence-backed explanations grounded strictly in user history and package features.
"""

def generate_recommendation_explanation(pkg: dict, profile: dict, reasons: list) -> dict:
    matched_reasons = []
    potential_concerns = []

    for r in reasons:
        if r.get("positive"):
            matched_reasons.append(r["text"])
        else:
            potential_concerns.append(r["text"])

    # Additional evidence checks based on user profile
    visited = profile.get("visited_destinations", [])
    pkg_dest = pkg.get("destinations", "")
    if not any(v.lower() in pkg_dest.lower() for v in visited) and visited:
        matched_reasons.append(f"Unexplored destination compared to your past trips ({', '.join(visited[:2])})")

    themes = profile.get("preferred_themes", [])
    pkg_theme = str(pkg.get("theme") or "").lower()
    matching_themes = [t for t in themes if t in pkg_theme]
    if matching_themes:
        matched_reasons.append(f"Matches your demonstrated interest in {', '.join(matching_themes)}")

    # Check for warnings/long transit in itinerary if available
    transit_hours = pkg.get("total_transit_hours") or 0
    if transit_hours > 15:
        potential_concerns.append(f"Contains {transit_hours} hrs of cumulative road transit")

    return {
        "title": f"Why TripLens suggested {pkg.get('package_name')}",
        "matched_reasons": matched_reasons[:4],
        "potential_concerns": potential_concerns[:2]
    }
