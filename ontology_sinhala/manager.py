from datetime import datetime
import re
from pathlib import Path
from owlready2 import get_ontology

from .config import ONTOLOGY_FILE, ONTOLOGY_IRI
from .models import FormattedNewsArticle
from . import schema


class OntologyManager:
    """
    Load an existing ontology from disk or create a new one.
    The heavy lifting of defining classes / properties lives in
    `news_ontology.schema`, so this class stays compact and readable.
    """
    def __init__(self,
                 path: Path = ONTOLOGY_FILE,
                 iri: str = ONTOLOGY_IRI):
        self.path = Path(path)
        self.iri  = iri

        if self.path.exists():
            self.ontology = get_ontology(self.path.as_uri()).load()
        else:
            self.ontology = get_ontology(self.iri)
            schema.build_all(self.ontology)            # only once
            self.save()                                # create file on disk

    # ------------------------------------------------------------------ utils

    @staticmethod
    def _safe_name(url: str) -> str:
        name = re.sub(r"^https?://", "", url)
        return re.sub(r"[^a-zA-Z0-9_]", "_", name)[:64]  # truncate to stay tidy

    # ------------------------------------------------------------------ public

    def add_article(self, article: FormattedNewsArticle):
        with self.ontology:
            NewsArticle = self.ontology.NewsArticle     # local shortcut
            individual  = NewsArticle(self._safe_name(article.url))

            # functional props → normal assignment
            individual.hasTitle          = article.headline
            individual.hasPublicationDate= article.timestamp
            individual.hasSourceURL      = article.url
            individual.processedDate     = datetime.utcnow()

            # multi-valued props → .append()
            individual.hasFullText.append(article.content)
            individual.publisherName.append(article.source)

        return individual

    def save(self, fmt: str = "rdfxml"):
    # Ensure the path is passed as a string to avoid issues with PosixPath
        self.ontology.save(file=str(self.path), format=fmt)


