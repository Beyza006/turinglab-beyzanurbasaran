# Bolum 2 Ilerleme Notu

Bu not, Bolum 2 kapsaminda tasarlanan makinelerin hangi noktada oldugunu ve testlerle nasil dogrulandigini ozetler.

## Commit Akisi

- 13 Mayis: `unary_to_binary` ve `binary_compare` icin ilk YAML taslaklari eklendi.
- 13 Mayis: `string_copy` ve `student_choice` makineleri eklendi, `design_notes.md` baslatildi.
- 14 Mayis: `unary_to_binary` kapsami 0-16 araligina genisletildi.
- 14 Mayis: `binary_compare` 0-15 arasi canonical binary sayi ciftlerini kapsayacak sekilde guclendirildi.
- 15 Mayis: Makine test kapsami genisletildi; desteklenen araliklar ve edge-case davranislari otomatik test edildi.

## Makine Durum Tablosu

| Makine | Dosya | Mevcut kapsam | Test durumu |
| --- | --- | --- | --- |
| Unary to Binary | `machines/unary_to_binary.yaml` | 0-16 unary uzunlugu | 17 desteklenen girdi otomatik test ediliyor |
| Binary Compare | `machines/binary_compare.yaml` | 0-15 arasi canonical `x#y` ciftleri | 16x16 = 256 cift otomatik test ediliyor |
| String Copy | `machines/string_copy.yaml` | `a`/`b` alfabeli dizgiler | Bos girdi, tek karakter, karisik dizgiler ve bilinmeyen sembol testi var |
| Student Choice | `machines/student_choice.yaml` | Binary 4'e bolunebilirlik | Kabul, ret, bos girdi ve leading-zero testleri var |

## Dogrulama Komutu

Tum motor ve makine testleri su komutla calistirilir:

```bash
pytest tests -q
```

15 Mayis itibariyla beklenen sonuc:

```text
344 passed
```

## Kalan Iyilestirme Fikirleri

- `unary_to_binary` icin finite araliktan genel binary sayac algoritmasina gecmek.
- `binary_compare` icin finite karar agaci yerine isaretleyicili genel uzunluk/bit karsilastirma algoritmasi kurmak.
- `design_notes.md` icindeki hata ayiklama hikayelerini daha dogal ve kisisel hale getirmek.
- Bolum 3'e gecmeden once README'deki ornekleri terminal ciktilariyla desteklemek.
