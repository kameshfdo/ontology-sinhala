# verify_news Verification Module

This module, `verify_news`, is designed to assess the truthfulness of news articles by leveraging an ontology. It utilizes the Owlready2 library for ontology manipulation and SPARQL for querying relationships and facts.

## Overview

The `verify_news` module provides tools to verify the accuracy of news articles by checking them against a predefined ontology. It includes functionalities to retrieve relationships between entities and validate claims made in articles.

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

### Verifying Articles

To verify a news article, you can use the `NewsVerifier` class from the `verifier.py` file. Here is a simple example:

```python
from src.verifier import NewsVerifier

verifier = NewsVerifier()
is_true = verifier.verify_article("Some news article text here.")
print(f"Article truthfulness: {is_true}")
```

### Retrieving Relationships

You can also retrieve relationships related to a specific entity using the `get_relationships` method:

```python
relationships = verifier.get_relationships("Entity Name")
print(relationships)
```

## Files

- `src/__init__.py`: Marks the directory as a Python package.
- `src/verifier.py`: Contains the `NewsVerifier` class for article verification.
- `src/sparql_queries.py`: Functions for executing SPARQL queries.
- `src/owlready_utils.py`: Utility functions for working with Owlready2.
- `src/config.py`: Configuration settings for the module.
- `requirements.txt`: Lists the dependencies required for the project.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.