# Bölüm 2 Tasarım Notları

Bu dosya, Bölüm 2 kapsamında tasarlanan dört Turing makinesinin tasarım kararlarını açıklar. Her makine için strateji, durum sayısı, şerit alfabesi, karmaşıklık ve hata ayıklama notları ayrı ayrı verilmiştir.

---

## TM-1: Unary to Binary

### 1. Strateji

Bu makine unary girdiyi önce uzunluk olarak sayar. Desteklenen aralıkta kaç tane `1` olduğunu durumlar üzerinden takip eder, sonra şeridin soluna bu sayının binary karşılığını yazar. Son olarak eski unary sembollerinden arta kalan hücreleri `B` ile temizler. Örneğin `111` girdisi 3 sayısını temsil eder ve sonuçta şeritte `11` kalır.

Bu sürüm 0-16 aralığını kapsar. Daha genel bir sürümde her işlenmemiş unary `1` için ayrı bir binary sayaç artırma algoritması kurulabilir. Bu yaklaşım daha az sınırlı olurdu, fakat Bölüm 2 ilerlemesinde önce dönüşüm mantığını test edilebilir hale getirmek hedeflendi.

### 2. Durum Sayısı

Durum sayısı görece yüksektir; çünkü makine sayma, başa dönme, binary sonucu yazma ve eski sembolleri temizleme fazlarına ayrılmıştır. Her desteklenen sayı için yazılacak binary çıktıyı temsil eden ayrı yazma durumları vardır. Daha genel sayaçlı tasarımda sayı başına ayrı durum açmak yerine aynı artırma döng@uşu@ tekrar kullanılabilirdi.

### 3. Şerit Alfabesi

Şerit alfabesi `0`, `1`, `B` ve `X` sembollerinden oluşur. `0` ve `1` binary çıktı için, `B` blank sembol için kullanılır. `X` bu sürümde aktif olarak kullanılmasa da genel sürüme geçildiğinde işlenmiş unary sembollerini işaretlemek için doğal bir yardımcı semboldür.

### 4. Karmaşıklık

Desteklenen aralıkta makine önce girdiyi sağa doğru tarar, sonra sola dönüp sonucu yazar ve kalan hücreleri temizler. Bu nedenle pratik çalışma maliyeti girdi uzunluğu ile doğrusal ilerler. Genel binary sayaç algoritmasına geçilirse her unary sembol için binary sayaç güncelleneceğinden maliyet daha yüksek olabilir.

### 5. Hata Ayıklama Hikayesi

En zor hata, binary sonuç yazıldıktan sonra eski unary sembollerinin şeritte kalmasıydı. Örneğin `11111` girdisinde `101` yazılsa bile sağ tarafta eski `1` sembolleri kalınca final çıktı kirleniyordu. Bunu çözmek için sonuç yazımından sonra çalışan ayrı bir `q_clear` fazı eklendi.

---

## TM-2: Binary Compare

### 1. Strateji

Bu makine `x#y` biçimindeki iki canonical binary sayıyı karşılaştırır. Mevcut sürüm 0-15 arası tüm canonical sayı çiftlerini kapsayan genişletilmiş bir karar ağacı olarak tasarlandı. Makine girdiyi soldan sağa okur; tam bir tanımlı örüntünün sonuna geldiğinde `x > y` ise kabul, aksi durumda ret durumuna geçer.

### 2. Durum Sayısı

Durum sayısı, 0-15 arası tüm `x#y` çiftlerinin prefix ağacından gelir. Ortak başlang@içlar paylaşıldığı için her girdi için tamamen ayrı yol açılmadı. Yine de finite karar ağacı yaklaşımı genel algoritmaya göre daha fazla durum üretir.

### 3. Şerit Alfabesi

Şerit alfabesi `0`, `1`, `#` ve `B` sembollerinden oluşur. Makine şeridi değiştirmez; yalnızca okuma yaparak karar verir. Bu nedenle ek işaretleyici sembole ihtiyaç duyulmadı.

### 4. Karmaşıklık

Makine her tanımlı girdiyi soldan sağa bir kez okur. Bu yüzden desteklenen girdiler için çalışma süresi `O(n)`dir. Genel işaretleyicili algoritmada tek şerit üzerinde ileri-geri tarama gerekeceği için maliyet daha yüksek olabilir.

### 5. Hata Ayıklama Hikayesi

İlk taslakta bazı ret durumları `no_transition` ile bitiyordu. Bu, testlerde sonucu belirsiz gösteriyordu. Özellikle eşit sayılar için açık bir `q_reject` durumuna gitmek daha doğru oldu. Böylece `101#101` gibi girdiler gerçekten reddediliyor ve `reason == "reject"` olarak görülebiliyor.

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

En dikkat isteyen kenar durum, tek sembollü `0` girdisini kabul ederken boş girdiyi reddetmekti. Eğer başlang@iç durumunda `B` doğrudan kabul edilseydi boş girdi de kabul edilmiş olurdu. Bu nedenle `q_start` durumunda `B` okununca makine `q_reject` durumuna gider.

---

## Final Kontrol Notu - 17 Mayıs

17 Mayıs Pazar günü Bölüm 2 için final kontrol yapıldı. Dört makine dosyası, `tests/test_machines.py`, `docs/design_notes.md` ve `docs/week2_progress.md` dosyaları yerinde. Test kapsamı genişletilmiş durumda ve tüm testler geçiyor. Bu noktada Bölüm 2, dosya yapısı ve dokümantasyon açısından kapatılabilir durumdadır.
