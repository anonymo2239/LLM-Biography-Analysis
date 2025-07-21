from extract import extract_entities
from find_connections import find_connections
from langchain_google_genai import ChatGoogleGenerativeAI
import json

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

# Biyografi dosyasından örnek veri al
with open("biographies.json", "r", encoding="utf-8") as f:
    biographies = json.load(f)

entity_data_list = []
for person in biographies:
    extracted = extract_entities(person["bio"], model)
    entity_data = json.loads(extracted)
    entity_data_list.append(entity_data)

# Bağlantıları bul
connections = find_connections(entity_data_list)

# Bağlantıları yazdır
for conn in connections:
    print(f'{conn["person1"]} ↔ {conn["person2"]}: Ortak Noktalar → {conn["shared"]}')
