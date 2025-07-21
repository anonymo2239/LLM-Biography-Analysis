# extract_new.py - Yeni Google Gemini 2.5 Flash API ile
import os
import json
import time
from dotenv import load_dotenv
from google import genai

# .env dosyasını yükle
load_dotenv()

"""DATASET_PATH = "C:\\Users\\emirhan.gul\\Desktop\\LLM_proje\\LLM-Biography-Analysis\\dataset2"
OUTPUT_JSON = "C:\\Users\\emirhan.gul\\Desktop\\LLM_proje\\LLM-Biography-Analysis\\structured_bios_dataset2.json"
"""

"""DATASET_PATH = "C:\\Users\\emirhan.gul\\Desktop\\LLM_proje\\LLM-Biography-Analysis\\dataset"
OUTPUT_JSON = "C:\\Users\\emirhan.gul\\Desktop\\LLM_proje\\LLM-Biography-Analysis\\structured_bios_dataset.json"
"""

DATASET_PATH = "C:\\Users\\emirhan.gul\\Desktop\\LLM_proje\\LLM-Biography-Analysis\\dataset3"
OUTPUT_JSON = "C:\\Users\\emirhan.gul\\Desktop\\LLM_proje\\LLM-Biography-Analysis\\structured_bios_dataset3.json"

# Google Gemini client'ı başlat (GEMINI_API_KEY ortam değişkenini otomatik alır)
client = genai.Client()

def extract_structured_data(md_text):
    prompt = f"""
    Aşağıdaki biyografiden şu bilgileri JSON formatında çıkar. 

    KURALLARI:
    - Bilgi yoksa null değer kullan (tırnaksız)
    - Tarihler: "GG.MM.YYYY" formatında yaz (örn: "15.09.1988")
    - Şehir isimleri: Sadece ana şehir adı (örn: "İzmir", "Bursa") 
    - Hobiler: Kısa ve sade ifadeler
    - Eş/çocuk yoksa null kullan
    - Boş listeler için boş array [] kullan

    {{
        "ad": "string",
        "doğum_yeri": "string", 
        "doğum_tarihi": "string",
        "ilkokul": "string",
        "lise": "string", 
        "üniversite": "string",
        "bölüm": "string",
        "yüksek_lisans": "string",
        "doktora": "string",
        "çalıştığı_kurumlar": ["liste"],
        "kurduğu_girişim_ve_dernekler": ["liste"],
        "yaşadığı_şehir": "string",
        "hobiler": ["liste"],
        "eş": "string",
        "çocuklar": ["liste"],
        "akademik_yayınlar": ["liste"]
    }}

    Biyografi:
    {md_text}
    
    SADECE temiz JSON döndür, başka açıklama yapma.
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        json_text = response.text.strip()
        
        # JSON'u temizle (markdown kod bloklarını kaldır)
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()
        elif "```" in json_text:
            json_text = json_text.split("```")[1].strip()
            
        return json_text
    except Exception as e:
        print(f"LLM hatası: {e}")
        return None

def run():
    all_data = []
    files = [f for f in os.listdir(DATASET_PATH) if f.endswith(".md")]
    
    # Tüm dosyaları işle (quota'ya dikkat ederek)
    test_files = files  # Tüm dosyaları işle
    print(f"Toplam {len(test_files)} dosya işlenecek...")
    
    for i, file in enumerate(test_files, 1):
        try:
            print(f"İşleniyor ({i}/{len(test_files)}): {file}")
            
            with open(os.path.join(DATASET_PATH, file), "r", encoding="utf-8") as f:
                text = f.read()
            
            json_str = extract_structured_data(text)
            
            if json_str:
                try:
                    parsed = json.loads(json_str)
                    parsed["dosya_adı"] = file  # Dosya adını da ekleyelim
                    all_data.append(parsed)
                    print(f"✅ Başarılı: {parsed.get('ad', 'Bilinmeyen')}")
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parse hatası: {e}")
                    print(f"Raw output: {json_str[:200]}...")
            else:
                print(f"❌ Başarısız: {file}")
            
            # Rate limiting - API quota'sını aşmamak için bekleme
            if i < len(test_files):  # Son dosya değilse bekle
                print("⏳ 3 saniye bekleniyor...")
                time.sleep(3)
                
        except Exception as e:
            print(f"❌ Hata ({file}): {e}")
    
    # Sonuçları kaydet
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n🎉 İşlem tamamlandı! {len(all_data)} dosya başarıyla işlendi.")
    print(f"📁 Sonuçlar: {OUTPUT_JSON}")

if __name__ == "__main__":
    run()
