from PyPDF2 import PdfReader
import re

def read_resume(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return clean_text(text)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z ]", " ", text)
    return text
