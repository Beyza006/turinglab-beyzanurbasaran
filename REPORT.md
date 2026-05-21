# TuringLab — Mini-Rapor

**Hesaplama Kuramı · Bilgisayar Mühendisliği · Final Ödevi**
Hazırlayan: Beyzanur Başaran · Selçuk Üniversitesi
Değerlendiren: Ahmet Erharman

---

## 1. Giriş

TuringLab, 4–22 Mayıs 2026 tarihleri arasında geliştirdiğim, deterministic single-tape Turing makinelerini YAML formatından okuyup çalıştıran bir Python kütüphanesidir. Proje üç zorunlu bölümden oluşur: (1) çekirdek motor, (2) dört farklı problem için tasarlanmış TM'ler, (3) bu raporun ve eşlik eden demo videosunun oluşturduğu sunum katmanı.

Ödevin asıl pedagojik kazanımı, soyut bir matematiksel modeli (`(Q, Σ, Γ, δ, q₀, F)` beşlisi) somut bir mühendislik artefaktına dönüştürmektir. Bu süreçte öğrendiğim en önemli şey, "çalışan bir TM" ile "Turing makinesi tasarımı becerisini gösteren bir TM" arasındaki farkı kendi deneyimimle fark etmek oldu. Bu raporun 3. bölümünde, 17 Mayıs'taki ilk kontrolden sonra iki makinemi neden tamamen yeniden tasarladığımı dürüstçe anlatacağım — bu, ödevin benim için en öğretici kısmıydı.

## 2. Mimari

### 2.1 Modüllerin Organizasyonu

Proje üç katmana ayrıldı: `turinglab/` (motor paketi), `machines/` (TM tanımları), `tests/` (pytest test paketi). Motor tek dosyada (`tm_engine.py`) toplandı çünkü kitapçık bunu zorunlu kıldı; ama dosyanın içinde sınıflar (`Tape`, `Transition`, `Configuration`, `RunResult`, `SingleTapeTM`) sorumluluklarına göre ayrı bloklar olarak duruyor. `turinglab/__init__.py` ise sadece public API'yi yeniden ihraç ediyor.

### 2.2 Şerit Temsili: Sparse Dictionary

Kitapçık, "şeridi `str` olarak tutmak" tuzağını s.9'da uyardı. Ben de iki seçenek arasında düşündüm: `list[str]` veya `dict[int, str]`. `list` ile sola taşmada negatif indis problemi başlardı (`tape[-1]` Python'da son eleman demek). `dict[int, str]` yaklaşımıyla:

- Yazılmamış hücreler otomatik olarak blank döner (`dict.get(pos, blank)`).
- Şerit hem sola hem sağa sonsuz genişler — negatif anahtarlar sorun değil.
- TM-1 (unary_to_binary) tasarımım bu özelliği aktif kullanıyor: binary sayacı negatif pozisyonlarda tutuyorum, böylece input ile çakışmadan MSB sola doğru rahatça genişliyor.

### 2.3 verbose=True Çıktısı

Verbose modu spec'in s.8'deki örneğine bire bir uyacak şekilde tasarladım. "Hareket" sütunu, o adımda **uygulanacak** harekettir; bu yüzden engine `_print_step` çağırılmadan önce bir sonraki transition'a peek eder. Kafa konumu `[sembol]` ile, şerit görünüm aralığı ise leftmost yazılı hücreden rightmost-yazılı+1'e (trailing blank için) kadar uzanır.

### 2.4 reason Alanı ve reject Genişletmesi

Kitapçık üç temel `reason` değeri tanımlar: `accept`, `no_transition`, `timeout`. Bunlara ek olarak motorum isteğe bağlı `reject_states` alanı destekliyor: makine bu durumlardan birine girerse `reason="reject"` döner. Bu, deterministik makinelerde "açık ret" tasarımına izin verir — örneğin `binary_compare` eşit sayılar için `q_reject` durumuna geçer ve cevap belirsiz kalmaz. README'de bu davranışı açıkça not ettim.

### 2.5 Hata Yönetimi

`from_yaml` üç farklı hata türünü ayırt eder: dosya yoksa `FileNotFoundError`, geçersiz YAML için ham `yaml.YAMLError`'u sarmalayan `ValueError`, eksik alan/yanlış hareket yönü/çakışan deterministik geçiş için açık mesajlı `ValueError`. Test paketinde her dört vaka için ayrı testler var.

## 3. Tasarlanan TM'ler

Bölüm 2 kapsamında dört Turing makinesi tasarladım. Tasarım sürecinin en öğretici kısmı, 17 Mayıs'ta TM-1 ve TM-2'nin "çalışan ama gerçek anlamda Turing makinesi olmayan" tasarımlar olduğunu fark etmek oldu.

**TM-1 — Unary to Binary (9 durum):** İlk denemem 87+ durumlu hard-coded bir lookup table'dı; sadece 0-16 aralığını destekliyordu. Bu tasarım test geçiriyordu ama TM tasarımı becerisini hiç göstermiyordu. Yeniden tasarladım: her unary `1` için negatif pozisyonlardaki binary sayacı +1 artıran genel bir algoritma. 9 durumla sınırsız uzunlukta girdiyi destekliyor. Kritik tasarım kararı: input `1`'lerini `I` ile değiştirip binary basamaklarıyla (`0`, `1`) karışmasını engellemek.

**TM-2 — Binary Compare (13 durum):** İlk denemem 289+ durumlu finite karar ağacıydı; sadece 4-bit canonical sayılar için çalışıyordu. Yeniden tasarladım: iki fazlı bir algoritma. Faz 1, x ile y'nin MSB bitlerini eşleştirir (`P=x'in 0'ı`, `Q=x'in 1'i`, `R=y'nin 0'ı`, `S=y'nin 1'i`) — value-preserving marker'lar Faz 2 için bit değerlerini saklar. Bir taraf önce biterse uzun olan kazanır. Faz 2, lengths-equal koşulunda MSB-first bit-bit karşılaştırma yapar. **Bu makine ödevin en zoru oldu** — çünkü tek şerit üzerinde paralel iki bilgiyi (uzunluk + bit değeri) aynı pozisyona kodlamayı öğretti.

**TM-3 — String Copy (8 durum):** `a/b` alfabesindeki bir dizgiyi `w#w` biçimine kopyalar. İşaretleyici sembol seçiminde dikkatli oldum: kitapçık `B'` öneriyordu ama bu blank `B` ile karışırdı, ben `C` kullandım — küçük ama tasarım kararıydı. Karmaşıklık O(n²), tek şeritli kopyalamanın doğal alt sınırı.

**TM-4 — Student Choice / 4'e Bölünebilirlik (9 durum):** Seçenek (a)'yı seçtim. Algoritma sade: durumlarda son iki biti hatırla, `B`'ye ulaşınca son iki bit `00` ise kabul. Sadece `{0,1,B}` alfabesi yeterli, hiç işaretleyiciye gerek yok.

## 4. Kavramsal Tartışma — Halting Problemi (~250 kelime)

> *Soru (a): Halting problemini TuringLab içinde "çözmek" mümkün mü? Neden değil?*

Hayır — ve bu "imkansızlık" rastgele bir mühendislik sınırı değil, hesaplama kuramının en temel sonuçlarından biridir. Halting problemi, herhangi bir TM tanımı `M` ve girdi `w` verildiğinde, `M(w)`'nin durup durmayacağını **her zaman** doğru söyleyen bir karar prosedürünün var olup olmadığını sorar. Alan Turing 1936'da bunun mümkün olmadığını gösterdi: böyle bir `H(M, w)` prosedürü olsaydı, kendine-referans (`H`'yi kendisi üzerinde çalıştırma) yoluyla mantıksal bir çelişki üretebilirdik.

TuringLab pratikte `max_steps` parametresi ile "zaman aşımı" kararı verir — verilen adım sınırında durmazsa `reason="timeout"` döner. Ama bu, halting'i çözmek değildir; sadece kararsızlığı bir parametreye taşımaktır. `max_steps=10` ile bitmeyen bir makine, `max_steps=10⁹` ile bitebilir; biz hangisinin doğru sınır olduğunu bilemeyiz. Daha akıllı bir analiz (örneğin static analysis ile döngü tespiti) bazı vakaları çözer ama **tüm** vakaları çözmez — çünkü tam çözüm olsaydı Turing'in kanıtıyla çelişirdi.

Bu sonuç bir motivasyon kaybı değil, aksine **hesaplamanın doğasını anlamak için en derin gözlemlerden biridir**. Programlama dillerinin tip sistemleri, derleyici optimizasyonları, formal verification araçları — hepsi halting kararsızlığının gölgesinde çalışır ve "her zaman çözüm" yerine "büyük bir altküme için karar" hedefler. TuringLab'in `max_steps` mekanizması da bu pratik yaklaşımın bir yansımasıdır: kanıtlanmış sınırın içinde kal, dışındaki vakaları timeout olarak işaretle.

## 5. Sınırlar ve İleri Çalışma

Projenin bilinçli olarak zorunlu kapsamla sınırlı tutulan kısımları var. Bonus seçenekler — multi-tape motor, non-deterministic TM (BFS ile), matplotlib görselleştirmesi — son hafta REPORT ve demo videosuna odaklanmak için bu sürümde yer almadı.

Bir hafta daha vaktim olsaydı şu sırayla ilerlerdim: (1) **Bonus A — Multi-tape TM**, çünkü tek-şeritli motorun küçük bir uzantısı ve TM-2'nin (binary compare) çok daha temiz bir versiyonunu yazma fırsatı verirdi — `x` ve `y`'yi iki ayrı şeride koyup paralel okumak ileri-geri tarama yükünü kaldırırdı. (2) **Bonus D — Görselleştirici** ile her adımın PNG karesini üretip GIF birleştirme; bu, design_notes'taki algoritma açıklamalarını canlı animasyonla destekleyebilirdi. (3) `binary_compare` için non-canonical girdileri (leading zero) tolere eden bir on-işleme fazı.

Daha küçük iyileştirmeler: `verbose` modunda renkli terminal çıktısı (`colorama`), YAML şema doğrulama için JSON Schema, `pyproject.toml` ile paket olarak kurulabilir hale getirme.

## 6. Kaynakça

1. Çetinkaya, A. (2026). *TuringLab Öğrenci El Kitabı*. Selçuk Üniversitesi Bilgisayar Mühendisliği. (Ödev kitapçığı — birincil referans)
2. Sipser, M. (2013). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning. Bölüm 3.1: Turing Makineleri ve Bölüm 4.2: Halting Problemi.
3. Turing, A. M. (1936). *On Computable Numbers, with an Application to the Entscheidungsproblem*. Proceedings of the London Mathematical Society. (Halting'in orijinal kanıtı)
4. Python Software Foundation. (2024). *Python 3.10 Documentation: dataclasses module*. https://docs.python.org/3/library/dataclasses.html
5. PyYAML Documentation. https://pyyaml.org/wiki/PyYAMLDocumentation
6. pytest Documentation. https://docs.pytest.org/

---

*Bu rapor, 22 Mayıs 2026 tarihli final teslim ile birlikte GitHub deposunda (`https://github.com/Beyza006/turinglab-beyzanurbasaran`) yer almaktadır.*
