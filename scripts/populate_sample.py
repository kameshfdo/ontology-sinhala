"""
Example CLI script that lives outside the package.
Run with:  python -m scripts.populate_sample
"""
from datetime import datetime
from models import FormattedNewsArticle
from manager import OntologyManager

if __name__ == "__main__":
    manager = OntologyManager()
    manager.add_article(
        FormattedNewsArticle(
            headline="ඊශ්‍රායලය සහ ඉරානය සටන් විරාමයට එකඟ වෙයි",
            content="ඊශ්‍රායලය සටන් විරාමයට එකඟ වූ බව එරට අග්‍රාමාත්‍ය බෙන්ජමින් නෙතන්යාහු විසින් තහවුරු කර තිබේ ඒ එරට " \
            "අග්‍රාමාත්‍ය කාර්යාලය හරහා නිවේදනයක් නිකුත් කරමින් මේ අතර ඉරාන රාජ්‍ය රූපවාහිනිය නිවේදනයක් නිකුත් කරමින් පැවසුවේ සටන් විරාමය ආරම්භ වී ඇති බවයි ඉරානය සහ ඊශ්‍රායලය අතර සටන් විරාමය  ක්‍රියාත්මක බව ඇමරිකානු ජනාධිපති ඩොනල්ඩ් ට්‍රම්ප් සිය" \
            "සමාජ මාධ්‍යයෙහි සටහනක් තබමින් පවසා තිබූ පසුබමක ෙදෙරට එම සටන් විරාමයට එකඟතාවය පළ කර තිබේ",
            timestamp=datetime(2025, 6, 8, 14, 30),
            url="https://sinhala.newsfirst.lk/2025/06/24/",
            source="NewsFirst Sri Lanka",
        )

    )
    manager.save()
    print("Ontology updated & saved:", manager.path)
