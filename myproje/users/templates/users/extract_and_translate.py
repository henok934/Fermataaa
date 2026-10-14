import os
import json
import re
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

HTML_DIR = '.'  # የፕሮጀክትህ ማህደር
english_texts = {}
amharic_texts = {}

# ጉግል ትርጉምን በመጠቀም እንግሊዝኛን ወደ አማርኛ ለመቀየር
translator = GoogleTranslator(source='en', target='am')

def clean_text(text):
    # ጂንጃ ታጎችን ማስወገድ ({% ... %} እና {{ ... }})
    text = re.sub(r'\{%.*?%\}', '', text)
    text = re.sub(r'\{\{.*?\}\}', '', text)
    # ተጨማሪ ክፍተቶችን ማስተካከል
    return " ".join(text.split())

def extract_and_translate():
    for root, dirs, files in os.walk(HTML_DIR):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f.read(), 'html.parser')
                        
                        # ስክሪፕት እና ስታይል ማስወገድ
                        for element in soup(['script', 'style', 'noscript']):
                            element.decompose()
                        
                        text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'button', 'span', 'label', 'th', 'td', 'li']
                        
                        for element in soup.find_all(text_tags):
                            raw_text = element.get_text(separator=' ', strip=True)
                            cleaned = clean_text(raw_text)
                            
                            # ባዶ ያልሆኑ፣ ቁጥር ብቻ ያልሆኑ፣ ኤችቲኤምኤል/ጂንጃ ያልሆኑ
                            if cleaned and not cleaned.isdigit() and len(cleaned) > 1:
                                if not cleaned.startswith('<') and '{' not in cleaned:
                                    if cleaned not in english_texts:
                                        english_texts[cleaned] = cleaned
                                        
                                        # በራሱ ወደ አማርኛ መተርጎም
                                        try:
                                            translated = translator.translate(cleaned)
                                            amharic_texts[cleaned] = translated if translated else cleaned
                                            print(f"Translated: {cleaned} -> {translated}")
                                        except Exception as et:
                                            print(f"Translation failed for '{cleaned}': {et}")
                                            amharic_texts[cleaned] = cleaned
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # ውጤቱን ወደ translations.json መጻፍ
    output_data = {
        "en": english_texts,
        "am": amharic_texts
    }
    
    with open('translations.json', 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=4)
    
    print("\nSuccess! All texts extracted and translated into translations.json")

if __name__ == '__main__':
    extract_and_translate()
