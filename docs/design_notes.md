# B?l?m 2 Tasar?m Notlar?

Bu dosya, B?l?m 2 kapsam?nda tasarlanan d?rt Turing makinesinin tasar?m kararlar?n? a??klar. Her makine i?in strateji, durum say?s?, ?erit alfabesi, karma??kl?k ve hata ay?klama notlar? ayr? ayr? verilmi?tir.

---

## TM-1: Unary to Binary

### 1. Strateji

Bu makine unary girdiyi ?nce uzunluk olarak sayar. Desteklenen aral?kta ka? tane `1` oldu?unu durumlar ?zerinden takip eder, sonra ?eridin soluna bu say?n?n binary kar??l???n? yazar. Son olarak eski unary sembollerinden arta kalan h?creleri `B` ile temizler. ?rne?in `111` girdisi 3 say?s?n? temsil eder ve sonu?ta ?eritte `11` kal?r.

Bu s?r?m 0-16 aral???n? kapsar. Daha genel bir s?r?mde her i?lenmemi? unary `1` i?in ayr? bir binary saya? art?rma algoritmas? kurulabilir. Bu yakla??m daha az s?n?rl? olurdu, fakat B?l?m 2 ilerlemesinde ?nce d?n???m mant???n? test edilebilir hale getirmek hedeflendi.

### 2. Durum Say?s?

Durum say?s? g?rece y?ksektir; ??nk? makine sayma, ba?a d?nme, binary sonucu yazma ve eski sembolleri temizleme fazlar?na ayr?lm??t?r. Her desteklenen say? i?in yaz?lacak binary ??kt?y? temsil eden ayr? yazma durumlar? vard?r. Daha genel saya?l? tasar?mda say? ba??na ayr? durum a?mak yerine ayn? art?rma d?ng?s? tekrar kullan?labilirdi.

### 3. ?erit Alfabesi

?erit alfabesi `0`, `1`, `B` ve `X` sembollerinden olu?ur. `0` ve `1` binary ??kt? i?in, `B` blank sembol i?in kullan?l?r. `X` bu s?r?mde aktif olarak kullan?lmasa da genel s?r?me ge?ildi?inde i?lenmi? unary sembollerini i?aretlemek i?in do?al bir yard?mc? sembold?r.

### 4. Karma??kl?k

Desteklenen aral?kta makine ?nce girdiyi sa?a do?ru tarar, sonra sola d?n?p sonucu yazar ve kalan h?creleri temizler. Bu nedenle pratik ?al??ma maliyeti girdi uzunlu?u ile do?rusal ilerler. Genel binary saya? algoritmas?na ge?ilirse her unary sembol i?in binary saya? g?ncellenece?inden maliyet daha y?ksek, yakla??k `O(n log n)` veya uygulama ayr?nt?s?na g?re `O(n^2)` olabilir.

### 5. Hata Ay?klama Hikayesi

En zor hata, binary sonu? yaz?ld?ktan sonra eski unary sembollerinin ?eritte kalmas?yd?. ?rne?in `11111` girdisinde `101` yaz?lsa bile sa? tarafta eski `1` sembolleri kal?nca final ??kt? kirleniyordu. Bunu ??zmek i?in sonu? yaz?m?ndan sonra ?al??an ayr? bir `q_clear` faz? eklendi.

---

## TM-2: Binary Compare

### 1. Strateji

Bu makine `x#y` bi?imindeki iki canonical binary say?y? kar??la?t?r?r. Mevcut s?r?m 0-15 aras? t?m canonical say? ?iftlerini kapsayan geni?letilmi? bir karar a?ac? olarak tasarland?. Makine girdiyi soldan sa?a okur; tam bir tan?ml? ?r?nt?n?n sonuna geldi?inde `x > y` ise kabul, aksi durumda ret durumuna ge?er.

Bu ??z?m, kar??la?t?rma problemini test edilebilir ve deterministik hale getirir. Daha genel s?r?mde ?nce say? uzunluklar? kar??la?t?r?labilir, uzunluklar e?itse soldan sa?a ilk farkl? bit bulunarak karar verilebilir.

### 2. Durum Say?s?

Durum say?s?, 0-15 aras? t?m `x#y` ?iftlerinin prefix a?ac?ndan gelir. Ortak ba?lang??lar payla??ld??? i?in her girdi i?in tamamen ayr? yol a??lmad?. Yine de finite karar a?ac? yakla??m? genel algoritmaya g?re daha fazla durum ?retir.

### 3. ?erit Alfabesi

?erit alfabesi `0`, `1`, `#` ve `B` sembollerinden olu?ur. Makine ?eridi de?i?tirmez; yaln?zca okuma yaparak karar verir. Bu nedenle ek i?aretleyici sembole ihtiya? duyulmad?.

### 4. Karma??kl?k

Makine her tan?ml? girdiyi soldan sa?a bir kez okur. Bu y?zden desteklenen girdiler i?in ?al??ma s?resi `O(n)`dir. Genel i?aretleyicili algoritmada tek ?erit ?zerinde ileri-geri tarama gerekece?i i?in maliyet daha y?ksek olabilir.

### 5. Hata Ay?klama Hikayesi

?lk taslakta baz? ret durumlar? `no_transition` ile bitiyordu. Bu, testlerde sonucu belirsiz g?steriyordu. ?zellikle e?it say?lar i?in a??k bir `q_reject` durumuna gitmek daha do?ru oldu. B?ylece `101#101` gibi girdiler ger?ekten reddediliyor ve `reason == "reject"` olarak g?r?lebiliyor.

---

## TM-3: String Copy

### 1. Strateji

Bu makine `a` ve `b` alfabeli bir dizgiyi `w#w` bi?iminde kopyalar. ?lk olarak girdinin sonuna `#` ay?rac? yerle?tirilir. Sonra soldan sa?a ilk i?aretlenmemi? sembol bulunur. `a` sembol? `A`, `b` sembol? `C` ile i?aretlenir; makine ?eridin sonuna gider ve ayn? sembol? kopyalar. T?m kaynak semboller i?aretlenince makine restore faz?na ge?er ve `A/C` i?aretlerini tekrar `a/b` yapar.

### 2. Durum Say?s?

Makine 8 ana faz kullan?r: sona gitme, ba?a d?nme, kaynak sembol bulma, `a` kopyalama, `b` kopyalama, kopyadan sonra geri d?nme, restore etme ve kabul. Bu ayr?m, algoritman?n okunmas?n? ve test edilmesini kolayla?t?rd?.

### 3. ?erit Alfabesi

?erit alfabesi `a`, `b`, `B`, `#`, `A` ve `C` sembollerinden olu?ur. `#` kaynak ve kopya b?lgesini ay?r?r. `A` ve `C`, kaynak tarafta daha ?nce i?lenmi? karakterleri g?sterir. `C` sembol?, `B` blank sembol?yle kar??mamas? i?in `b` i?aretleyicisi olarak se?ildi.

### 4. Karma??kl?k

Her karakter i?in makine kaynak b?lgeden kopya b?lgesinin sonuna kadar gidip tekrar ba?a d?ner. Bu y?zden toplam hareket say?s? yakla??k `O(n^2)`dir. Tek ?eritli TM i?in bu beklenen bir maliyettir; ?ok ?eritli bir tasar?mda kopyalama daha verimli yap?labilirdi.

### 5. Hata Ay?klama Hikayesi

En ?nemli hata, kopyalanan `a/b` sembollerinin tekrar kaynak sembol gibi i?lenmesiydi. Makine kopya alan?na ge?tikten sonra yeniden kopyalama yapmaya ?al???yordu. Bunu `q_find` durumunun `#` sembol?nde durmas?n? sa?layarak ??zd?m. B?ylece yaln?zca `#` ?ncesindeki kaynak b?lge taran?yor.

---

## TM-4: Student Choice - Binary 4'e B?l?nebilirlik

### 1. Strateji

??renci se?imi olarak binary girdinin 4'e b?l?n?p b?l?nmedi?ini test eden makine se?ildi. Binary say?larda `0` say?s? veya son iki biti `00` olan say?lar 4'e b?l?n?r. Bu nedenle makine t?m girdiyi soldan sa?a okur ve sadece son bir veya iki bit bilgisini durumlarda saklar.

### 2. Durum Say?s?

Durum say?s? azd?r. `q_last0` ve `q_last1` tek semboll? girdileri temsil eder. `q_pair00`, `q_pair01`, `q_pair10`, `q_pair11` ise en son g?r?len iki biti saklar. Girdi bitti?inde makine bu duruma g?re kabul veya ret verir.

### 3. ?erit Alfabesi

?erit alfabesi yaln?zca `0`, `1` ve `B` sembollerinden olu?ur. Bu makine bir karar problemi ??zd??? i?in ?eridi de?i?tirmeye veya yard?mc? i?aretleyici kullanmaya gerek yoktur.

### 4. Karma??kl?k

Makine girdiyi bir kez soldan sa?a okur. Bu nedenle ?al??ma s?resi `O(n)`dir. Kullan?lan bilgi yaln?zca son bitler oldu?u i?in durum belle?i sabittir.

### 5. Hata Ay?klama Hikayesi

En dikkat isteyen kenar durum, tek semboll? `0` girdisini kabul ederken bo? girdiyi reddetmekti. E?er ba?lang?? durumunda `B` do?rudan kabul edilseydi bo? girdi de kabul edilmi? olurdu. Bu nedenle `q_start` durumunda `B` okununca makine `q_reject` durumuna gider.

---

## Final Kontrol Notu - 17 May?s

17 May?s Pazar g?n? B?l?m 2 i?in final kontrol yap?ld?. D?rt makine dosyas?, `tests/test_machines.py`, `docs/design_notes.md` ve `docs/week2_progress.md` dosyalar? yerinde. Test kapsam? geni?letilmi? durumda ve t?m testler ge?iyor. Bu noktada B?l?m 2, dosya yap?s? ve dok?mantasyon a??s?ndan kapat?labilir durumdad?r.
