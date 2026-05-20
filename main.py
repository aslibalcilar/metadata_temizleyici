import os
import re
import hashlib
import json

if not os.path.exists("output"):
    os.mkdir("output")

def hash_hesapla(dosya_yolu):
    with open(dosya_yolu, "rb") as dosya:
        veri = dosya.read()
        return hashlib.sha256(veri).hexdigest()

def temizle(dosya_yolu):
    if not os.path.exists(dosya_yolu):
        print("Dosya bulunamadi")
        return

    eski_hash = hash_hesapla(dosya_yolu)

    with open(dosya_yolu, "r", encoding="utf-8") as dosya:
        icerik = dosya.read()

    desenler = [
        r"author\s*:.*",
        r"date\s*:.*",
        r"location\s*:.*",
        r"email\s*:.*"
    ]

    silinen_sayi = 0

    for desen in desenler:
        yeni_icerik = re.sub(desen, "", icerik, flags=re.IGNORECASE)
        if yeni_icerik != icerik:
            silinen_sayi += 1
        icerik = yeni_icerik

    dosya_adi = os.path.basename(dosya_yolu)
    yeni_yol = "output/temizlenmis_" + dosya_adi

    with open(yeni_yol, "w", encoding="utf-8") as dosya:
        dosya.write(icerik)

    yeni_hash = hash_hesapla(yeni_yol)

    rapor = {
        "orijinal_dosya": dosya_yolu,
        "temiz_dosya": yeni_yol,
        "eski_hash": eski_hash,
        "yeni_hash": yeni_hash,
        "silinen_metadata_sayisi": silinen_sayi
    }

    with open("output/rapor.json", "w", encoding="utf-8") as dosya:
        json.dump(rapor, dosya, indent=4, ensure_ascii=False)

    print("Temizleme tamamlandi")
    print("Yeni dosya:", yeni_yol)
    print("Silinen metadata sayisi:", silinen_sayi)

print("1 - Metadata temizle")
print("2 - Cikis")

secim = input("Seciminiz: ")

if secim == "1":
    dosya = input("Dosya yolunu gir: ")
    temizle(dosya)
else:
    print("Program kapandi")