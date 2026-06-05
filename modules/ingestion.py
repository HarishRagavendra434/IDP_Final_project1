
import fitz
from PIL import Image
import io

def load_documents(uploaded_file):

    file_bytes = uploaded_file.read()

    if uploaded_file.type == "application/pdf":

        document = fitz.open(
            stream=file_bytes,
            filetype="pdf"
        )

        pages = []

        for page in document:

            pixmap = page.get_pixmap(dpi=300)

            image = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples
            )

            pages.append(image)

        return pages

    image = Image.open(io.BytesIO(file_bytes))

    return [image]
