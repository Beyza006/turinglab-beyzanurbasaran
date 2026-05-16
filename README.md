# TuringLab

**Hesaplama Kuram? Final ?devi**  
Sel?uk ?niversitesi ? Bilgisayar M?hendisli?i  
Haz?rlayan: Beyzanur Ba?aran  
De?erlendirme: Ahmet Erharman

---

## Proje Hakk?nda

TuringLab, YAML format?nda tan?mlanm?? deterministik tek ?eritli Turing makinelerini y?kleyip ?al??t?ran bir Python k?t?phanesidir. Proje ?? zorunlu b?l?mden olu?ur:

| B?l?m | Konu | Puan |
| --- | --- | --- |
| B?l?m 1 | TM Motoru (`tm_engine.py`) | 50 |
| B?l?m 2 | 4 TM Tasar?m? | 35 |
| B?l?m 3 | Demo Video + Mini-Rapor | 15 |

---

## Kurulum

```bash
git clone https://github.com/Beyza006/turinglab-beyzanurbasaran.git
cd turinglab-beyzanurbasaran
pip install -r requirements.txt
```

---

## Temel Kullan?m

```python
from turinglab import SingleTapeTM

makine = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
sonuc = makine.run(input_string="1011", max_steps=1000, verbose=False)

print(sonuc.accepted)              # True
print(sonuc.final_tape.strip("B")) # 1100
print(sonuc.steps)                 # ad?m say?s?
```

Verbose modda her ad?m ?erit ve kafa konumuyla birlikte yazd?r?l?r:

```python
makine = SingleTapeTM.from_yaml("machines/binary_increment.yaml")
sonuc = makine.run("1011", max_steps=1000, verbose=True)
```

---

## B?l?m 2 Makineleri

B?l?m 2 kapsam?nda d?rt Turing makinesi `machines/` klas?r?ne eklendi:

| Makine | Dosya | Davran?? |
| --- | --- | --- |
| Unary to Binary | `machines/unary_to_binary.yaml` | 0-16 aras? unary girdiyi binary ??kt?ya ?evirir. |
| Binary Compare | `machines/binary_compare.yaml` | 0-15 aras? canonical binary `x#y` ?iftlerinde `x > y` ise kabul eder. |
| String Copy | `machines/string_copy.yaml` | `a`/`b` dizgisini `w#w` format?nda kopyalar. |
| Student Choice | `machines/student_choice.yaml` | Binary girdinin 4'e b?l?n?p b?l?nmedi?ini test eder. |

### ?rnek 1: String Copy

```python
from turinglab import SingleTapeTM

makine = SingleTapeTM.from_yaml("machines/string_copy.yaml")
sonuc = makine.run("abba", max_steps=2000)

print(sonuc.accepted)              # True
print(sonuc.final_tape.strip("B")) # abba#abba
```

### ?rnek 2: Binary Compare

```python
from turinglab import SingleTapeTM

makine = SingleTapeTM.from_yaml("machines/binary_compare.yaml")
sonuc = makine.run("1100#1011", max_steps=2000)

print(sonuc.accepted) # True, ??nk? 12 > 11
```

### ?rnek 3: 4'e B?l?nebilirlik

```python
from turinglab import SingleTapeTM

makine = SingleTapeTM.from_yaml("machines/student_choice.yaml")
sonuc = makine.run("10100", max_steps=2000)

print(sonuc.accepted) # True, ??nk? 20 say?s? 4'e b?l?n?r
```

---

## Testleri ?al??t?rma

T?m testler:

```bash
pytest tests -q
```

Sadece B?l?m 2 testleri:

```bash
pytest tests/test_machines.py -q
```

15 May?s itibar?yla test sonucu:

```text
344 passed
```

---

## Repo Yap?s?

```text
turinglab/
??? README.md
??? REPORT.md                  # B?l?m 3'te eklenecek
??? requirements.txt
??? .gitignore
??? turinglab/
?   ??? __init__.py
?   ??? tm_engine.py            # B?l?m 1: TM motoru
??? machines/
?   ??? binary_increment.yaml
?   ??? unary_increment.yaml
?   ??? even_a.yaml
?   ??? unary_to_binary.yaml
?   ??? binary_compare.yaml
?   ??? string_copy.yaml
?   ??? student_choice.yaml
??? tests/
?   ??? test_tm_engine.py
?   ??? test_machines.py
??? docs/
    ??? design_notes.md
    ??? week2_progress.md
```

---

## Tasar?m Kararlar?

### ?erit Temsili

?erit `dict[int, str]` yani sparse dictionary olarak tutulur. Bu yakla??m yaz?lmam?? h?creleri otomatik olarak blank sembol kabul eder ve ?eridin iki y?nde de geni?lemesine izin verir.

### Sola Ta?ma

Motor negatif indisleri destekler. Bu nedenle kafa sola hareket etti?inde Python listesindeki `-1` gibi yanl?? bir indeksleme problemi olu?maz. A??r? uzun veya hatal? ?al??an makineler i?in `max_steps` s?n?r? kullan?l?r.

---

## Demo Video

B?l?m 3'te eklenecek.

---

## Lisans

Akademik ?dev; yaln?zca e?itim ama?l?d?r.
