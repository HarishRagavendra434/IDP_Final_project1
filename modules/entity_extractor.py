import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text, document_type):

    document = nlp(text)

    extracted_data = {}

    names = []
    organizations = []

    for entity in document.ents:

        if entity.label_ == "PERSON":
            names.append(entity.text)

        if entity.label_ == "ORG":
            organizations.append(entity.text)

    emails = re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+",
        text
    )

    phones = re.findall(
        r"\+?\d[\d\s\-]{8,}",
        text
    )

    dates = re.findall(
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
        text
    )

    amounts = re.findall(
        r"\$?\d+(?:,\d+)?(?:\.\d+)?",
        text
    )

    extracted_data["DocumentType"] = document_type
    extracted_data["Names"] = list(set(names))
    extracted_data["Organizations"] = list(set(organizations))
    extracted_data["Emails"] = emails
    extracted_data["Phones"] = phones
    extracted_data["Dates"] = dates
    extracted_data["Amounts"] = amounts

    return extracted_data