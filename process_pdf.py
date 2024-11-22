import os
import re
import argparse
import textwrap
from PyPDF2 import PdfReader
from nltk.corpus import words as nltk_words
import nltk

nltk.download("words")
ENGLISH_WORDS = set(nltk_words.words())

# Valid months for date detection
VALID_MONTHS = {"jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"}

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using PyPDF2."""
    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        # Extract text for each page and add a newline for separation
        page_text = page.extract_text()
        if page_text:
            text.append(page_text.strip() + "\n")
    return "\n".join(text)

def is_english_word_or_number(word):
    """
    Checks if a word is an English word, valid date, or standard number.
    """
    # Check if word is a valid English word
    if word.lower() in ENGLISH_WORDS:
        return True
    # Check if word is a valid month or numeric year
    if word.lower() in VALID_MONTHS or word.isdigit():
        return True
    # Check if word is a standard number (e.g., 2.1)
    if re.match(r"^\d+(\.\d+)?$", word):
        return True
    return False

def filter_text(text, threshold):
    """
    Filters text to remove non-English words or substrings above a certain threshold.
    Substrings under the threshold are included even if they fail the English word check.
    """
    # Split text into segments based on spaces and commas
    segments = re.split(r"[ ,]+", text)
    filtered_segments = []
    for segment in segments:
        # Check if segment is an English word, valid date, or number, or under the length threshold
        if is_english_word_or_number(segment) or len(segment) <= threshold:
            filtered_segments.append(segment)
        else:
            # Clean excessive non-alphanumeric characters and check length again
            cleaned_segment = re.sub(r"[^a-zA-Z0-9\s.,!?']+", "", segment)
            if len(cleaned_segment) <= threshold:
                filtered_segments.append(cleaned_segment)
    return " ".join(filtered_segments)

def save_text_as_file(text, output_folder, file_name, wrap_width=80):
    """
    Saves the processed text as a .txt file in the specified folder with line wrapping.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.txt")
    wrapped_text = "\n".join(textwrap.fill(line, width=wrap_width) for line in text.splitlines())
    with open(output_path, "w", encoding="utf-8") as text_file:
        text_file.write(wrapped_text)

def process_folder(input_folder, output_folder, threshold, process_raw, wrap_width):
    """
    Processes all PDF files in the input folder, filtering text
    and saving the results in the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".pdf"):
            input_path = os.path.join(input_folder, file_name)

            # Step 1: Extract text
            extracted_text = extract_text_from_pdf(input_path)
            # Step 2: Process raw or filter text
            if process_raw:
                processed_text = extracted_text
            else:
                processed_text = filter_text(extracted_text, threshold)
            # Step 3: Save the processed text as a .txt file
            save_text_as_file(processed_text, output_folder, file_name, wrap_width)
            print(f"Processed and saved text: {file_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PDFs into text files.")
    parser.add_argument("--length-threshold", type=int, default=10, help="Set the threshold for non-English word length (default: 10).")
    parser.add_argument("--input-folder", type=str, default="pdfs_to_convert", help="Folder containing PDFs to process.")
    parser.add_argument("--output-folder", type=str, default="text_output", help="Folder to save processed text files.")
    parser.add_argument("--process-raw", action="store_true", help="If set, processes PDFs to text without filtering.")
    parser.add_argument("--wrap-width", type=int, default=80, help="Maximum width of lines in the output text files (default: 80).")

    args = parser.parse_args()

    # Process the folder with the given settings
    process_folder(args.input_folder, args.output_folder, args.length_threshold, args.process_raw, args.wrap_width)
