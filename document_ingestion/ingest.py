import pdfplumber
import docx
import mailparser

def extract_from_pdf(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_from_docx(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_from_email(file_path):
    text = ""
    try:
        mail = mailparser.parse_from_file(file_path)
        text = mail.body
    except Exception as e:
        print(f"Error reading EML: {e}")
    return text

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_from_docx(file_path)
    elif file_path.endswith(".eml"):
        return extract_from_email(file_path)
    else:
        raise ValueError("Unsupported file type")