from rdflib import Graph, Namespace, URIRef

# Load your ontology
g = Graph()
g.parse("new-ontology-v1.owl", format="xml")  # Change to the correct path if needed

# Define your ontology's namespace
ns = Namespace("http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#")

# Register the namespace for cleaner querying
g.bind("ns", ns)

# Define the SPARQL query
query = """
PREFIX ns: <http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1#>

SELECT ?article ?team
WHERE {
  ?article ns:hasCategory ?category .
  FILTER (?category = ns:Sports || ?category = ns:Cricket) .
  ?article ns:hasCricketTeam ?team .
}
"""

# Execute the query
results = g.query(query)
print("Query executed successfully.")
print("Number of results:", len(results))
# Print the results
for row in results:
    print(f"Article: {row.article}, Cricket Team: {row.team}")
