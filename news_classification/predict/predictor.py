import pickle
from transformers import TextClassificationPipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TextClassificationPipeline

# This script provides a function to predict the subcategory of a news article
subcategory_to_main = {
    "InternationalPolitics": "PoliticsAndGovernance",
    "DomesticPolitics": "PoliticsAndGovernance",
    "TechAndInnovation": "ScienceAndTechnology",
    "ResearchAndSpace": "ScienceAndTechnology",
    "ScreenAndStage": "CultureAndEntertainment",
    "MusicAndArts": "CultureAndEntertainment",
    "Cricket": "Sports",
    "Football": "Sports",
    "Other": "Sports",
    "CrimeReport": "CrimeAndJustice",
    "CourtsAndInvestigation": "CrimeAndJustice" 
}

def predict_category(model, tokenizer, text, label_encoder=None, sub_to_main=None, device=-1):
    """
    Predicts subcategory and maps it to a main category (if mapping provided).

    Args:
        model: HuggingFace model.
        tokenizer: Tokenizer.
        text (str): Input text.
        label_encoder (LabelEncoder): For decoding subcategory label index.
        sub_to_main (dict): Mapping from subcategory to main category.
        device (int): 0 for GPU, -1 for CPU.

    Returns:
        tuple: (subcategory, main_category or None)
    """
    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=False, device=device)
    result = pipeline(text)[0]

    if label_encoder is not None:
        if result['label'].startswith("LABEL_"):
            sub_idx = int(result['label'].replace("LABEL_", ""))
        else:
            sub_idx = int(result['label'])
        subcategory = label_encoder.inverse_transform([sub_idx])[0]
    else:
        subcategory = result['label']

    main_category = sub_to_main.get(subcategory, None) if sub_to_main else None
    return subcategory, main_category

model_path = "./models"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
# Create a pipeline for text classification
pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=False, device=0) 


if __name__ == "__main__":

    # Load from file
    with open('label_encoder.pkl', 'rb') as f:
        le = pickle.load(f)

    # Example text
    text = "ඊශ්‍රායලයෙන් ඉරානයේ ප්‍රදේශ කිහිපයකට ගුවන් ප්‍රහාර"
    result = pipeline(text)
    print(result)
