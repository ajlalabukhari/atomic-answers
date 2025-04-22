import re
from pathlib import Path
import re

def clean_markdown(text: str) -> str:
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        stripped = line.strip()

        # Convert bullets like • or weird symbols
        if stripped.startswith(("•", "‣", "▪", "*")):
            stripped = "- " + stripped[1:].strip()

        # Detect ALL CAPS headings and title-case them
        if stripped.isupper() and len(stripped.split()) < 10:
            stripped = f"## {stripped.title()}"

        # Convert "Problem #..." to heading
        if re.match(r"Problem\s?#\d+", stripped, re.IGNORECASE):
            stripped = f"### {stripped}"

        # Convert 'Chapter Summary' into heading
        if "chapter summary" in stripped.lower():
            stripped = "## Chapter Summary"

        cleaned.append(stripped)

    # Rebuild the markdown content
    cleaned_text = "\n".join(cleaned)

    # Replace multiple blank lines with max 1
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)

    return cleaned_text

def split_into_chapters(md_path: str, output_dir: str):
    content = Path(md_path).read_text(encoding="utf-8")
    Path(output_dir).mkdir(parents=True, exist_ok=True)


    # Match chapter breaks: a line with only a number followed by a title
    chapter_pattern = re.compile(r"(?m)^(\d+)\n([^\n]+)\n")

    matches = list(chapter_pattern.finditer(content))

    output = []

    # Add intro section (before first numbered chapter)
    if matches:
        intro_text = content[:matches[0].start()].strip()
        intro_text = clean_markdown(intro_text)
        intro_file = Path(output_dir) / "chapter_00_intro.md"
        intro_file.write_text(f"# Introduction\n\n{intro_text}", encoding="utf-8")

        output.append(str(intro_file))

    for idx, match in enumerate(matches):
        chapter_number = match.group(1).zfill(2)
        chapter_title = match.group(2).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        chapter_text = content[start:end].strip()

        chapter_body = clean_markdown(chapter_text)
        chapter_md = f"# Chapter {chapter_number}: {chapter_title}\n\n{chapter_body}"

        chapter_file = Path(output_dir) / f"chapter_{chapter_number}.md"
        if chapter_file.exists():
            print(f"⏭️ Skipping existing {chapter_file.name}")
            continue

        chapter_file.write_text(chapter_md, encoding="utf-8")
        output.append(str(chapter_file))

    print(f"✅ Split into {len(output)} markdown files.")

    # Save everything after the last chapter as additional content
    if matches:
        final_text = content[matches[-1].end():].strip()
        if final_text:
            additional_text = clean_markdown(final_text)
            extra_path = Path("../data/additional_data.md")
            extra_path.write_text("# Additional Content\n\n" + additional_text, encoding="utf-8")
            print("✅ Saved additional content to additional_data.md")

    return output


if __name__ == "__main__":
    split_into_chapters(
        md_path="../data/atomic_habits_full.md",
        output_dir="../data/chapters"
    )
