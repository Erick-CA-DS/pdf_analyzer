import os
import pdfplumber
import re

def read_pdf_and_count_keywords(pdf_path, keywords):
    try:
        total_keyword_count = 0
        total_word_count = 0

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text().lower()
                words = re.findall(r'\b\w+\b', page_text)
                total_word_count += len(words)

                for word in words:
                    for keyword in keywords:
                        if keyword in word:
                            total_keyword_count += 1

        return total_keyword_count, total_word_count

    except Exception as e:
        print(f"Error reading PDF file {pdf_path}: {e}")
        return None, None

def process_directory(directory_path, target_keywords, output_file):
    with open(output_file, 'w') as output:
        output.write("Title\tNumber of Keywords\tNumber of Words\tKeyword Density\n")

        for filename in os.listdir(directory_path):
            if filename.endswith(".pdf"):
                pdf_file_path = os.path.join(directory_path, filename)
                title = os.path.splitext(filename)[0]

                keyword_count, word_count = read_pdf_and_count_keywords(pdf_file_path, target_keywords)

                if keyword_count is not None and word_count is not None:
                    keyword_density = keyword_count / word_count if word_count > 0 else 0
                    output.write(f"{title}\t{keyword_count}\t{word_count}\t{keyword_density}\n")
                    print(f"Processed {title}: {keyword_count} keywords, {word_count} words")

# Example usage
directory_path = "/Users/yerkinmudebayev/Documents/2013-2018"
output_file = "output_keywords_density.txt"
target_keywords = ["confidence", "trust", "investment"]

process_directory(directory_path, target_keywords, output_file)