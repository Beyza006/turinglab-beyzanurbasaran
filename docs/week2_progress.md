# Bölüm 2 İlerleme Notu

Bu not, Bölüm 2 kapsamında tasarlanan makinelerin hangi noktada olduğunu ve testlerle nasıl doğrulandığını özetler.

## Commit Akışı

- 13 Mayıs: `unary_to_binary` ve `binary_compare` için ilk YAML taslakları eklendi.
- 13 Mayıs: `string_copy` ve `student_choice` makineleri eklendi, `design_notes.md` başlatıldı.
- 14 Mayıs: `unary_to_binary` kapsamı 0-16 aralığına genişletildi.
- 14 Mayıs: `binary_compare` 0-15 arası canonical binary sayı çiftlerini kapsayacak şekilde güçlendirildi.
- 15 Mayıs: Makine test kapsamı genişletildi; desteklenen aralıklar ve edge-case davranışları otomatik test edildi.
- 16 Mayıs: README ve dokümantasyon Türkçe karakterler ve kullanım örnekleri açısından düzenlendi.
- 17 Mayıs: Bölüm 2 final kontrolü yapıldı; tasarım notları hocanın beklediği 5 soruya göre düzenlendi.

## Makine Durum Tablosu

| Makine | Dosya | Mevcut kapsam | Test durumu |
| --- | --- | --- | --- |
| Unary to Binary | `machines/unary_to_binary.yaml` | 0-16 unary uzunluğu | 17 desteklenen girdi otomatik test ediliyor |
| Binary Compare | `machines/binary_compare.yaml` | 0-15 arası canonical `x#y` çiftleri | 16x16 = 256 çift otomatik test ediliyor |
| String Copy | `machines/string_copy.yaml` | `a`/`b` alfabeli dizgiler | Boş girdi, tek karakter, karışık dizgiler ve bilinmeyen sembol testi var |
| Student Choice | `machines/student_choice.yaml` | Binary 4'e bölünebilirlik | Kabul, ret, boş girdi ve leading-zero testleri var |

## Doğrulama Komutu

Tüm motor ve makine testleri şu komutla çalıştırılır:

```bash
pytest tests -q
```

17 Mayıs final kontrolünde beklenen sonuç:

```text
344 passed
```

## Bölüm 2 Kapanış Durumu

PDF'te istenen dört makine, test dosyası ve tasarım notları repoda yer alıyor. Test kapsamı 344 testten oluşuyor ve final kontrolde tüm testler geçiyor. Bu nedenle Bölüm 2, Pazar günü itibarıyla kapatılmış kabul edilebilir.

## Kalan İyileştirme Fikirleri

- `unary_to_binary` için finite aralıktan genel binary sayaç algoritmasına geçmek.
- `binary_compare` için finite karar ağacı yerine işaretleyicili genel uzunluk/bit karşılaştırma algoritması kurmak.
- Bölüm 3'e geçmeden önce demo videosu ve mini-rapor için senaryo hazırlamak.
