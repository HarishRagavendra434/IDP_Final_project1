import json
import time
import logging
import streamlit as st

from modules.ingestion import load_documents
from modules.preprocessing import preprocess_image
from modules.ocr_engine import extract_text
from modules.text_cleaner import clean_text
from modules.entity_extractor import extract_entities
from modules.validation import validate_fields
from modules.classifier import classify_document
from database.mongo_handler import store_results

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

st.set_page_config(
    page_title="Intelligent Document Processing System",
    layout="wide"
)

st.title("Intelligent Document Processing System")

st.sidebar.header("Processing Settings")

document_option = st.sidebar.selectbox(
    "Document Type",
    [
        "Auto Detect",
        "Invoice",
        "Resume",
        "KYC",
        "Insurance",
        "Healthcare",
        "Logistics",
        "Government"
    ]
)

show_ocr = st.sidebar.checkbox(
    "Show OCR Output",
    value=True
)

show_processed = st.sidebar.checkbox(
    "Show Processed Image",
    value=False
)

enable_validation = st.sidebar.checkbox(
    "Enable Validation",
    value=True
)

uploaded_files = st.file_uploader(
    "Upload Documents",
    type=["pdf", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if "success_count" not in st.session_state:
    st.session_state.success_count = 0

if "failed_count" not in st.session_state:
    st.session_state.failed_count = 0

if uploaded_files:

    overall_results = []

    for uploaded_file in uploaded_files:

        st.subheader(uploaded_file.name)

        try:

            start_time = time.time()

            with st.spinner("Processing document"):

                pages = load_documents(uploaded_file)

                file_results = []

                for page_number, page in enumerate(pages):

                    processed_image = preprocess_image(page)

                    if show_processed:
                        st.image(
                            processed_image,
                            caption=f"Processed Page {page_number + 1}"
                        )

                    ocr_response = extract_text(processed_image)

                    if isinstance(ocr_response, tuple):

                        extracted_text = ocr_response[0]
                        confidence_score = ocr_response[1]

                    else:

                        extracted_text = ocr_response
                        confidence_score = 85

                    cleaned_text = clean_text(extracted_text)

                    predicted_type = classify_document(cleaned_text)

                    if document_option == "Auto Detect":
                        document_type = predicted_type
                    else:
                        document_type = document_option

                    extracted_entities = extract_entities(
                        cleaned_text,
                        document_type
                    )

                    if enable_validation:

                        validated_entities = validate_fields(
                            extracted_entities
                        )

                    else:

                        validated_entities = extracted_entities

                    page_result = {
                        "page_number": page_number + 1,
                        "document_type": document_type,
                        "confidence_score": confidence_score,
                        "entities": validated_entities
                    }

                    file_results.append(page_result)

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"Detected Document Type: {document_type}"
                        )

                        st.metric(
                            "OCR Confidence",
                            f"{confidence_score}%"
                        )

                    with col2:

                        if confidence_score < 70:

                            st.warning(
                                "Low OCR confidence detected"
                            )

                        else:

                            st.success(
                                "OCR confidence acceptable"
                            )

                    if show_ocr:

                        st.text_area(
                            f"OCR Output - Page {page_number + 1}",
                            cleaned_text,
                            height=220
                        )

                    st.json(validated_entities)

                store_results(
                    uploaded_file.name,
                    document_type,
                    file_results
                )

                json_output = json.dumps(
                    file_results,
                    indent=4
                )

                st.download_button(
                    label="Download JSON Output",
                    data=json_output,
                    file_name=f"{uploaded_file.name}.json",
                    mime="application/json"
                )

                processing_time = round(
                    time.time() - start_time,
                    2
                )

                st.success(
                    f"Processing completed in "
                    f"{processing_time} seconds"
                )

                st.session_state.success_count += 1

                overall_results.append(
                    {
                        "file_name": uploaded_file.name,
                        "status": "Success"
                    }
                )

                logging.info(
                    f"{uploaded_file.name} processed successfully"
                )

        except Exception as error:

            st.session_state.failed_count += 1

            logging.error(
                f"{uploaded_file.name} failed: {error}"
            )

            overall_results.append(
                {
                    "file_name": uploaded_file.name,
                    "status": "Failed"
                }
            )

            st.error(
                f"Processing failed: {error}"
            )

    st.divider()

    st.header("Processing Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Successful Files",
            st.session_state.success_count
        )

    with col2:

        st.metric(
            "Failed Files",
            st.session_state.failed_count
        )

    st.json(overall_results)