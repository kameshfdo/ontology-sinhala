"""
Central place for constants so you don’t repeat literals across modules.
"""
from pathlib import Path

ONTOLOGY_IRI: str  = (
    "http://www.semanticweb.org/kameshfdo/ontologies/2025/5/new-ontology-v1"
)
ONTOLOGY_FILE: Path = Path(__file__).parent.parent / "new-ontology-v1.owl"
