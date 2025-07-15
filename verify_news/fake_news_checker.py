from owlready2 import get_ontology, default_world
from rapidfuzz.fuzz import ratio
from .querymapping import QUERY_MAP
from .query import query43,query44 # Importing the new query for publisher names
import json
import requests

# 1. Helper: Get verified values from ontology using SPARQL
def get_verified_values(sparql_query):
    results = list(default_world.sparql(sparql_query))
    return [str(item[0]) for item in results]

def get_trusted_publishers():
    sparql = """
    PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>
    SELECT DISTINCT ?publisher
    WHERE {
      ?article ns:publisherName ?publisher .
    }
    """
    results = list(default_world.sparql(sparql))
    return [str(r[0]) for r in results]

def get_source_credibility(news_publisher, trusted_publishers):
    # Binary score for now: 1.0 if in trusted, else 0.0
    return 1.0 if news_publisher in trusted_publishers else 0.0


# def get_all_trusted_contents():
#     sparql = """
#     PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>
#     SELECT DISTINCT ?trustSementics
#     WHERE {
#       ?article ns:hasFullText ?trustSementics .
#     }
#     """
#     results = list(default_world.sparql(sparql))
#     return [str(r[0]) for r in results]

def get_trusted_contents_by_category(category):
    # Make sure category is the exact string after 'ns:', e.g., 'Cricket'
    category_uri = f"ns:{category}"

    sparql = f"""
    PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>
    SELECT DISTINCT ?trustSementics
    WHERE {{
      ?article ns:hasCategory ?cat .
      FILTER (?cat = {category_uri})
      ?article ns:hasFullText ?trustSementics .
    }}
    """
    results = list(default_world.sparql(sparql))
    return [str(r[0]) for r in results]

def get_semantic_similarity_score(news_text, trusted_texts, api_url="https://5f563af82bb5.ngrok-free.app/similarity"):
    payload = {
        "news_text": news_text,
        "trusted_texts": trusted_texts
    }
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return float(result.get("max_similarity", 0.0))
    except Exception as e:
        print(f"[Error] Could not get similarity from API: {e}")
        return 0.0


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

    entity_similarity_score = weighted_sum / total_weight if total_weight > 0 else 0.0
    if debug:
        print("\n[Entity Similarity] Average scores per entity type:")
        for etype, score in avg_scores.items():
            print(f"  {etype}: {score:.3f} (count={counts[etype]})")
        print(f"  Overall entity similarity score: {entity_similarity_score:.3f}")
    
    # --- Semantic Similarity ---
    trusted_texts = get_trusted_contents_by_category(subcat)
    content = news_json.get("content", "")
    semantic_similarity_score = get_semantic_similarity_score(content, trusted_texts)
    if debug:
        print(f"\n[Semantic Similarity] Content: {content!r}")
        print(f"  Trusted texts: {trusted_texts[:3]}... (total {len(trusted_texts)})")
        print(f"  Semantic similarity score: {semantic_similarity_score:.3f}")

    # --- Source Credibility ---
    trusted_publishers = get_trusted_publishers()
    publisher = news_json.get("source", "")
    source_credibility_score = get_source_credibility(publisher, trusted_publishers)

    if debug:
        print(f"\n[Source Credibility] Publisher: {publisher!r}")
        print(f"  Trusted publishers: {trusted_publishers[:3]}... (total {len(trusted_publishers)})")
        print(f"  Source credibility score: {source_credibility_score:.3f}")


    # --- Composite Score (weights can be tuned, e.g. 0.4/0.3/0.3) ---
    final_score = (
        0.4 * entity_similarity_score +
        0.3 * semantic_similarity_score +
        0.3 * source_credibility_score
    )

    return final_score, {
        "entity_similarity": entity_similarity_score,
        "semantic_similarity": semantic_similarity_score,
        "source_credibility": source_credibility_score,
        "per_entity": avg_scores
    }, debug_outputs


# 4. Usage Example
if __name__ == "__main__":
    # EXAMPLE JSON (replace with your input)
    news_json = {
        "headline": "සත්කාරක ශ්‍රී ලංකා - බංග්ලාදේශ දෙවැනි පන්දුවාර 20යි 20 ක්‍රිකට් තරගය අද (13) පැවැත්වේ",
        "content": "තරගාවලියේ පළමු තරගය කඩුලු 7 කින් ජය ගත්තේ ශ්‍රී ලංකා කණ්ඩායමයි.ඒ අනුව ඔවුන් තරග 3කින් සමන්විත පන්දුවාර 20යි 20 ක්‍රිකට් තරගාවලිය තරග 1ට 0ක් ලෙස පෙරමුණ ගෙන සිටී.රන්ගිරි දඹුල්ල ජාත්‍යන්තර ක්‍රිකට් ක්‍රීඩාංගනයේ පැවැත්වෙන තරගය අද රාත්‍රී 07.00ට ආරම්භ කිරීමට නියමිතයි.",
        "timestamp": "2025-06-08T14:30:00",
        "url": "https://sinhala.newsfirst.lk/2025/06/24/",
        "source": "NewsFirst Sri Lanka",
        "category": "Sports",
        "subcategory": "Cricket",
        "persons": [],
        "locations": ["දඹුල්ල", "ජාත්‍යන්තර ක්‍රිකට් ක්‍රීඩාංගනයේ", "රන්ගිරි දඹුල්ල"],
        "events": ["තරගාවලියේ","ක්‍රිකට් තරගාවලිය"],
        "organizations": ["ශ්‍රී ලංකා කණ්ඩායම","බංග්ලාදේශ"]
    }

    score, details, debug_outputs = check_fake(news_json, debug=True)
    print(f"\nFinal composite score: {score:.3f}")
    print("Breakdown:", details)
    print("News is", "NOT FAKE ✅" if score >= 0.7 else "SUSPICIOUS (possibly FAKE) ❌")
