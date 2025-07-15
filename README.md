Of course! Here’s a **complete, copy-paste-ready `README.md`** for your project, including an **API usage section** and all the best practices in Markdown formatting:

---

````markdown
# ontology-sinhala

A FastAPI-based system for verifying news authenticity in Sinhala using ontologies.

---

## 🚀 Getting Started

### 1. Clone the repository and navigate to the project directory:

```bash
cd ontology-sinhala
````

### 2. Create and activate a Python virtual environment:

```bash
python3 -m venv pyenv
source pyenv/bin/activate
```

### 3. Install all dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI server:

```bash
uvicorn verify_news.main:app --reload
```

The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🗄️ Repopulating the Ontology

If you need to repopulate the ontology, run the following command:

```bash
python -m scripts.populate_sample
```

---

## 📝 Notes

* **Virtual Environment:**
  Always activate your virtual environment before installing dependencies or running the server:

  ```bash
  source pyenv/bin/activate
  ```

* **API Documentation:**
  Once the server is running, access the automatic API documentation at:
  [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* **Ontology File:**
  Ensure the `new-ontology-v1.owl` file is present in your project root directory.

---

## 📂 Project Structure

```
ontology-sinhala/
├── verify_news/
│   ├── main.py
│   ├── query.py
│   ├── querymapping.py
│   └── ...
├── scripts/
│   └── populate_sample.py
├── new-ontology-v1.owl
├── requirements.txt
└── README.md
```

---

## 📡 API Usage

### Endpoint

* **POST** `/check_fake`

### Request Body Example

```json
{
  "headline": "සත්කාරක ශ්‍රී ලංකා - බංග්ලාදේශ දෙවැනි පන්දුවාර 20යි 20 ක්‍රිකට් තරගය අද (13) පැවැත්වේ",
  "content": "තරගාවලියේ පළමු තරගය කඩුලු 7 කින් ජය ගත්තේ ශ්‍රී ලංකා කණ්ඩායමයි.ඒ අනුව ඔවුන් තරග 3කින් සමන්විත පන්දුවාර 20යි 20 ක්‍රිකට් තරගාවලිය තරග 1ට 0ක් ලෙස පෙරමුණ ගෙන සිටී.රන්ගිරි දඹුල්ල ජාත්‍යන්තර ක්‍රිකට් ක්‍රීඩාංගනයේ පැවැත්වෙන තරගය අද රාත්‍රී 07.00ට ආරම්භ කිරීමට නියමිතයි.",
  "timestamp": "2025-06-08T14:30:00",
  "url": "https://sinhala.newsfirst.lk/2025/06/24/",
  "source": "NewsFirst Sri Lanka",
  "category": "Sports",
  "subcategory": "Cricket",
  "persons": [],
  "locations": ["දඹුල්ල", "ජාත්‍යන්තර ක්‍රිකට් ක්‍රීඩාංගනයේ", "රන්ගිරි දඹුල්ල"],
  "events": ["තරගාවලියේ", "ක්‍රිකට් තරගාවලිය"],
  "organizations": ["ශ්‍රී ලංකා කණ්ඩායම", "බංග්ලාදේශ"]
}
```

### Example CURL Request

```bash
curl -X POST "http://127.0.0.1:8000/check_fake" \
     -H "Content-Type: application/json" \
     -d '{
       "headline": "සත්කාරක ශ්‍රී ලංකා - බංග්ලාදේශ දෙවැනි පන්දුවාර 20යි 20 ක්‍රිකට් තරගය අද (13) පැවැත්වේ",
       "content": "තරගාවලියේ පළමු තරගය කඩුලු 7 කින් ජය ගත්තේ ශ්‍රී ලංකා කණ්ඩායමයි.ඒ අනුව ඔවුන් තරග 3කින් සමන්විත පන්දුවාර 20යි 20 ක්‍රිකට් තරගාවලිය තරග 1ට 0ක් ලෙස පෙරමුණ ගෙන සිටී.රන්ගිරි දඹුල්ල ජාත්‍යන්තර ක්‍රිකට් ක්‍රීඩාංගනයේ පැවැත්වෙන තරගය අද රාත්‍රී 07.00ට ආරම්භ කිරීමට නියමිතයි.",
       "timestamp": "2025-06-08T14:30:00",
       "url": "https://sinhala.newsfirst.lk/2025/06/24/",
       "source": "NewsFirst Sri Lanka",
       "category": "Sports",
       "subcategory": "Cricket",
       "persons": [],
       "locations": ["දඹුල්ල", "ජාත්‍යන්තර ක්‍රිකට් ක්‍රීඩාංගනයේ", "රන්ගිරි දඹුල්ල"],
       "events": ["තරගාවලියේ", "ක්‍රිකට් තරගාවලිය"],
       "organizations": ["ශ්‍රී ලංකා කණ්ඩායම", "බංග්ලාදේශ"]
     }'
```

### Sample Response

```json
{
  "final_score": 0.81,
  "result": "NOT FAKE ✅",
  "breakdown": {
    "entity_similarity": 0.95,
    "semantic_similarity": 0.73,
    "source_credibility": 1.0,
    "per_entity": {
      "persons": 1.0,
      "locations": 0.92,
      "events": 0.97,
      "organizations": 0.89
    }
  }
}
```

#### Score Interpretation

* **NOT FAKE ✅** : Score ≥ 0.7
* **MIGHT BE FAKE ⚠️** : 0.4 ≤ Score < 0.7
* **POSSIBLY FAKE ❌** : Score < 0.4

---

## 🤝 Contributions

Pull requests, issues, and improvements are welcome!

---

## 📜 License

This project is for research and educational purposes.

---

```

---

Let me know if you want to add author info, a description of the model/approach, or anything else!
```
