import easyocr
import pytesseract

reader = easyocr.Reader(["en"])

def extract_text(image):

    try:

        result = reader.readtext(image)

        extracted_text = " ".join(
            [item[1] for item in result]
        )

        if len(extracted_text.strip()) < 10:
            extracted_text = pytesseract.image_to_string(image)

        return extracted_text

    except Exception:

        return pytesseract.image_to_string(image)