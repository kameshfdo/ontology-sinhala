from owlready2 import get_ontology, default_world
from rapidfuzz.fuzz import ratio
from .querymapping import QUERY_MAP
import json

# 1. Helper: Get verified values from ontology using SPARQL
def get_verified_values(sparql_query):
    results = list(default_world.sparql(sparql_query))
    return [str(item[0]) for item in results]

def get_average_similarity(input_list, verified_list, debug_label=None):
    if not input_list:
        return 1.0, []
    total = 0
    debug_pairs = []
    for value in input_list:
        if verified_list:
            scores = [ratio(value, v) for v in verified_list]
            max_score = max(scores)
            best_match = verified_list[scores.index(max_score)]
        else:
            max_score = 0
            best_match = None
        total += max_score / 100.0
        debug_pairs.append((value, best_match, max_score/100.0))
    if debug_label:
        print(f"\n[{debug_label}] Best matches:")
        for val, match, scr in debug_pairs:
            print(f"  Input: {val!r} --> Ontology: {match!r} (score={scr:.2f})")
    return total / len(input_list), debug_pairs


def check_fake(news_json, ontology_path="new-ontology-v1.owl", debug=True):
    onto = get_ontology(f"file://{ontology_path}").load()
    subcat = news_json.get('subcategory')
    entity_types = ['persons', 'locations', 'events', 'organizations']

    avg_scores = {}
    debug_outputs = {}
    counts = {}
    total_weight = 0
    weighted_sum = 0

    for etype in entity_types:
        values = news_json.get(etype, [])
        counts[etype] = len(values)
        if subcat in QUERY_MAP and etype in QUERY_MAP[subcat]:
            verified = get_verified_values(QUERY_MAP[subcat][etype])
        else:
            verified = []
        avg, debug_pairs = get_average_similarity(values, verified, etype if debug else None)
        avg_scores[etype] = avg
        debug_outputs[etype] = debug_pairs
        weighted_sum += avg * counts[etype]
        total_weight += counts[etype]

    if total_weight == 0:
        return 0.0, {"error": "No entities found in input JSON"}

    final_score = weighted_sum / total_weight
    return final_score, avg_scores, debug_outputs


# 4. Usage Example
if __name__ == "__main__":
    # EXAMPLE JSON (replace with your input)
    news_json = {
        "headline": "ඊශ්‍රායලය සහ ඉරානය සටන් විරාමයට එකඟ වෙයි",
        "content": "ඊශ්‍රායලය සටන් විරාමයට එකඟ වූ බව ...",
        "timestamp": "2025-06-08T14:30:00",
        "url": "https://sinhala.newsfirst.lk/2025/06/24/",
        "source": "NewsFirst Sri Lanka",
        "category": "PoliticsAndGovernance",
        "subcategory": "InternationalPolitics",
        "persons": ["අග්‍රාමාත්‍ය", "බෙන්ජමින්", "නෙතන්යාහු", "ජනාධිපති", "ඩොනල්ඩ්", "ට්‍රම්ප්"],
        "locations": ["ඊශ්‍රායලය", "ඉරානය", "ඇමරිකා"],
        "events": ["සටන් විරාමය"],
        "organizations": ["කාර්යාලය"]
    }

    score, details, debug_outputs = check_fake(news_json, debug=True)
    print(f"\nFinal similarity score: {score:.3f}")
    print("Detail scores:", details)
    print("News is", "NOT FAKE ✅" if score >= 0.7 else "SUSPICIOUS (possibly FAKE) ❌")
