import json
from ontology_sinhala.manager import OntologyManager
from ontology_sinhala.ontology_populator import populate_article_from_json

if __name__ == "__main__":
    manager = OntologyManager()
    
    # Here is an example array; in production, load from a file or database
    sample_dataset = [
        {
            "headline": "ඊශ්‍රායලය සහ ඉරානය සටන් විරාමයට එකඟ වෙයි",
            "content": "ඊශ්‍රායලය සටන් විරාමයට එකඟ වූ බව ...",
            "timestamp": "2025-06-08T14:30:00",
            "url": "https://sinhala.newsfirst.lk/2025/06/24/",
            "source": "NewsFirst Sri Lanka",
            "category": "PoliticsAndGovernance",
            "subcategory": "InternationalPolitics",
            "persons": ["අග්‍රාමාත්‍ය", "බෙන්ජමින්", "නෙතන්යාහු", "ජනාධිපති", "ඩොනල්ඩ්", "ට්‍රම්ප්"],
            "locations": ["ඊශ්‍රායලය", "ඉරානය", "ඇමරිකා"],
            "events": ["සටන් විරාමය"],
            "organizations": ["කාර්යාලය"]
        },
        # add more sample dicts here...
    ]
    
    for article_json in sample_dataset:
        populate_article_from_json(article_json, manager)

    manager.save()
    print("Ontology updated & saved:", manager.path)
    print("Sample dataset populated successfully.")
    print("Sample dataset:", json.dumps(sample_dataset, ensure_ascii=False, indent=2))
    print("Ontology path:", manager.path)
    print("Ontology version:", manager.version)
    print("Ontology last updated:", manager.last_updated)
    print("Ontology size:", manager.size)
    print("Ontology stats:", manager.stats)
    print("Ontology categories:", manager.categories)
    print("Ontology subcategories:", manager.subcategories)
    print("Ontology persons:", manager.persons)
    print("Ontology locations:", manager.locations)
    print("Ontology events:", manager.events)
    print("Ontology organizations:", manager.organizations)
    print("Ontology articles:", manager.articles)   
