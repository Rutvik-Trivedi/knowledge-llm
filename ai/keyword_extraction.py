from typing import Dict

import spacy
from nltk.tokenize import sent_tokenize  # type: ignore

nlp = spacy.load("en_core_web_sm")


def _extract_keywords_from_single_sentence(text: str) -> list:
    text = text.strip().lower()
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]


def extract_keywords(text: str, top_k: int = 3) -> list:
    text = text.strip()
    if not text:
        return []
    sentences = sent_tokenize(text)
    keywords = []
    for sentence in sentences:
        sent_keywords = _extract_keywords_from_single_sentence(sentence)
        keywords.extend(sent_keywords)
    keyword_freq: Dict[str, int] = {}
    for keyword in keywords:
        keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
    sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
    return [kw[0] for kw in sorted_keywords[:top_k]]
