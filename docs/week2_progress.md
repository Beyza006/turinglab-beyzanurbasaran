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
| Unary to Binary | `machines/unary_to_binary.yaml` | Sınırsız unary uzunluğu (20 Mayıs yeniden tasarımı) | 0-32 aralığı + n=40/64/100/127 büyük girdiler test ediliyor |
| Binary Compare | `machines/binary_compare.yaml` | Sınırsız bit sayısı canonical `x#y` (20 Mayıs yeniden tasarımı) | 16x16=256 çift + 17 5-11 bit çifti test ediliyor |
| String Copy | `machines/string_copy.yaml` | `a`/`b` alfabeli dizgiler | Boş girdi, tek karakter, karışık dizgiler ve bilinmeyen sembol testi var |
| Student Choice | `machines/student_choice.yaml` | Binary 4'e bölünebilirlik | Kabul, ret, boş girdi ve leading-zero testleri var |

## Doğrulama Komutu

Tüm motor ve makine testleri şu komutla çalıştırılır:

```bash
pytest tests -q
```

20 Mayıs yeniden tasarımından sonra test sonucu:

```text
381 passed
```

## 20 Mayıs Yeniden Tasarım

17 Mayıs'taki ilk final kontrolün ardından, design_notes.md'yi tekrar gözden geçirdiğimde TM-1 ve TM-2 tasarımlarının "çalışan ama yeterince genel olmayan" finite lookup tabloları olduğunu fark ettim:

- **TM-1 eski hali**: 87+ durum, sadece 0-16 unary uzunluğu.
- **TM-2 eski hali**: 289+ durum, sadece 4-bit canonical sayılar.

Her ikisini de 20 Mayıs günü yeniden tasarladım:

- **TM-1 yeni hali**: 9 durum, sınırsız uzunluk. Her unary `1` için negatif pozisyonlardaki binary sayacı +1.
- **TM-2 yeni hali**: 13 durum + kabul/ret, sınırsız uzunluk. İki fazlı: uzunluk eşleme + MSB-first bit-bit.

Test kapsamı 344'ten 381'e çıktı; bu artış sayesinde n=100 unary girdiyi veya 10-bit binary çiftlerini de doğrulayabiliyorum.

## Bölüm 2 Kapanış Durumu

PDF'te istenen dört makine, test dosyası ve tasarım notları repoda yer alıyor. 20 Mayıs yeniden tasarımı sonrası tüm 381 test geçiyor. Bu nedenle Bölüm 2, dosya yapısı ve algoritmik genellik açısından kapatılmış kabul edilebilir.

## Kalan İyileştirme Fikirleri

- Bölüm 3 için demo videosu ve mini-rapor (`REPORT.md`) hazırlamak.
- (Opsiyonel) Bonus A (Multi-tape) veya Bonus D (Visualizer) için zaman ayırmak.
