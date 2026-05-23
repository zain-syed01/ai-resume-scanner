from pypdf import PdfReader
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:

    try:

        pdf_file = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_file)

        extracted_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

        return extracted_text.strip()
    
    except Exception as e:
        raise Exception(f"Failed to parse PDF document: {str(e)}")




    

