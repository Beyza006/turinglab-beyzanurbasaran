# B?l?m 2 Tasar?m Notlar?

## TM-1: Unary to Binary

Strateji: Bu makine unary girdiyi ?nce uzunluk olarak sayar, sonra ayn? ?eridin solundan binary kar??l???n? yazar ve kalan eski unary h?crelerini blank sembole ?evirir. Bu s?r?mde 0-16 aral??? kapsand?; b?ylece d?n???m fikri, yazma ad?m? ve temizleme faz? geni? bir test k?mesiyle do?rulanabilir hale geldi. Daha genel s?r?mde `X` i?aretleyiciyle tekrar tekrar binary saya? art?rmak daha do?ru bir yakla??m olurdu.

Durum say?s?; sayma, ba?a d?nme, binary sonucu yazma ve eski sembolleri temizleme fazlar?na ayr?ld??? i?in y?ksektir. ?erit alfabesinde `0`, `1`, `B` ve ileride genelle?tirme i?in `X` bulunur. Desteklenen aral?kta ?al??ma do?rusal tarama ve yazma ad?mlar?ndan olu?ur. En zor hata, sonu? yaz?ld?ktan sonra eski unary sembollerinin ?eritte kalmas?yd?; bunu ayr? bir `q_clear` faz?yla ??zd?m.

## TM-2: Binary Compare

Strateji: Makine `#` ayrac?yla verilen iki canonical binary ifadeyi kar??la?t?rmak i?in geni?letilmi? bir karar a?ac? olarak kuruldu. Bu s?r?m 0-15 aras? t?m canonical say? ?iftlerini kapsar. Girdi soldan sa?a okunur; sona gelindi?inde birinci say? ikinci say?dan b?y?kse `q_accept`, de?ilse `q_reject` durumuna ge?ilir.

Durum say?s?, 0-15 aras? say? ?iftlerinin prefix a?ac?ndan gelir. Ortak ba?lang??lar payla??ld??? i?in her girdi i?in tamamen ayr? yol a??lmad?. ?erit alfabesinde yaln?zca `0`, `1`, `#` ve `B` vard?r; ??nk? bu makine ?eridi de?i?tirmez, sadece karar verir. En ?nemli hata ay?klama noktas?, e?it say?lar?n `no_transition` ile de?il a??k bir reject durumuyla bitmesini sa?lamakt?.

## TM-3: String Copy

Strateji: Makine ?nce girdinin sonuna `#` koyar. Sonra soldan sa?a ilk i?aretlenmemi? `a` veya `b` sembol?n? bulur. `a` i?in `A`, `b` i?in `C` i?aretleyicisini yazar, ?eridin sonuna gidip ayn? sembol? kopyalar ve tekrar ba?a d?ner. `#` sembol?ne gelindi?inde t?m kaynak semboller i?aretlenmi?tir; son fazda `A` tekrar `a`, `C` tekrar `b` yap?l?r.

Bu tasar?m 8 ana durum kullan?r: sona gitme, ba?a d?nme, kaynak sembol bulma, `a` kopyalama, `b` kopyalama, kopyadan sonra geri d?nme, restore etme ve kabul. `A`/`C` i?aretleyicileri kopyalanm?? semboller ile hen?z i?lenmemi? kaynak sembolleri ay?rmak i?in gereklidir. Her karakter i?in ?erit birka? kez tarand???ndan karma??kl?k yakla??k `O(n^2)` olur. En zor hata, kopyalanan sembollerin tekrar kaynak gibi i?lenmesiydi; `q_find` durumunu `#` sembol?nde durdurunca bu sorun ??z?ld?.

## TM-4: Student Choice - Binary 4'e B?l?nebilirlik

Strateji: Se?im makinesi binary girdinin 4'e b?l?n?p b?l?nmedi?ini test eder. Binary say?larda `0` say?s? veya son iki biti `00` olan say?lar 4'e b?l?n?r. Bu nedenle makine girdiyi soldan sa?a okur ve yaln?zca son bir veya iki bit bilgisini durumlarda saklar.

Durum say?s? azd?r. `q_last0` ve `q_last1` tek semboll? girdileri, `q_pair00`, `q_pair01`, `q_pair10`, `q_pair11` ise son iki biti temsil eder. Ek ?erit sembol?ne gerek yoktur; ??nk? bu bir karar problemidir ve ?erit de?i?tirilmeden ??z?lebilir. En dikkat isteyen kenar durum, tek semboll? `0` girdisini kabul ederken bo? girdiyi reddetmekti.

## 15 May?s Test Kapsam? G?ncellemesi

Test dosyas? yaln?zca tekil ?rnekleri kontrol eden bir yap?dan ??kar?ld?. `unary_to_binary` i?in desteklenen 0-16 aral???n?n tamam?, `binary_compare` i?in 0-15 aras? t?m canonical say? ?iftleri parametrik testlerle kontrol ediliyor. `string_copy` taraf?nda daha uzun `a`/`b` dizgileri ve bilinmeyen sembol durumu eklendi. `student_choice` i?in de 4'e b?l?nen, b?l?nmeyen, bo? ve leading-zero i?eren girdiler ayr?ld?. B?ylece testler kabul, ret ve `no_transition` davran??lar?n? daha a??k g?steriyor.
