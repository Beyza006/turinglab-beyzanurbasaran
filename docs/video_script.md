# Demo Video Senaryosu — 2-3 Dakika

**Format:** MP4 (H.264), min 1280x720, mikrofonlu Türkçe ses
**Süre Hedefi:** 2 dakika 30 saniye (esnek 2-3 dk)
**Kayıt Aracı:** OBS Studio veya ShareX
**İpucu:** Editör/terminal yazı tipini en az 16pt yap, sessiz odada kayıt al, ilk kayıt asla en iyi değildir — 2-3 deneme yap

---

## [00:00 - 00:25] Açılış (25 sn)

> "Merhaba, ben Beyzanur Başaran. Hesaplama Kuramı dersi final ödevim TuringLab'i sunuyorum. TuringLab, YAML formatında tanımlanmış deterministic single-tape Turing makinelerini çalıştıran bir Python kütüphanesi. Bu kısa videoda motoru çalışırken göstereceğim, tasarladığım 4 makineden ikisini açıklayacağım ve en kritik tasarım kararımı paylaşacağım."

**Ekranda:** Repo'nun GitHub sayfası veya proje klasörü açık. README.md'nin başlığı görünür.

---

## [00:25 - 01:30] Canlı Demo (65 sn)

**Adım 1 — YAML göster (15 sn):**
- Editörde `machines/binary_increment.yaml` aç.
- States, transitions kısmını göster.
> "Bu, ikili sayıyı bir artıran TM'nin YAML tanımı. 3 durum: q0 sağa tara, q_carry carry uygula, q_accept kabul. 6 geçiş kuralı."

**Adım 2 — Verbose çalıştır (25 sn):**
- Terminal aç, çalıştır:
  ```python
  python -c "from turinglab import SingleTapeTM; SingleTapeTM.from_yaml('machines/binary_increment.yaml').run('1011', verbose=True)"
  ```
- Çıktıyı göster.
> "Her adımda durum, şerit, kafa konumu ve uygulanacak hareket görünüyor. Spec ile birebir uyumlu. 1011 girdisi 8 adımda 1100'e dönüştü."

**Adım 3 — TM-2 binary_compare örneği (25 sn):**
- Terminal:
  ```python
  python -c "from turinglab import SingleTapeTM; tm = SingleTapeTM.from_yaml('machines/binary_compare.yaml'); print(tm.run('10101010#10101001').accepted)"
  ```
- Cevap True (170 > 169).
> "Binary compare 8-bit sayıları da çözüyor. 170 ile 169 karşılaştırması — kabul."

---

## [01:30 - 02:15] En Kritik Tasarım Kararı (45 sn)

> "En önemli kararım: TM-1 unary_to_binary makinesini 17 Mayıs'tan sonra tamamen yeniden tasarlamak.
> 
> İlk denemem 87 durumlu hard-coded bir lookup table'dı — sadece 0-16 aralığındaki unary girdileri çalışıyordu. Test geçiriyordu ama bu bir Turing makinesi tasarımı değildi, sınırlı bir if-else ağacıydı.
> 
> Yeniden tasarladım: sadece 9 durumla, her unary 1 için negatif pozisyonlardaki binary sayacı bir artıran genel algoritma. Sınırsız uzunluk destekleniyor — n=100 unary girdiyi de doğru çevirebiliyor.
> 
> Burada öğrendiğim ders: tek şeritte sembol seçimi kritik. Input '1'lerini önce 'I' işaretleyicisine çevirdim ki binary basamaklarıyla karışmasın. Bu küçük tasarım kararı, algoritmayı doğru çalıştıran şeydi. Şerit sembolleri sadece veri değil, bilgi taşıyan birer etiket."

**Ekranda:** `design_notes.md`'nin TM-1 bölümünün "5. Hata Ayıklama Hikayesi" kısmı.

---

## [02:15 - 02:45] Kapanış (30 sn)

> "Test paketinde 381 test geçiyor: hem algoritma doğruluğunu hem de sınırsız girdiyi kanıtlıyor.
> 
> Bir hafta daha vaktim olsa Bonus A — multi-tape TM'yi yapardım; özellikle binary compare'i iki şeritte yazmak çok daha temiz olurdu.
> 
> Bu projeden en büyük kazancım: soyut bir matematiksel modeli somut bir mühendislik artefaktına çevirme deneyimi. 'Çalışan bir TM' ile 'TM tasarımı becerisini gösteren bir TM' arasındaki farkı kendi parmaklarımla öğrendim.
> 
> Dinlediğiniz için teşekkürler."

**Ekranda:** GitHub repo sayfası tekrar, README'deki demo video bağlantısı.

---

## Kayıt Öncesi Kontrol Listesi

- [ ] Terminal yazı tipi en az 16pt
- [ ] Editör yazı tipi en az 14pt
- [ ] Mikrofon test: arka plan gürültüsü minimal mi?
- [ ] OBS sahnesi: ekran + ses kaydedildi mi?
- [ ] Kayıt çözünürlüğü: en az 1280x720
- [ ] Pencere düzeni: terminal sağda, editör solda (split)
- [ ] Komutlar önceden yazılmış, copy-paste hazır
- [ ] 2 deneme kaydı yap, en iyisini seç

## Kayıt Sonrası

- [ ] MP4 olarak dışa aktar (H.264 codec)
- [ ] YouTube'a unlisted yükle
- [ ] README.md'deki "Demo Video" bölümüne linki ekle
- [ ] Linki test et (incognito modda çalışıyor mu?)
- [ ] `git add README.md && git commit -m "demo video baglantisi eklendi"`
- [ ] `git tag final && git push --tags`
