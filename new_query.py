from owlready2 import get_ontology, default_world

# Load the ontology
onto_path = "new-ontology-v1.owl"  # Update with actual path
onto = get_ontology(f"file://{onto_path}").load()


# Define SPARQL queries
#-----------------------------------------cricket queries-----------------------------------------
# Query to get cricket teams
query1 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?teamName
WHERE {
  ?article ns:hasCategory ?category .
  FILTER (?category = ns:Cricket) .
  ?article ns:hasCricketTeam ?team .
  ?team ns:canonicalName ?teamName .
}
"""

# Query to get cricket players
query2 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?playerName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Cricket)
  ?article ns:hasCricketPlayer ?player.
  ?player ns:canonicalName ?playerName
}
"""
# Query to get cricket venues
query3 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?venueName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Cricket)
  ?article ns:hasCricketVenue ?venue.
  ?venue ns:canonicalName ?venueName
}
"""

# Query to get cricket tournaments
query4 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?tournamentName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Cricket)
  ?article ns:hasCricketTournament ?tournement.
  ?tournement ns:canonicalName ?tournamentName
}
"""
#-----------------------------------------football queries-----------------------------------------
# Query to get football teams
query5 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?teamName
WHERE {
  ?article ns:hasCategory ?category .
  FILTER (?category = ns:Football) .
  ?article ns:hasFootballTeam ?team .
  ?team ns:canonicalName ?teamName .
}
"""
# Query to get football players
query6 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?playerName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Football)
  ?article ns:hasFootballPlayer ?player.
  ?player ns:canonicalName ?playerName
}
"""
# Query to get football venues
query7 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?venueName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Cricket)
  ?article ns:hasCricketVenue ?venue.
  ?venue ns:canonicalName ?venueName
}
"""

# query to get football tournaments
query8 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?tournamentName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Football)
  ?article ns:hasFootballTournament ?tournement.
  ?tournement ns:canonicalName ?tournamentName
}
"""

#------------------------------------------OTHER SPORT  queries-----------------------------------------

query9 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?teamName
WHERE {
  ?article ns:hasCategory ?category .
  FILTER (?category = ns:Other) .
  ?article ns:hasTeam ?team .
  ?team ns:canonicalName ?teamName .
}
"""


query9 = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?playerName
WHERE {
  ?article ns:hasCategory ?category 
  FILTER (?category = ns:Other)
  ?article ns:hasPlayer ?player.
  ?player ns:canonicalName ?playerName
}
"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

query9 = """

"""

























results = list(default_world.sparql(query1))

# Print results
for team in results:
    print(f"Teams: {team}")
