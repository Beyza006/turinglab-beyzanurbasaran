# Bölüm 2 Tasarım Notları

Bu dosya, Bölüm 2 kapsamında tasarlanan dört Turing makinesinin tasarım kararlarını açıklar. Her makine için strateji, durum sayısı, şerit alfabesi, karmaşıklık ve hata ayıklama notları ayrı ayrı verilmiştir.

---

## TM-1: Unary to Binary

### 1. Strateji

Bu makine "her unary `1` için binary sayacı 1 artır" prensibini uygular. Adımlar:

1. **Dönüşüm fazı**: Tüm input `1` sembolleri `I` ile değiştirilir, sona `#` yazılır. Bu, input işaretleyicileri ile binary basamaklarının aynı `1` sembolünü paylaşmasını engeller — TM tek şeritte pozisyon bilgisi tutamadığı için sembol ayrımı şarttır.
2. **Başlangıç**: Sola doğru yürünerek pozisyon -1'e başlangıç binary değeri olan `0` yazılır. Binary sayısı negatif pozisyonlarda, MSB sola doğru genişleyecek şekilde tutulur.
3. **İterasyon** (her unary `1` için): `#`'ten sola doğru en sağdaki işaretsiz `I` bulunur ve `X` yapılır; sonra LSB'ye (pozisyon -1) varılır ve binary sayaç +1 ile artırılır. Carry sola yayılır; gerekirse yeni MSB pozisyonu açılır.
4. **Temizlik**: Tüm `I` bittiğinde, kalan `X` ve `#` semboller `B`'ye çevrilir; geriye sadece binary kalır.

`final_tape.strip("B")` çağrısı doğru sonucu verir çünkü binary negatif pozisyonlarda, pozitif pozisyonlarda ise sadece blank kalır.

### 2. Durum Sayısı

9 durum: `q_start`, `q_convert`, `q_init_binary`, `q_find_hash`, `q_seek_I`, `q_back_to_binary`, `q_carry`, `q_cleanup`, `q_accept`. Her durum algoritmanın bir fazına karşılık geliyor; bu okunabilirliği ve verbose çıktı izlenebilirliğini artırıyor. `q_back_to_binary` ile `q_carry` birleştirilebilirdi (her ikisi de carry mantığı yapıyor) ama LSB ile diğer basamaklar arasında transit-okuma farkı olduğundan ayrı tutmak daha temiz çıktı.

Önceki tasarımım her n için ayrı `q_count_n`, `q_back_n`, `q_w_n_k` durumları üretiyordu (87+ durum, sadece n ≤ 16). Yeni tasarım girdi uzunluğundan bağımsız sabit durum sayısı kullanıyor.

### 3. Şerit Alfabesi

Şerit alfabesi `0`, `1`, `B`, `I`, `X`, `#`. Kritik tasarım kararı: input `1`'lerini `I`'ye çevirmek. Eğer input ve binary ikisi de `1` kullansaydı, makine sembol bazlı hangi bölgede olduğunu ayırt edemezdi. `I/X` (input markerları) ile `0/1` (binary basamakları) arasında kesin ayrım olunca, transition tablosu sembol bakarak doğru kararı veriyor.

`#` input bölgesinin sağ sınırını, `B` ise sol sınırını (binary'den önceki pozisyonlar) belirler. `X` "işlenmiş input" rolünü üstleniyor; `I` ile aynı şerit pozisyonunu paylaşmıyor (sıralı olarak değişiyor).

### 4. Karmaşıklık

Girdi uzunluğu *n* iken: her iterasyon `#` ↔ LSB arası tarama gerektirir, bu mesafe O(n + log n). Toplam *n* iterasyon olduğu için **Θ(n²)** adım. Test sonuçları bunu doğruluyor: n=50 ~5500 adım, n=100 ~21000 adım (kabaca dört kat → n²).

### 5. Hata Ayıklama Hikayesi

İlk taslakta binary'yi `#`'in **sağına** koymuştum (sağ tarafta MSB-first, growing rightward). Carry işlemi şöyle gidiyordu: LSB'den sola doğru taşıma, ama MSB extension'a geldiğinde `#`'i bir pozisyon sağa kaydırmam gerekiyordu — bu da hemen sağındaki marker'ları silme sorunu yarattı. Test girdisinde `11111` (n=5) çalıştırınca beklenen `101` yerine `10#1` gibi karışık bir sonuç alıyordum.

**Çözüm**: Binary'yi negatif pozisyonlara taşıdım. Tape sınıfımız `dict[int, str]` tabanlı olduğu için negatif indeksler doğal şekilde destekleniyor ve MSB sola doğru rahatça genişliyor. Tek dezavantaj: artık `strip("B")` ile temiz çıktı almak için temizlik fazı (`q_cleanup`) gerekli oldu — `X`'leri ve `#`'i `B`'ye çevirmek. Bu da algoritmaya tek bir terminal faz olarak eklendi.

---

## TM-2: Binary Compare

### 1. Strateji

Bu makine `x#y` biçimindeki iki canonical binary sayıyı karşılaştırır. Tek şeritte bunu yapmak iki temel zorluğu birden çözmeyi gerektiriyor: (a) uzunluk karşılaştırması (uzun olan, canonical varsayım altında büyüktür) ve (b) eşit uzunluklarda MSB-first bit-bit karşılaştırma. İki fazlı yaklaşım kullandım:

**Faz 1 — Uzunluk eşleme**: x'in MSB'sini ve y'nin MSB'sini sırayla eşleştir; her bit işaretlenir. x'in bitleri `P` (was 0) veya `Q` (was 1) ile, y'nin bitleri `R` (was 0) veya `S` (was 1) ile işaretlenir. Bu marker'lar **bit değerini saklar** — Faz 2 için gerekli. Bir taraf işaretsiz bit kalmaz olursa: diğer tarafta hala `0`/`1` varsa, o uzun taraf canonical olarak büyüktür → karar verilir. Hem x hem y aynı anda biterse → Faz 2'ye geçilir.

**Faz 2 — MSB-first bit-bit karşılaştırma**: Uzunluklar eşitse, soldan sağa `P/Q`-`R/S` çiftleri karşılaştırılır. Her çift karşılaştırılırken `X`'e çevriliyor ("tüketildi"). İlk farklılaşan bitte: `1 vs 0` → kabul; `0 vs 1` → ret. Tüm bitler eşitse → ret (eşit sayılar).

### 2. Durum Sayısı

13 durum + kabul/ret = 15 toplam:

- Faz 1: `q_p1_seek_x`, `q_p1_seek_hash`, `q_p1_seek_y`, `q_p1_x_done` (4)
- Dönüş: `q_return_to_p1`, `q_return_to_p2` (2)
- Faz 2: `q_p2_seek_x`, `q_p2_x_was_0`, `q_p2_x_was_1`, `q_p2_seek_y_for_0`, `q_p2_seek_y_for_1` (5)
- Terminal: `q_accept`, `q_reject` (2)

Önceki tasarımım 289+ durum kullanıyordu — her olası 4-bit `x#y` çifti için bir karar ağacı dalı. Yeni tasarım bit sayısından bağımsız: 1024-bit'lik girdi de aynı 13 durumla çalışır.

`q_p2_x_was_0` ve `q_p2_x_was_1` birleştirilebilirdi (sadece x'in bitini bir "memory" markerda taşımak), ama Faz 2 mantığını parametrize etmek transition sayısını ikiye katlardı. Mevcut ayrım okumayı kolaylaştırıyor.

### 3. Şerit Alfabesi

Şerit alfabesi `0`, `1`, `#`, `B`, `P`, `Q`, `R`, `S`, `X`. Marker tasarımı önemli:

- **P=0, Q=1 (x için)**, **R=0, S=1 (y için)**: Marker değer-koruyucu. Faz 1'de işaretlenen bit, Faz 2'de değeri kaybetmeden geri okunuyor.
- **x ve y için farklı marker setleri**: P/Q ile R/S ayrımı sayesinde `#` pozisyonunu sürekli aramaya gerek kalmadan hangi bölgede olduğumuzu yerel sembolden anlayabiliyoruz.
- **X (Faz 2 tüketilmiş)**: Faz 1 marker'larından ayrı; "bu bit artık tüketildi, atla" anlamına geliyor.

### 4. Karmaşıklık

`|x| = a`, `|y| = b`, `n = max(a,b)`:

- Faz 1: Her iterasyonda en sola dön + x'i bul + y'yi bul → O(n) per iterasyon × n iterasyon = O(n²).
- Faz 2: Benzer şekilde O(n²).
- Toplam **Θ(n²)**.

Test verisi: 4-bit çiftler ~50-150 adım, 8-bit ~300-600, 10-bit ~800-1500 adım — n² büyüme doğrulandı.

### 5. Hata Ayıklama Hikayesi

İlk denemem single-pass MSB-first algoritmasıydı: x ve y'nin sol bitlerinden başla, eşit değilse hemen kararı ver. Bu **eşit uzunluklarda** doğru çalışıyordu ama farklı uzunluklarda hatalı sonuçlar üretiyordu. Örneğin `1#100` girdisi (1 vs 4): algoritma x[0]='1' ve y[0]='1'i karşılaştırıyor, "eşit" diye geçiyor; ikinci iterasyonda x bitti, ama y'nin kalan bitleri var. Algoritma bu "uzunluk farkı" durumunu doğru yorumlayamıyordu.

**Çözüm**: İki fazlı yaklaşım. Faz 1 sadece uzunluk karşılaştırması (eşleştirerek), Faz 2 lengths-equal koşullu MSB-first bit-bit karşılaştırma. Marker'lara bit değerini saklatmak (P=0, Q=1, R=0, S=1) sayesinde Faz 2'de bilgi kaybı olmadan aynı bitleri tekrar okuyabiliyoruz. Bu çözüm bana **tek şerit üzerinde paralel bilgi tutmanın** (uzunluk + bit değeri aynı pozisyonda) Turing makinesi tasarımının temel becerilerinden biri olduğunu gösterdi.

---

## TM-3: String Copy

### 1. Strateji

Bu makine `a` ve `b` alfabeli bir dizgiyi `w#w` biçiminde kopyalar. İlk olarak girdinin sonuna `#` ayracı yerleştirilir. Sonra soldan sağa ilk işaretlenmemiş sembol bulunur. `a` sembolü `A`, `b` sembolü `C` ile işaretlenir; makine şeridin sonuna gider ve aynı sembolü kopyalar. Tüm kaynak semboller işaretlenince makine restore fazına geçer ve `A/C` işaretlerini tekrar `a/b` yapar.

### 2. Durum Sayısı

Makine 8 ana faz kullanır: sona gitme, başa dönme, kaynak sembol bulma, `a` kopyalama, `b` kopyalama, kopyadan sonra geri dönme, restore etme ve kabul. Bu ayrım, algoritmanın okunmasını ve test edilmesini kolaylaştırdı.

### 3. Şerit Alfabesi

Şerit alfabesi `a`, `b`, `B`, `#`, `A` ve `C` sembollerinden oluşur. `#` kaynak ve kopya bölgesini ayırır. `A` ve `C`, kaynak tarafta daha önce işlenmiş karakterleri gösterir. `C` sembolü, `B` blank sembolüyle karışmaması için `b` işaretleyicisi olarak seçildi.

### 4. Karmaşıklık

Her karakter için makine kaynak bölgeden kopya bölgesinin sonuna kadar gidip tekrar başa döner. Bu yüzden toplam hareket sayısı yaklaşık `O(n^2)`dir. Tek şeritli TM için bu beklenen bir maliyettir.

### 5. Hata Ayıklama Hikayesi

En önemli hata, kopyalanan `a/b` sembollerinin tekrar kaynak sembol gibi işlenmesiydi. Makine kopya alanına geçtikten sonra yeniden kopyalama yapmaya çalışıyordu. Bunu `q_find` durumunun `#` sembolünde durmasını sağlayarak çözdüm.

---

## TM-4: Student Choice - Binary 4'e Bölünebilirlik

### 1. Strateji

Öğrenci seçimi olarak binary girdinin 4'e bölünüp bölünmediğini test eden makine seçildi. Binary sayılarda `0` sayısı veya son iki biti `00` olan sayılar 4'e bölünür. Bu nedenle makine tüm girdiyi soldan sağa okur ve yalnızca son bir veya iki bit bilgisini durumlarda saklar.

### 2. Durum Sayısı

Durum sayısı azdır. `q_last0` ve `q_last1` tek sembollü girdileri temsil eder. `q_pair00`, `q_pair01`, `q_pair10`, `q_pair11` ise en son görülen iki biti saklar. Girdi bittiğinde makine bu duruma göre kabul veya ret verir.

### 3. Şerit Alfabesi

Şerit alfabesi yalnızca `0`, `1` ve `B` sembollerinden oluşur. Bu makine bir karar problemi çözdüğü için şeridi değiştirmeye veya yardımcı işaretleyici kullanmaya gerek yoktur.

### 4. Karmaşıklık

Makine girdiyi bir kez soldan sağa okur. Bu nedenle çalışma süresi `O(n)`dir. Kullanılan bilgi yalnızca son bitler olduğu için durum belleği sabittir.

### 5. Hata Ayıklama Hikayesi

En dikkat isteyen kenar durum, tek sembollü `0` girdisini kabul ederken boş girdiyi reddetmekti. Eğer başlangıç durumunda `B` doğrudan kabul edilseydi boş girdi de kabul edilmiş olurdu. Bu nedenle `q_start` durumunda `B` okununca makine `q_reject` durumuna gider.

---

## Final Kontrol Notu - 17 Mayıs

17 Mayıs Pazar günü Bölüm 2 için ilk final kontrol yapıldı. Dört makine dosyası, `tests/test_machines.py`, `docs/design_notes.md` ve `docs/week2_progress.md` dosyaları yerinde. Test kapsamı genişletilmiş durumda ve tüm testler geçiyor. Bu noktada Bölüm 2'yi kapatılabilir olarak işaretlemiştim.

## Yeniden Tasarım Notu - 20 Mayıs

17 Mayıs'taki final kontrolün ardından, 3. haftaya başlarken design_notes.md'yi tekrar okuduğumda iki tasarım kararının ödevin asıl beklentisiyle örtüşmediğini fark ettim:

- **TM-1 (unary_to_binary)** 87+ durumlu hard-coded lookup table idi; sadece 0-16 unary uzunluğunu destekliyordu. n=17 için `no_transition` hatası veriyordu.
- **TM-2 (binary_compare)** 289+ durumlu finite karar ağacı idi; sadece 4-bitlik canonical sayıları destekliyordu. 5-bit girdi `no_transition` veriyordu.

İkisi de "test girdilerinde çalışan ama Turing makinesi olarak yeterince genel olmayan" tasarımlardı. Rubrikteki "Durum sayısı: Daha az durum mümkün müydü?" ve "Algoritmadan δ kurallarına çevirme" beklentilerine bu tasarımlar yeterli cevap vermiyordu.

20 Mayıs'ta her ikisini de yeniden tasarladım:

- **TM-1**: 9 durum, sınırsız uzunluk. Her unary `1` için negatif pozisyonlardaki binary sayacı +1. (87 → 9 durum)
- **TM-2**: 13 durum + kabul/ret, sınırsız uzunluk. İki fazlı: uzunluk eşleme + MSB-first bit-bit. (289 → 13 durum)

Bu yeniden tasarım sürecinde öğrendiğim en önemli şey: bir TM'nin "çalışması" yetmiyor; algoritmanın **genel** olması, sınırlı sayıda durum kullanması ve sembollere anlam yüklemeyi öğrenmesi gerekiyor. Hard-coded yaklaşım test geçirir ama TM tasarımı becerisini göstermez. Yeni tasarımlar da mevcut tüm test girdilerini geçiyor ve buna ek olarak n=100 unary girdiyi veya 10-bit binary çiftleri sorunsuz işliyor.
