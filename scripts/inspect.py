from ontology_sinhala.manager import OntologyManager

manager = OntologyManager()
onto = manager.ontology

# Example: List all NewsArticles
print("NewsArticles:")
for article in onto.NewsArticle.instances():
    print(f"  Title: {article.hasTitle}")
    print(f"  Source: {article.publisherName}")
    print(f"  URL: {article.hasSourceURL}")
    print(f"  Date: {article.hasPublicationDate}")
    print(f"  Processed: {article.processedDate}")
    print(f"  Full Text: {article.hasFullText}")
    # print(f"  Mentions: {[e.name for e in article.mentionsEntity]}")
    print(f"  Categories: {[c.name for c in article.hasCategory]}")