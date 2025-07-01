def load_ontology(ontology_path: str):
    from owlready2 import get_ontology
    return get_ontology(ontology_path).load()

def get_classes(ontology):
    return list(ontology.classes())