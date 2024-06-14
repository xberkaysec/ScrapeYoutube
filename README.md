## Nasıl Çalışır

- Kullanıcıdan scrape edilecek YouTube hesabının URL'si alınır.
- Videoların sayısı ve bilgileri ekrana yazdırılır.
- Videoların başlıkları, thumbnail linkleri, görüntülenme sayıları, yükleme tarihleri ve süreleri görüntülenir.
- Son olarak, veriler JSON formatında gösterilir.

## Örnek Çıktı

```
Video Before : 260
Video After  : 260
We have reached the end! 

Thumbnail: [Linki Buraya Yapıştır]
Title: A Drag Adventure Story with @trixie & @JunoBirch
Views: 757,000
Upload: 3 days ago
Duration: 6:55
```

## Kullanılan Kütüphane

Bu program, Playwright (https://playwright.dev/)'ü kullanır. Playwright, modern web tarayıcılarını otomatize etmek için bir kütüphanedir.

## Kurulum

Öncelikle Playwright kütüphanesini yüklemelisiniz. Bunun için aşağıdaki komutu kullanabilirsiniz:

pip install playwright


## Kullanım

1. YouTube hesabı URL'sini girin örnek --> https://www.youtube.com/@youtube/videos
2. Program, videoları scrape etmeye başlayacak ve bilgileri ekrana yazdıracaktır.
