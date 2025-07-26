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

class TrustedContent(BaseModel):
    trustSementics: str
    title: str
    url: str

# --- News input model
class News(BaseModel):
    # headline: str
    content: str
    # timestamp: str
    # url: str
    source: str
    category: str
    subcategory: str
    persons: List[str] = []
    locations: List[str] = []
    events: List[str] = []
    organizations: List[str] = []

class News(BaseModel):
    #headline: str
    content: str
    #timestamp: str
    #url: str
    #source: str

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
    SELECT DISTINCT ?trustSementics ?title ?url
    WHERE {{
      ?article ns:hasCategory ?cat .
      FILTER (?cat = {category_uri})
      ?article ns:hasFullText ?trustSementics .
      ?article ns:hasTitle ?title .
      ?article ns:hasSourceURL ?url .
    }}
    """
    results = list(default_world.sparql(sparql))
    return [TrustedContent(
        trustSementics=str(r[0]),
        title=str(r[1]),
        url=str(r[2])
    ) for r in results]

def get_semantic_similarity_score(news_text, trusted_texts, api_url="https://relaxing-morally-wallaby.ngrok-free.app/similarity"):
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
    
def get_news_or_not(news_text,api_url="https://relaxing-morally-wallaby.ngrok-free.app/check_news"):
    payload = {
        "text": news_text
    }
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("checking", "")
    except Exception as e:
        print(f"[Error] Could not get news or not from API: {e}")
        return False
    
def get_category_subcategory(news_text, api_url="https://relaxing-morally-wallaby.ngrok-free.app/check_category"): 
    payload = {
        "text": news_text
    }
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("category", ""), result.get("subcategory", "")
    except Exception as e:
        print(f"[Error] Could not get category and subcategory from API: {e}")
        return "", ""
    
def get_entities(news_text, api_url="https://ner-server-v2.onrender.com/ner"):
    payload = {
        "text": news_text
    }
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result.get("persons", []), result.get("locations", []), result.get("events", []), result.get("organizations", [])
    except Exception as e:
        print(f"[Error] Could not get entities from API: {e}")
        return [], [], [], []

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

    # --- Semantic Similarity Ranking ---
    trusted_cont = get_trusted_contents_by_category(subcat)
    content = news_json.get("content", "")
    similarity_results = []
    for t in trusted_cont:
        score = get_semantic_similarity_score(content, [t.trustSementics])  # Send [t], not t!
        similarity_results.append({
            "title": t.title,
            "url": t.url,
            "trustSementics": t.trustSementics,
            "score": score
        })
    similarity_results.sort(key=lambda x: x["score"], reverse=True)
    for idx, item in enumerate(similarity_results, 1):
        item["rank"] = idx

    max_semantic_similarity_score = similarity_results[0]["score"] if similarity_results else 0.0
    semantic_similarity_score = sum(x["score"] for x in similarity_results) / len(similarity_results) if similarity_results else 0.0

    trusted_publishers = get_trusted_publishers()
    publisher = news_json.get("source", "")
    source_credibility_score = get_source_credibility(publisher, trusted_publishers)

    final_score = (
        0.4 * entity_similarity_score +
        0.3 * max_semantic_similarity_score +
        0.3 * source_credibility_score
    )

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
            "semantic_similarity": max_semantic_similarity_score,
            "source_credibility": source_credibility_score,
            "per_entity": avg_scores,
        },
        "semantic_ranking": similarity_results,
    }


# --- FastAPI POST endpoint ---
@app.post("/check_fake")
def check_news(news: News, debug: Optional[bool] = Query(False)):
    # check News validity
    if not news.content:
        return {"error": "Invalid news data. Please provide all required fields."}
    # check if the news is actually news
    is_news = get_news_or_not(news.content)
    print(f"[DEBUG] is_news: {is_news}")
    if is_news != 'news':
        result = "The provided content is not recognized as news."
        return {"error": "The provided content is not recognized as news.", "content": news.dict(), "result": is_news}
    
    # Get category and subcategory
    category, subcategory = get_category_subcategory(news.content)
    if not category or not subcategory:
        return {"error": "Could not determine category or subcategory for the news.", "content": news.dict()}
    
    # Update news_json with category and subcategory
    news_json = news.dict()
    news_json['category'] = category
    news_json['subcategory'] = subcategory

    # Get entities
    persons, locations, events, organizations = get_entities(news.content)
    news_json['persons'] = persons
    news_json['locations'] = locations
    news_json['events'] = events
    news_json['organizations'] = organizations

    # Check for fake news
    result = check_fake(news_json, debug=debug)
    return result
