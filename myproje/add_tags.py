import os
from bs4 import BeautifulSoup

file_path = "users/templates/users/index.html"

print("🔄 የ index.html ፋይልን በማስተካከል ላይ...")

with open(file_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# ሊለወጡ የሚገባቸውን 텍ስቶች እና ቁልፎቻቸውን (Keys) እንገልፃለን
replacements = {
    "About Us": "aboutUs",
    "My Ticket": "myTicket",
    "Departure City": "depCityLabel",
    "Destination City": "desCityLabel",
    "SEARCH TRAVEL": "searchTravelBtn",
    "The Pride of Ethiopian Transit": "heroTitle",
    "Fast, Reliable & Modern Cross-Country Digital Network": "heroSubtitle",
    "Fast & Secure Ticketing": "heroBadge",
    "Seamless Travel Across Ethiopia": "seamlessTitle",
    "Connecting regional cities and major public transport terminals with modern digital ticketing solutions.": "seamlessDesc"
}

# 텍ስቶቹን እየፈለግን data-lang መለያ እንጨምራቸዋለን
for tag in soup.find_all(['a', 'label', 'button', 'h1', 'p', 'span']):
    text = tag.get_text(strip=True)
    if text in replacements:
        tag['data-lang'] = replacements[text]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("success! 🚀 index.html ፋይልዎ በተሳካ ሁኔታ ተስተካክሏል!")
