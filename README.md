# TuringLab

**Hesaplama Kuramı Final Ödevi**  
Selçuk Üniversitesi - Bilgisayar Mühendisliği  
Hazırlayan: Beyzanur Başaran  
Değerlendirme: Ahmet Erharman

---

## Proje Hakkında

TuringLab, YAML formatında tanımlanmış deterministik tek şeritli Turing makinelerini yükleyip çalıştıran bir Python kütüphanesidir. Proje üç zorunlu bölümden oluşur:

| Bölüm | Konu | Puan |
| --- | --- | --- |
| Bölüm 1 | TM Motoru (`tm_engine.py`) | 50 |
| Bölüm 2 | 4 TM Tasarımı | 35 |
| Bölüm 3 | Demo Video + Mini-Rapor | 15 |

---

## Kurulum

```bash
git clone https://github.com/Beyza006/turinglab-beyzanurbasaran.git
cd turinglab-beyzanurbasaran
pip install -r requirements.txt
```

---

## Temel Kullanım

```python
from turinglab import SingleTapeTM

makine = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
sonuc = makine.run(input_string="1011", max_steps=1000, verbose=False)

print(sonuc.accepted)              # True
print(sonuc.final_tape.strip("B")) # 1100
print(sonuc.steps)                 # adim sayisi
```

Verbose modda her adım şerit ve kafa konumuyla birlikte yazdırılır:

```python
makine = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
sonuc = makine.run("1011", max_steps=1000, verbose=True)
```

---

## Bölüm 2 Makineleri

Bölüm 2 kapsamında dört Turing makinesi `machines/` klasörüne eklendi:

| Makine | Dosya | Davranış |
| --- | --- | --- |
| Unary to Binary | `machines/unary_to_binary.yaml` | Herhangi bir uzunluktaki unary girdiyi binary'e çevirir (9 durum, sınırsız uzunluk). |
| Binary Compare | `machines/binary_compare.yaml` | Canonical binary `x#y` çiftlerinde `x > y` ise kabul eder; bit sayısı serbest (13 durum, iki fazlı). |
| String Copy | `machines/string_copy.yaml` | `a`/`b` dizgisini `w#w` formatında kopyalar. |
| Student Choice | `machines/student_choice.yaml` | Binary girdinin 4'e bölünüp bölünmediğini test eder. |

### Örnek 1: String Copy

```python
from turinglab import SingleTapeTM

makine = SingleTapeTM.from_yaml("machines/string_copy.yaml")
sonuc = makine.run("abba", max_steps=2000)

print(sonuc.accepted)              # True
print(sonuc.final_tape.strip("B")) # abba#abba
```

### Örnek 2: Binary Compare

```python
from turinglab import SingleTapeTM

makine = SingleTapeTM.from_yaml("machines/binary_compare.yaml")
sonuc = makine.run("1100#1011", max_steps=2000)

print(sonuc.accepted) # True, cunku 12 > 11

# Sinirsiz uzunluk de destekleniyor:
sonuc2 = makine.run("10101010#10101001", max_steps=50000)
print(sonuc2.accepted) # True, cunku 170 > 169
```

### Örnek 3: 4'e Bölünebilirlik

```python
from turinglab import SingleTapeTM

makine = SingleTapeTM.from_yaml("machines/student_choice.yaml")
sonuc = makine.run("10100", max_steps=2000)

print(sonuc.accepted) # True, cunku 20 sayisi 4'e bolunur
```

---

## Testleri Çalıştırma

Tüm testler:

```bash
pytest tests -q
```

Sadece Bölüm 2 testleri:

```bash
pytest tests/test_machines.py -q
```

20 Mayıs yeniden tasarım sonrası test sonucu:

```text
381 passed
```

TM-1 ve TM-2'nin 20 Mayıs'taki yeniden tasarım hikayesi için bkz. [`docs/design_notes.md`](docs/design_notes.md) sondaki "Yeniden Tasarım Notu" bölümü.

---

## Repo Yapısı

```text
turinglab/
|-- README.md
|-- REPORT.md                  # Bolum 3'te eklenecek
|-- requirements.txt
|-- .gitignore
|-- turinglab/
|   |-- __init__.py
|   `-- tm_engine.py            # Bolum 1: TM motoru
|-- machines/
|   |-- binary_increment.yaml
|   |-- unary_increment.yaml
|   |-- even_a.yaml
|   |-- unary_to_binary.yaml
|   |-- binary_compare.yaml
|   |-- string_copy.yaml
|   `-- student_choice.yaml
|-- tests/
|   |-- test_tm_engine.py
|   `-- test_machines.py
`-- docs/
    |-- design_notes.md
    `-- week2_progress.md
```

---

## Tasarım Kararları

### Şerit Temsili

Şerit `dict[int, str]` yani sparse dictionary olarak tutulur. Bu yaklaşım yazılmamış hücreleri otomatik olarak blank sembol kabul eder ve şeridin iki yönde de genişlemesine izin verir.

### Sola Taşma

Motor negatif indisleri destekler. Bu nedenle kafa sola hareket ettiğinde Python listesindeki `-1` gibi yanlış bir indeksleme problemi oluşmaz. Aşırı uzun veya hatalı çalışan makineler için `max_steps` sınırı kullanılır.

---

## Demo Video

Bölüm 3'te eklenecek.

---

## Lisans

Akademik ödev; yalnızca eğitim amaçlıdır.
