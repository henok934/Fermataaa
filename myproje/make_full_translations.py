import os
from bs4 import BeautifulSoup

# የቴምፕሌት ማህደሮችህ ያሉበት መንገድ (ለምሳሌ users/templates/users)
templates_dir = "users/templates/users"
all_texts = set()

print("🔍 የሁሉም HTML ፋይሎች 텍ስቶች በሰንሰለት በመቃኘት ላይ...")

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
                        
                    # የዩአይ 텍ስቶች የሚገኙባቸው ታጎች
                    tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'span', 'label', 'button', 'small', 'li'])
                    for tag in tags:
                        text = tag.get_text(strip=True)
                        # ባዶ ያልሆኑ እና ጂንካ / ቴምፕሌት ታጎች የሌሉባቸውን እንይዛለን
                        if text and len(text) < 120 and not text.startswith("{%") and not text.startswith("{{"):
                            all_texts.add(text)
            except Exception as e:
                print(f"ማስታወሻ ({file_path}): ማንበብ አልተቻለም - {e}")

print(f"✨ በአጠቃላይ {len(all_texts)} ልዩ 텍ስቶች ተገኝተዋል!")

# translations.js ፋይልን በኮድ ማዋቀር
js_content = """// በራስ-ሰር ከሁሉም የ HTML ፋይሎች የተፈጠረ የቋንቋ መዝገብ
const translations = {
    en: {
"""

# እንግሊዝኛ 텍ስቶቹን በቁልፍ (Key) እና በቫልዩ (Value) መልክ እናስገባለን
key_map = {}
for i, text in enumerate(sorted(all_texts)):
    safe_key = "txt_" + "".join(e for e in text if e.isalnum())[:15] + f"_{i}"
    key_map[text] = safe_key
    # አርኪ (Quote) ምልክቶችን እንዳያበላሹ እናስተካክላለን
    escaped_text = text.replace('"', '\\"')
    js_content += f'        "{safe_key}": "{escaped_text}",\n'

js_content += """    },
    am: {
        // የኢትዮጵያ አማርኛ ትርጉሞች እዚህ ይገባሉ (ለጊዜው በእንግሊዝኛ ይቆያሉ, እየገቡ ሲሄዱ መቀየር ይቻላል)
"""
for text, safe_key in key_map.items():
    escaped_text = text.replace('"', '\\"')
    js_content += f'        "{safe_key}": "{escaped_text}",\n'

js_content += """    },
    om: {
        // የኦሮምኛ ትርጉሞች እዚህ ይገባሉ
"""
for text, safe_key in key_map.items():
    escaped_text = text.replace('"', '\\"')
    js_content += f'        "{safe_key}": "{escaped_text}",\n'

js_content += """    }
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

# ፋይሉን በቀጥታ ወደ static/js/ ማህደር መጻፍ
output_path = "users/static/js/translations.js"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"success! 🚀 የሁሉም ገጾች 텍ስቶች ተጠቃለዋል: {output_path}")
