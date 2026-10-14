import os
import json
import re
from bs4 import BeautifulSoup

HTML_DIR = '.'  # የፕሮጀክትህ ማህደር
english_texts = {}
amharic_texts = {}

def clean_text(text):
    # ጂንጃ ታጎችን ማስወገድ (ለምሳሌ {% if ... %} እና {{ ... }})
    text = re.sub(r'\{%.*?%\}', '', text)
    text = re.sub(r'\{\{.*?\}\}', '', text)
    
    # ተጨማሪ ክፍተቶችን ማስተካከል
    text = " ".join(text.split())
    return text

def extract_from_html():
    for root, dirs, files in os.walk(HTML_DIR):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f.read(), 'html.parser')
                        
                        # 1. ስክሪፕት፣ ስታይል እና ኖስክሪፕት ማስወገድ
                        for element in soup(['script', 'style', 'noscript']):
                            element.decompose()
                        
                        # 2. እውነተኛ ጽሑፍ ሊኖራቸው የሚችሉ ታጎች ብቻ
                        text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'button', 'span', 'label', 'th', 'td', 'li']
                        
                        for element in soup.find_all(text_tags):
                            raw_text = element.get_text(separator=' ', strip=True)
                            cleaned = clean_text(raw_text)
                            
                            # ጽሑፉ ባዶ ካልሆነ፣ ቁጥር ብቻ ካልሆነ እና ኤችቲኤምኤል/ሲኤስኤስ ኮድ ካልሆነ
                            if cleaned and not cleaned.isdigit() and len(cleaned) > 1:
                                # ታጎች ወይም ቁምፊዎች እንዳሉበት ስንፈትሽ
                                if not cleaned.startswith('<') and not '{' in cleaned:
                                    english_texts[cleaned] = cleaned
                                    amharic_texts[cleaned] = ""  # ለአማርኛ ትርጉም ዝግጁ ማድረጊያ
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    # እንደጠየቅከው የ JSON መዋቅር ማዘጋጀት
    output_data = {
        "en": english_texts,
        "am": amharic_texts
    }
    
    with open('translations.json', 'w', encoding='utf-8') as outfile:
        json.dump(output_data, outfile, ensure_ascii=False, indent=4)
    
    print("Success! Clean text extracted without Jinja, HTML, CSS, or JS into translations.json")

if __name__ == '__main__':
    extract_from_html()
