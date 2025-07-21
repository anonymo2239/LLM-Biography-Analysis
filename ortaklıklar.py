import json
from collections import defaultdict

with open("structured_bios_dataset.json", "r", encoding="utf-8") as f:
    bios = json.load(f)

# Boş/eksik alanlar normalize edilir
def clean(x):
    if x in [None, "null", "", []]:
        return None
    return x

for bio in bios:
    for k in bio:
        bio[k] = clean(bio[k])


baglantilar = defaultdict(lambda: {"alanlar": set(), "degerler": defaultdict(set)})

def ekle_gruplama(alan_adi):
    lookup = defaultdict(list)
    for kisi in bios:
        deger = kisi.get(alan_adi)
        if deger:
            # Eğer liste ise, her eleman için ayrı ayrı işle
            if isinstance(deger, list):
                for item in deger:
                    if item:  # Boş string kontrolü
                        lookup[item.lower()].append(kisi["ad"])
            else:
                lookup[deger.lower()].append(kisi["ad"])

    # Aynı değeri paylaşanları eşleştir
    for deger, grup in lookup.items():
        for a in grup:
            for b in grup:
                if a != b:
                    baglantilar[(a, b)]["alanlar"].add(alan_adi)
                    baglantilar[(a, b)]["degerler"][alan_adi].add(deger)

for alan in ["ilkokul", "lise", "üniversite", "çalıştığı_kurumlar", "yaşadığı_şehir"]:
    ekle_gruplama(alan)

print(f"Toplam bağlantı sayısı: {len(baglantilar)}")
print("\nEn çok ortak noktası olan ilk 10 kişi çifti:")

# Ortak alan sayısına göre sırala
sorted_baglantilar = sorted(baglantilar.items(), key=lambda x: len(x[1]["alanlar"]), reverse=True)

for i, ((a, b), veri) in enumerate(sorted_baglantilar[:10]):
    print(f"{i+1}. {a} <-> {b}")
    print(f"   Ortak alanlar ({len(veri['alanlar'])}):")
    for alan in veri["alanlar"]:
        degerler = ", ".join(veri["degerler"][alan])
        print(f"     - {alan}: {degerler}")
    print()
