from pathlib import Path
from pypdf import PdfReader

def extract_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    return text

if __name__ == "__main__":
    pdf_path = Path("../data/AtomicHabits.pdf")
    output_path = Path("../data/atomic_habits_full.md")

    text = extract_pdf_text(str(pdf_path))
    output_path.write_text(text, encoding="utf-8")

    print("✅ Text extraction complete. Saved to:", output_path)
