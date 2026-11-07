"""Transparent rule-based recommendation engine for four common open-source licenses."""

def recommend_license(data):
    scores = {"MIT": 0, "BSD": 0, "Apache": 0, "GPL": 0}
    reasons = {key: [] for key in scores}
    conflicts = []

    commercial = data["commercial"] == "yes"
    modification = data["modification"] == "yes"
    redistribution = data["redistribution"] == "yes"
    copyleft = data["same_license"] == "yes"
    attribution = data["attribution"] == "yes"
    patent = data["patent"] == "yes"
    preference = data["preference"]

    # These four licenses permit commercial use, modification and redistribution.
    if commercial:
        for key in scores:
            scores[key] += 1
            reasons[key].append("permits commercial use")
    if modification:
        for key in scores:
            scores[key] += 1
            reasons[key].append("permits modification")
    if redistribution:
        for key in scores:
            scores[key] += 1
            reasons[key].append("permits redistribution subject to license conditions")

    if copyleft:
        scores["GPL"] += 8
        reasons["GPL"].append("requires covered distributed derivative works to follow GPL copyleft terms")
        for key in ("MIT", "BSD", "Apache"):
            scores[key] -= 5
        if preference == "permissive":
            conflicts.append("You selected both same-license sharing (copyleft) and a permissive preference. These goals point to different license models.")
    elif data["same_license"] == "no":
        for key in ("MIT", "BSD", "Apache"):
            scores[key] += 2
            reasons[key].append("does not impose a general copyleft requirement on derivatives")
        scores["GPL"] -= 3

    if patent:
        scores["Apache"] += 9
        reasons["Apache"].append("includes an express contributor patent license")
        scores["GPL"] += 2
        reasons["GPL"].append("GPLv3 includes an express contributor patent license, subject to its terms")
        scores["MIT"] -= 2
        scores["BSD"] -= 2
    if preference == "copyleft":
        scores["GPL"] += 6
        reasons["GPL"].append("matches your copyleft preference")
        for key in ("MIT", "BSD", "Apache"):
            scores[key] -= 2
    elif preference == "permissive":
        for key in ("MIT", "BSD", "Apache"):
            scores[key] += 3
            reasons[key].append("matches your permissive-license preference")
        scores["GPL"] -= 3

    # Attribution is a condition of all four licenses, not an optional feature.
    if attribution:
        for key in scores:
            scores[key] += 1
            reasons[key].append("requires preservation of relevant copyright/license notices")
    else:
        conflicts.append("All four licenses require preservation of certain notices. Selecting 'No' for attribution does not remove those legal obligations.")

    if not commercial:
        conflicts.append("You selected that commercial use should not be allowed, but all four licenses in this system permit commercial use. None is a suitable match for that restriction.")
    if not modification:
        conflicts.append("All four listed open-source licenses permit modification. If you need to prohibit modification, these four are not a suitable set.")
    if not redistribution:
        conflicts.append("All four listed open-source licenses permit redistribution subject to their terms. If you need to prohibit redistribution, these four are not a suitable set.")

    # Rank with stable ordering; patent and copyleft requirements carry stronger weights.
    ranked = sorted(scores, key=lambda k: scores[k], reverse=True)
    best = ranked[0]
    if copyleft:
        best = "GPL"
    elif patent:
        best = "Apache"

    alternatives = [key for key in ranked if key != best][:2]
    explanations = reasons[best] or ["it is the closest match among the four licenses based on the answers provided"]
    description = (
        f"{LICENSE_NAMES[best]} is the closest match to the stated requirements. "
        + "It " + "; it ".join(explanations[:4]) + "."
    )
    if conflicts:
        description += " Review the compatibility warnings below before choosing."
    return {
        "recommended_key": best,
        "explanation": description,
        "reasons": explanations,
        "alternatives": alternatives,
        "conflicts": conflicts,
        "scores": scores
    }

LICENSE_NAMES = {
    "MIT": "MIT License",
    "BSD": "BSD 3-Clause License",
    "Apache": "Apache License 2.0",
    "GPL": "GNU General Public License (GPL)"
}
