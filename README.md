# PDF Processor Script

A Python script for processing PDFs by extracting text, filtering non-natural language substrings, and saving the results as new PDFs. Optionally, it can save the processed text as `.txt` files.

---

## **Features**
- Extracts text from PDFs.
- Filters non-natural language substrings based on a length threshold.
- Saves the processed content back as PDFs.
- Optionally saves the processed text as `.txt` files.
- Supports batch processing of all PDFs in a folder.
- Offers raw text processing without filtering.

---

## **Arguments**
| Argument              | Default Value       | Description                                                                 |
|-----------------------|---------------------|-----------------------------------------------------------------------------|
| `--length-threshold`  | `10`               | Sets the maximum allowed length for non-natural language substrings.        |
| `--input-folder`      | `pdfs_to_convert`  | Folder containing PDFs to process.                                         |
| `--output-folder`     | `converted_pdfs`   | Folder where processed PDFs will be saved.                                 |
| `--process-raw`       | `False`            | If set, converts PDFs to text and back without filtering.                  |
| `--text-output`       | `None`             | Folder where processed text will be saved as `.txt` files (optional).      |
