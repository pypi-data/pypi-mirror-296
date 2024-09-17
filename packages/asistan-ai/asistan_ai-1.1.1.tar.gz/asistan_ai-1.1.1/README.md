# Asistan AI Python Client

`asistan_ai` paketi, Asistan AI modeline kolayca erişim sağlayan bir Python istemcisidir. Asistan AI, GPT-Turbo modelli çok yönlü bir sohbet botudur.

## Kurulum

Paketinizi PyPI'den yüklemek için:

```bash
pip install asistan_ai
```

## Kullanım

```python
from asistan_ai import Asistan

# Kütüphaneyi başlat
asistan = Asistan()

# Bir mesaj gönder ve yanıt al
request = input("Enter message: ")
reply = asistan.message(request)
print(reply)
```

## Lisans
MIT Lisansı