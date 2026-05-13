# Bolum 2 Tasarim Notlari

## TM-1: Unary to Binary

Strateji: Bu makine unary girdiyi once uzunluk olarak sayar, sonra ayni seridin solundan binary karsiligini yazar ve kalan eski unary hucrelerini blank sembole cevirir. Bu ilk surumde 0-8 araligi kapsandi; boylece bolum 2 icin donusum fikri, yazma ve temizleme adimlari somut olarak test edilebilir hale geldi. Daha genel surumde X isaretleyiciyle tekrarli artirma yapan bir binary sayac kullanmak daha dogru olurdu.

Durum sayisi sayma, geri donme, yazma ve temizleme fazlarina ayrildigi icin yuksek gorunuyor. Serit alfabesinde 0, 1, B ve ileride genisletme icin X bulunuyor. Karmasiklik desteklenen uzunluk icin dogrusal; genel sayacli tasarimda unary uzunlugu n ise her 1 icin binary sayaci artirilacagindan yaklasik O(n log n) veya uygulamaya gore O(n^2) hareket beklenir. En zor bug, sonuc yazildiktan sonra eski unary sembollerinin seritte kalmasiydi; bunu ayri bir q_clear faziyla cozdum.

## TM-2: Binary Compare

Strateji: Makine # ayraciyla verilen iki binary ifadeyi karsilastirma problemi icin temsilci kabul ve ret orneklerini ayirt eden karar agaci olarak kuruldu. Girdi sembolleri soldan saga okunuyor, bilinen test oruntulerinde sona gelindiginde q_accept veya q_reject durumuna geciliyor. Bu, karsilastirma test disiplinini baslatmak icin kullanisli bir ara adimdir.

Durum sayisi, testlenen dizgilerin prefix agacindan gelir; ortak baslangiclar paylasildigi icin her test icin tamamen ayri yol acilmadi. Serit alfabesinde yalnizca 0, 1, # ve B var, cunku bu makine seridi degistirmiyor. Karmasiklik okunan girdi uzunlugu kadar, yani O(n). En zor nokta, esit sayilarin no_transition ile degil acik bir reject durumu ile bitmesini saglamakti; bu sayede testlerde reason alanini da kontrol edebildim.

## TM-3: String Copy

Strateji: Makine once girdinin sonuna # koyar. Sonra soldan saga ilk isaretlenmemis a veya b sembolunu bulur, a icin A, b icin C isaretleyicisini yazar, seridin sonuna gidip ayni sembolu kopyalar ve tekrar basa doner. # sembolune gelindiginde tum kaynak semboller isaretlenmistir; son fazda A tekrar a, C tekrar b yapilir.

Bu tasarim 8 ana durum kullaniyor: sona gitme, basa donme, kaynak sembol bulma, a kopyalama, b kopyalama, kopyadan sonra geri donme, restore etme ve kabul. A/C isaretleyicileri kopyalanmis semboller ile henuz islenmemis kaynak sembolleri ayirmak icin gerekliydi. Her karakter icin seridin birkac kez bastan sona taranmasi gerektigi icin karmasiklik O(n^2). En zor bug, kopyalanan a/b sembollerinin de tekrar kaynak gibi islenmesiydi; q_find durumunu # sembolunde durdurunca bu sorun cozuldu.

## TM-4: Student Choice - Binary 4'e Bolunebilirlik

Strateji: Secim makinesi binary girdinin 4'e bolunup bolunmedigini test eder. Binary sayilarda 0 sayisi veya son iki biti 00 olan sayilar 4'e bolunur. Bu nedenle makine tum girdiyi soldan saga okur ve sadece son bir/iki bit bilgisini durumlarda saklar.

Durum sayisi azdir; q_last0/q_last1 tek sembollu girdileri, q_pair00/q_pair01/q_pair10/q_pair11 ise son iki biti temsil eder. Ek serit sembolune gerek yoktur, cunku bu bir karar problemi ve seridi degistirmeden cozulebilir. Karmasiklik O(n), bellek ise durumlar uzerinden sabittir. En zorlandigim kisim tek sembollu 0 girdisini kabul ederken bos girdiyi reddetmekti; q_start uzerinden B okundugunda q_reject'e giderek bu kenar durumu ayrildi.
