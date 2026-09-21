"""
TripLens - Hybrid Ranking Engine + Explainability
Deterministic scoring (per project rule: no LLM as the final ranking
engine) combining budget, destination, duration, interest, pace, and
semantic similarity into one weighted score. Every score is backed by
an actual comparison against real package data — nothing here is
invented, only calculated.
"""
from config.ranking_weights import RANKING_WEIGHTS


def score_budget_fit(price, budget_min, budget_max):
    if price is None:
        return 0.5, None
    if budget_max is None:
        return 0.8, None  # no constraint given, neutral-positive
    lo = budget_min if budget_min is not None else 0
    if lo <= price <= budget_max:
        return 1.0, {"text": f"Within your budget range (₹{int(price):,} fits ₹{int(lo):,}–₹{int(budget_max):,})", "positive": True}
    if price > budget_max:
        diff = price - budget_max
        if diff <= 4000:
            return 0.6, {"text": f"₹{int(diff):,} above your max budget, but close enough to consider", "positive": True}
        return 0.2, {"text": f"₹{int(diff):,} above your max budget of ₹{int(budget_max):,}", "positive": False}
    # price < lo
    return 0.9, {"text": f"₹{int(lo - price):,} under your minimum budget, leaves room for extras", "positive": True}


def score_destination_fit(destinations_str, start_location_actual, destination_region, start_location_pref):
    if not destination_region:
        return 0.7, None
    dest_text = str(destinations_str or "").lower()
    region_matches = destination_region.lower() in dest_text or any(
        part.strip() in dest_text for part in destination_region.lower().split()
    )
    if region_matches:
        reason = {"text": f"Destination matches your requested {destination_region}", "positive": True}
        score = 1.0
    else:
        reason = {"text": f"Destinations ({destinations_str}) don't clearly match {destination_region}", "positive": False}
        score = 0.2

    if start_location_pref and start_location_actual:
        if start_location_pref.lower() != str(start_location_actual).lower():
            reason_start = {
                "text": f"Starts from {start_location_actual}, not your requested {start_location_pref}",
                "positive": False,
            }
            return max(0.0, score - 0.2), reason_start if score < 1.0 else reason
    return score, reason


def score_duration_fit(duration_days_actual, duration_days_pref):
    if not duration_days_pref or duration_days_actual is None:
        return 0.7, None
    diff = abs(duration_days_actual - duration_days_pref)
    if diff == 0:
        return 1.0, {"text": f"Duration matches your requested {duration_days_pref} days exactly", "positive": True}
    if diff == 1:
        return 0.7, {"text": f"{int(duration_days_actual)} days, close to your requested {duration_days_pref}", "positive": True}
    return 0.3, {"text": f"{int(duration_days_actual)} days instead of your requested {duration_days_pref}", "positive": False}


def score_interest_fit(theme_clean, interests_pref):
    if not interests_pref:
        return 0.6, None
    theme_text = str(theme_clean or "").lower()
    matched = [i for i in interests_pref if i in theme_text]
    if matched:
        return 1.0, {"text": f"Matches your interest in {', '.join(matched)}", "positive": True}
    return 0.3, {"text": f"Theme ({theme_clean}) doesn't clearly match your interests ({', '.join(interests_pref)})", "positive": False}


def score_pace_fit(itinerary_pace_inferred, pace_pref):
    if not pace_pref:
        return 0.7, None
    if str(itinerary_pace_inferred).lower() == str(pace_pref).lower():
        return 1.0, {"text": f"Pace matches your preferred {pace_pref} style", "positive": True}
    return 0.5, {"text": f"Pace is {itinerary_pace_inferred}, you preferred {pace_pref}", "positive": False}


def rank_candidates(candidates: list, prefs: dict) -> list:
    ranked = []
    for pkg in candidates:
        budget_score, budget_reason = score_budget_fit(pkg.get("price"), prefs.get("budget_min"), prefs.get("budget_max"))
        dest_score, dest_reason = score_destination_fit(
            pkg.get("destinations"), pkg.get("start_location"), prefs.get("destination_region"), prefs.get("start_location")
        )
        duration_score, duration_reason = score_duration_fit(pkg.get("duration_days"), prefs.get("duration_days"))
        interest_score, interest_reason = score_interest_fit(pkg.get("theme_clean"), prefs.get("interests"))
        pace_score, pace_reason = score_pace_fit(pkg.get("itinerary_pace_inferred"), prefs.get("pace"))
        semantic_score = pkg.get("semantic_similarity", 0.0)

        weights = RANKING_WEIGHTS
        final_score = (
            weights["budget_fit"] * budget_score
            + weights["destination_match"] * dest_score
            + weights["duration_fit"] * duration_score
            + weights["interest_match"] * interest_score
            + weights["pace_match"] * pace_score
            + weights["semantic_similarity"] * semantic_score
        )

        reasons = [r for r in [dest_reason, budget_reason, interest_reason, pace_reason, duration_reason] if r]

        ranked.append({
            "package_id": pkg["package_id"],
            "package_name": pkg["package_name"],
            "agency_name": pkg.get("agency_name"),
            "source_url_or_doc": pkg.get("source_url_or_doc"),
            "destinations": pkg.get("destinations"),
            "start_location": pkg.get("start_location"),
            "theme": pkg.get("theme_clean"),
            "pace": pkg.get("itinerary_pace_inferred"),
            "price": pkg.get("price"),
            "duration_days": pkg.get("duration_days"),
            "fit_score": round(final_score * 100, 1),
            "score_breakdown": {
                "budget_fit": round(budget_score, 2),
                "destination_match": round(dest_score, 2),
                "duration_fit": round(duration_score, 2),
                "interest_match": round(interest_score, 2),
                "pace_match": round(pace_score, 2),
                "semantic_similarity": round(semantic_score, 2),
            },
            "reasons": reasons,
        })

    ranked.sort(key=lambda x: x["fit_score"], reverse=True)
    return ranked


if __name__ == "__main__":
    from scripts.preference_extraction import extract_preferences
    from scripts.retrieval import get_candidates

    sample = "I want a relaxed 5-day Kerala trip from Kochi for 2 people under ₹30,000 with beaches, nature and sightseeing."
    prefs = extract_preferences(sample)
    candidates = get_candidates(prefs, sample, top_k=10)
    ranked = rank_candidates(candidates, prefs)

    for r in ranked:
        print(f"\n{r['package_id']} — {r['package_name']} | Fit: {r['fit_score']}% | ₹{r['price']}")
        for reason in r["reasons"]:
            mark = "✓" if reason["positive"] else "⚠"
            print(f"  {mark} {reason['text']}")
