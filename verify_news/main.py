from fastapi import FastAPI, Request, Body, Query
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from owlready2 import get_ontology, default_world
from rapidfuzz.fuzz import ratio
import requests

# --- Imports for QUERY_MAP, query43, query44
from .querymapping import QUERY_MAP
from .query import query43, query44


# --- FastAPI setup
app = FastAPI()

# --- News input model
class NewsInput(BaseModel):
    headline: str
    content: str
    timestamp: str
    url: str
    source: str
    category: str
    subcategory: str
    persons: List[str] = []
    locations: List[str] = []
    events: List[str] = []
    organizations: List[str] = []

# --- Helper Functions (copied from your script) ---
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
    return 1.0 if news_publisher in trusted_publishers else 0.0

def get_trusted_contents_by_category(category):
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
    return total / len(input_list), debug_pairs

# --- Ontology is loaded once on app startup
@app.on_event("startup")
def load_ontology():
    global onto
    onto = get_ontology("file://new-ontology-v1.owl").load()

# --- Main checking logic, adapted for FastAPI usage ---
def check_fake(news_json, debug=False):
    subcat = news_json.get('subcategory')
    entity_types = ['persons', 'locations', 'events', 'organizations']

    avg_scores = {}
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
        avg, _ = get_average_similarity(values, verified)
        avg_scores[etype] = avg
        weighted_sum += avg * counts[etype]
        total_weight += counts[etype]

    entity_similarity_score = weighted_sum / total_weight if total_weight > 0 else 0.0

    trusted_texts = get_trusted_contents_by_category(subcat)
    content = news_json.get("content", "")
    semantic_similarity_score = get_semantic_similarity_score(content, trusted_texts)

    trusted_publishers = get_trusted_publishers()
    publisher = news_json.get("source", "")
    source_credibility_score = get_source_credibility(publisher, trusted_publishers)

    final_score = (
        0.4 * entity_similarity_score +
        0.3 * semantic_similarity_score +
        0.3 * source_credibility_score
    )

    # Result label based on your new rules
    if final_score >= 0.7:
        result = "NOT FAKE ✅"
    elif final_score >= 0.4:
        result = "MIGHT BE FAKE ⚠️"
    else:
        result = "POSSIBLY FAKE ❌"

    return {
        "final_score": round(final_score, 3),
        "result": result,
        "breakdown": {
            "entity_similarity": entity_similarity_score,
            "semantic_similarity": semantic_similarity_score,
            "source_credibility": source_credibility_score,
            "per_entity": avg_scores
        }
    }

# --- FastAPI POST endpoint ---
@app.post("/check_fake")
def check_news(news: NewsInput, debug: Optional[bool] = Query(False)):
    # Convert model to dict
    news_json = news.dict()
    result = check_fake(news_json, debug=debug)
    return result
