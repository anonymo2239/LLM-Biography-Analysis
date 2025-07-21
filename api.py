# api.py
from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def root():
    return {"mesaj": "LLM Biyografi Analiz API'si çalışıyor."}

@app.get("/kisiler")
def get_all_people():
    with open("structured_bios.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/baglantilar")
def get_all_connections():
    with open("connections.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/baglantilar/{isim}")
def get_connections_for_name(isim: str):
    with open("connections.json", "r", encoding="utf-8") as f:
        all_conn = json.load(f)
    kisinin_baglantilari = [
        c for c in all_conn if isim.lower() in c["kişi_1"].lower() or isim.lower() in c["kişi_2"].lower()
    ]
    return kisinin_baglantilari
