import os
import json
from bs4 import BeautifulSoup

# የቴምፕሌት ማህደርህ ያለበት ትክክለኛ መንገድ (ለምሳሌ './users/templates')
templates_dir = "." 

extracted_texts = set()

print("🔍 የ HTML ፋይሎችን በመቃኘት ላይ...")

for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                    
                    # ስክሪፕት እና ስታይል ኮዶችን እናስወግዳለን
                    for script in soup(["script", "style"]):
                        script.decompose()
                        
                    # የተወሰኑ ታጎች ውስጥ ያሉ ጽሑፎችን ብቻ እንወስዳለን (ለምሳሌ ርዕሶች፣ አዝራሮች፣ ሊንኮች)
                    tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'span', 'label', 'button', 'small'])
                    for tag in tags:
                        text = tag.get_text(strip=True)
                        # ባዶ ያልሆኑ እና አጭር ጽሑፎችን እንይዛለን
                        if text and len(text) < 100 and not text.startswith("{%") and not text.startswith("{{"):
                            extracted_texts.add(text)
            except Exception as e:
                print(f"ማስታወሻ ({file_path}): ማንበብ አልተቻለም - {e}")

print(f"✨ በአጠቃላይ {len(extracted_texts)} ልዩ ጽሑፎች ተገኝተዋል!\n")

# translations.js ፋይልን በራስ-ሰር ማዘጋጀት
js_content = """// በራስ-ሰር የተፈጠረ የቋንቋ መዝገብ (Auto-generated Translations)
const translations = {
    en: {\n"""

# እንግሊዝኛ ጽሑፎቹን በቁልፍ (Key) መልክ እናስገባለን
for i, text in enumerate(sorted(extracted_texts)):
    # ቁልፍ (Key) የሚሆን ቃላትን እናጸዳለን
    safe_key = "".join(e for e in text if e.isalnum())[:20]
    if not safe_key:
        safe_key = f"key_{i}"
    else:
        safe_key = f"{safe_key}_{i}"
        
    js_content += f'        "{safe_key}": "{text}",\n'

js_content += """    },
    am: {
        // እዚህ ጋር የአማርኛ ትርጉሞችን ማስገባት ትችላለህ
    },
    om: {
        // እዚህ ጋር የኦሮምኛ ትርጉሞችን ማስገባት ትችላለህ
    }
};

function changeLanguage(langCode, langName) {
    localStorage.setItem("userLanguage", langCode);
    localStorage.setItem("userLanguageName", langName);

    const langDisplay = document.getElementById('currentLang');
    if (langDisplay) {
        langDisplay.innerText = langName;
    }

    const selectedTexts = translations[langCode];
    if (selectedTexts) {
        document.querySelectorAll("[data-lang]").forEach(element => {
            const key = element.getAttribute("data-lang");
            if (selectedTexts[key]) {
                element.innerText = selectedTexts[key];
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const savedLang = localStorage.getItem("userLanguage") || "en";
    const savedName = localStorage.getItem("userLanguageName") || "English";
    changeLanguage(savedLang, savedName);
});
"""

# ፋይሉን በ static/js/ ማህደር ውስጥ ማስቀመጥ (ማህደሩ ከሌለ ይፈጠራል)
os.makedirs("users/static/js", exist_ok=True)
output_path = "users/static/js/translations.js"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"success! 🚀 ፋይልዎ በተሳካ ሁኔታ ተፈጥሯል: {output_path}")
