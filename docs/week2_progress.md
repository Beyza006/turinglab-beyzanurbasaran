# B?l?m 2 ?lerleme Notu

Bu not, B?l?m 2 kapsam?nda tasarlanan makinelerin hangi noktada oldu?unu ve testlerle nas?l do?ruland???n? ?zetler.

## Commit Ak???

- 13 May?s: `unary_to_binary` ve `binary_compare` i?in ilk YAML taslaklar? eklendi.
- 13 May?s: `string_copy` ve `student_choice` makineleri eklendi, `design_notes.md` ba?lat?ld?.
- 14 May?s: `unary_to_binary` kapsam? 0-16 aral???na geni?letildi.
- 14 May?s: `binary_compare` 0-15 aras? canonical binary say? ?iftlerini kapsayacak ?ekilde g??lendirildi.
- 15 May?s: Makine test kapsam? geni?letildi; desteklenen aral?klar ve edge-case davran??lar? otomatik test edildi.
- 16 May?s: README ve dok?mantasyon T?rk?e karakterler ve kullan?m ?rnekleri a??s?ndan d?zenlendi.

## Makine Durum Tablosu

| Makine | Dosya | Mevcut kapsam | Test durumu |
| --- | --- | --- | --- |
| Unary to Binary | `machines/unary_to_binary.yaml` | 0-16 unary uzunlu?u | 17 desteklenen girdi otomatik test ediliyor |
| Binary Compare | `machines/binary_compare.yaml` | 0-15 aras? canonical `x#y` ?iftleri | 16x16 = 256 ?ift otomatik test ediliyor |
| String Copy | `machines/string_copy.yaml` | `a`/`b` alfabeli dizgiler | Bo? girdi, tek karakter, kar???k dizgiler ve bilinmeyen sembol testi var |
| Student Choice | `machines/student_choice.yaml` | Binary 4'e b?l?nebilirlik | Kabul, ret, bo? girdi ve leading-zero testleri var |

## Do?rulama Komutu

T?m motor ve makine testleri ?u komutla ?al??t?r?l?r:

```bash
pytest tests -q
```

15 May?s itibar?yla beklenen sonu?:

```text
344 passed
```

## Kalan ?yile?tirme Fikirleri

- `unary_to_binary` i?in finite aral?ktan genel binary saya? algoritmas?na ge?mek.
- `binary_compare` i?in finite karar a?ac? yerine i?aretleyicili genel uzunluk/bit kar??la?t?rma algoritmas? kurmak.
- B?l?m 3'e ge?meden ?nce demo videosu ve mini-rapor i?in senaryo haz?rlamak.
