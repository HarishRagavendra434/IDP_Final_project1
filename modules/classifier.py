
def classify_document(text):

    text = text.lower()

    if "invoice" in text:
        return "Invoice"

    if "resume" in text:
        return "Resume"

    if "policy" in text:
        return "Insurance"

    if "aadhaar" in text:
        return "KYC"

    return "General"
