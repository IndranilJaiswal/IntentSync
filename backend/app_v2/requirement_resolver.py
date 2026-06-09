"""
requirement_resolver.py

Maps natural language requirement text to known governed requirements.
"""

from requirement_library import load_requirements


def _score_requirement(query: str, requirement) -> int:
    query_tokens = set(query.lower().replace(".", "").split())

    requirement_text = " ".join(
        [
            requirement.requirement_id,
            requirement.title,
            requirement.description,
        ]
    ).lower()

    requirement_tokens = set(
        requirement_text.replace(".", "").split()
    )

    return len(query_tokens.intersection(requirement_tokens))


def resolve_requirement(
    requirement_text: str,
) -> dict:
    requirements = load_requirements()

    ranked = sorted(
        requirements,
        key=lambda requirement: _score_requirement(
            requirement_text,
            requirement,
        ),
        reverse=True,
    )

    best = ranked[0]

    score = _score_requirement(
        requirement_text,
        best,
    )

    confidence = "LOW"

    if score >= 5:
        confidence = "HIGH"
    elif score >= 2:
        confidence = "MEDIUM"

    return {
        "input_text": requirement_text,
        "requirement_id": best.requirement_id,
        "title": best.title,
        "description": best.description,
        "match_score": score,
        "match_confidence": confidence,
    }
