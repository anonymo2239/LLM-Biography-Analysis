# match.py
import json

def find_connections(data):
    results = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            p1 = data[i]
            p2 = data[j]
            ortaklar = {}
            for key in ["ilkokul", "lise", "üniversite", "yaşadığı_şehir", "çalıştığı_kurumlar"]:
                if p1.get(key) and p2.get(key) and p1[key] == p2[key]:
                    ortaklar[key] = p1[key]
            if ortaklar:
                results.append({
                    "kişi_1": p1.get("ad", "Bilinmiyor"),
                    "kişi_2": p2.get("ad", "Bilinmiyor"),
                    "ortak_noktalar": ortaklar
                })
    return results

def run():
    with open("structured_bios.json", "r", encoding="utf-8") as f:
        bios = json.load(f)
    conn = find_connections(bios)
    with open("connections.json", "w", encoding="utf-8") as f:
        json.dump(conn, f, ensure_ascii=False, indent=2)
    print("Ortak noktalar bulundu.")

if __name__ == "__main__":
    run()
