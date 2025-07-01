def execute_query(query: str) -> list:
    from owlready2 import get_ontology
    from owlready2 import default_world

    # Load the ontology
    ontology = get_ontology("path_to_your_ontology.owl").load()

    # Execute the SPARQL query
    results = default_world.sparql(query)

    # Convert results to a list of dictionaries
    result_list = []
    for row in results:
        result_dict = {str(var): row[var] for var in row}
        result_list.append(result_dict)

    return result_list