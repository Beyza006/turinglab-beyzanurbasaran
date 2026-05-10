# TuringLab

**Hesaplama Kuramı Final Ödevi**  
Selçuk Üniversitesi · Bilgisayar Mühendisliği  
Hazırlayan: Beyzanur Başaran  
Değerlendirme: Ahmet Erharman

---

## Proje Hakkında

TuringLab, YAML formatında tanımlanmış deterministik tek-şeritli Turing makinelerini
yükleyip çalıştıran bir Python kütüphanesidir. Proje üç zorunlu bölümden oluşur:

| Bölüm | Konu | Puan |
|-------|------|------|
| Bölüm 1 | TM Motoru (`tm_engine.py`) | 50 |
| Bölüm 2 | 4 TM Tasarımı | 35 |
| Bölüm 3 | Demo Video + Mini-Rapor | 15 |

---

## Kurulum

```bash
# Repo'yu klonla
git clone https://github.com/KULLANICI_ADI/turinglab-ADSOYADINIZ.git
cd turinglab-ADSOYADINIZ

# Bağımlılıkları yükle
pip install -r requirements.txt
```

---

## Kullanım

```python
from turinglab import SingleTapeTM, RunResult

# Makineyi YAML'dan yükle
tm = SingleTapeTM.from_yaml("machines/binary_increment.yaml")

# Çalıştır
result: RunResult = tm.run(
    input_string="1011",
    max_steps=1000,
    verbose=False
)

# Sonucu incele
print(result.accepted)       # True
print(result.final_tape.strip("B"))  # "1100"
print(result.steps)          # kaç adım sürdü
print(len(result.history))   # steps + 1 konfigürasyon

# Tek bir adımı incele
config = result.history[5]
print(config.state, config.tape, config.head_position)
```

### Verbose Mod

```python
result = tm.run("1011", verbose=True)
```

Örnek çıktı:

```
Adım   0 | Durum: q0           | Şerit: [1]011B | Hareket: —
Adım   1 | Durum: q0           | Şerit: 1[0]11B | Hareket: R
Adım   2 | Durum: q0           | Şerit: 10[1]1B | Hareket: R
...
```

---

## Testleri Çalıştırma

```bash
pytest tests/ -v
```

---

## Repo Yapısı

```
turinglab/
├── README.md
├── REPORT.md              # (Bölüm 3 — eklenecek)
├── requirements.txt
├── .gitignore
├── turinglab/
│   ├── __init__.py
│   ├── tm_engine.py       # Bölüm 1: TM motoru
│   ├── multi_tape.py      # (Bonus A — opsiyonel)
│   ├── ntm.py             # (Bonus B — opsiyonel)
│   └── visualizer.py      # (Bonus D — opsiyonel)
├── machines/
│   ├── binary_increment.yaml
│   ├── unary_increment.yaml
│   ├── even_a.yaml
│   ├── unary_to_binary.yaml    # (Bölüm 2 — eklenecek)
│   ├── binary_compare.yaml     # (Bölüm 2 — eklenecek)
│   ├── string_copy.yaml        # (Bölüm 2 — eklenecek)
│   └── student_choice.yaml     # (Bölüm 2 — eklenecek)
├── tests/
│   ├── test_tm_engine.py
│   └── test_machines.py        # (Bölüm 2 — eklenecek)
└── docs/
    ├── design_notes.md         # (Bölüm 2 — eklenecek)
    └── images/
```

---

## Tasarım Kararları

### Şerit Temsili

Şerit `dict[int, str]` (sparse dictionary) olarak tutulur.
Bu yaklaşımın avantajları:
- Sonsuz genişleyebilir (pozitif ve negatif indisler)
- Yazılmamış hücreler otomatik olarak blank döner
- Python string'lerinin immutability sorununu tamamen çözer

### Sola Taşma (head_position < 0)

Motor `dict[int, str]` (sparse) kullandığından kafa negatif indislere gidebilir — şerit
sola da sonsuz genişleyebilir. Bu, teorik TM tanımıyla tam uyumludur. Makine tasarımları
gereksiz sola hareketten kaçınmalıdır; aşırı sola gidişi `max_steps` limiti önler.

---

## Demo Video

*(Bölüm 3'te eklenecek)*

---

## Lisans

Akademik ödev — yalnızca eğitim amaçlıdır.
