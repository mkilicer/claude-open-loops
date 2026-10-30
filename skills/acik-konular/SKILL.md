---
name: acik-konular
description: Konuşmada açık kalan uçları (cevapsız soru, bulunan hata, onay bekleyen öneri) projenin tek "Açık konular" listesine yazar, kapananı işaretler, oturum başında hatırlatır. Kullanıcı başka konuya geçtiğinde geride açık uç kaldıysa SORMADAN kullan; ayrıca kullanıcı "açık konular", "neler kaldı", "unuttuğumuz", "bekleyenler" deyince ya da bir maddeyi bitirince.
---

# Açık konular

Kullanıcı (30.10.2026): "bir şey konuşuyorum, konu kesilince ya da başka konuya atlayınca eski konuları unutuyorum —
cevaplanmamış sorular, senin bulduğun hatalar geride kalıyor." Bu beceri o uçları yakalar ve her projede **tek bir
listede** toplar. Kullanıcı hatırlamak zorunda değil; yakalamak senin işin.

## Liste nerede

Her projede bir tane:

1. **GitHub deposu varsa** (`gh repo view` çalışıyorsa): `acik-konu` etiketli **tek açık issue**, başlığı
   `Açık konular — unutulmasın`. Bul: `gh issue list --label acik-konu --state open --json number,title,body`.
   Yoksa aç (etiket yoksa önce `gh label create acik-konu --color fbca04 --description "Konuşmada açık kalan uçlar"`).
   Birden fazla açık bulunursa en eskisini kullan, kullanıcıya söyle.
2. **GitHub yoksa:** `~/.claude/acik-konular/<proje-klasörü-adı>.md` (repoya girmez). Aynı biçim.

Gövde biçimi — başlıklar sabit, maddeler işaretlenebilir kutu:

```markdown
### Onay bekleyen öneriler
- [ ] **Kısa ad.** Ne öneriliyor, hangi rakamla (ölçüm, tarih). Karar: <kullanıcının vermesi gereken karar>
### Bulunan sorunlar
- [ ] **Kısa ad.** Ne oldu, nerede (dosya:satır / log saati), etkisi. Karar: <düzeltilsin mi / nasıl>
### Cevapsız sorular
- [ ] **Kısa ad.** Kimin sorusu, ne soruldu.
### Bilgi (karar gerekmez)
- Unutulmaması gereken ölçüm ya da cevap; kutusuz.
```

Her madde tek başına anlaşılır olsun: konuşmayı görmeyen biri (ya da yeni oturumdaki sen) okuyunca neyin beklendiğini
bilmeli. Tarih yaz (gg.aa). Rakamı uydurma; ölçmediysen "ölçülmedi" yaz.

## Ne zaman yazılır — sormadan

- Kullanıcı başka konuya geçti ve önceki konuda şunlardan biri kaldı: senin sorduğun ama cevaplanmamış soru, senin
  bulduğun ama düzeltilmemiş hata/tutarsızlık, onay bekleyen önerin, "sonra bakarız" denen iş.
- Uzun bir cevabın sonunda karar bekleyen birden çok madde varsa, cevabı verdikten sonra yaz.
- Kullanıcı "açık konulara ekle", "unutmayalım" derse hemen.

Yazmadan sorma: issue kullanıcının kendi deposunda, geri alınabilir, kullanıcı bu işi sana bıraktı. Düzenlemeyi
`gh issue edit <no> --body-file <dosya>` ile yap (gövdeyi önce `gh issue view <no> --json body` ile oku, maddeyi ekle,
ötekileri koru). Aynı konu zaten listede ise yenisini açma, var olanı güncelle.

Yazma: bu oturumda hemen bitirilecek işi; kullanıcının açıkça "gerek yok / vazgeçtim" dediğini (listede varsa kapat).

## Kapatma

- Madde çözülünce (karar verildi, düzeltildi, cevaplandı): kutuyu `[x]` yap ve sonuna `→ <sonuç, gg.aa>` ekle.
  Kararın gerekçesi commit mesajına / ilgili yere de gitsin; issue yalnız takip listesi.
- Bütün kutular `[x]` olunca işaretli maddeleri sil (gövde kısa kalsın); liste boşalırsa issue'yu kapatma — boş
  bırak, bir sonraki açık uç oraya yazılır.

## Hatırlatma

- Oturum başında `~/.claude/scripts/acik_konular_hook.sh` (SessionStart kancası) açık maddeleri bağlama koyar. Varsa ilk
  cevabının sonuna tek satır: `Açık konular: N (#<issue>) — en eskisi: <kısa ad>`. Kullanıcı başka şey soruyorsa uzatma.
- Cevap verdiğin konu listedeki bir maddeyi kapatıyorsa, cevabın sonunda söyle ve kutuyu işaretle.
- Kullanıcı "neler kaldı" derse listeyi kısa ver: madde başına bir satır, beklenen karar.

## Kullanıcıya söyleme

Listeye yazdığında cevabın sonuna tek satır: `Açık konulara eklendi: <kısa ad> (#<issue>)`. Bağlantıyı ilk seferde ver.
