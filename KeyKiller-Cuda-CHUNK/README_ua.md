<!--
  KeyKiller-Cuda-CHUNK
  https://github.com/egorrushka/KeyKiller-Cuda-CHUNK
  Copyright (C) 2025  egorrushka
  Ліцензія: GNU AGPL v3 — дивись LICENSE.txt
  Оригінальний код: https://github.com/Qalander/KeyKiller-Cuda
-->

# main.cpp — KeyKiller з підтримкою чанків

**Базується на:** [KeyKiller-Cuda](https://github.com/Qalander/KeyKiller-Cuda)  
**Оригінальні автори:** Jean-Luc Pons / VanitySearch, FixedPaul, 8891689  
**Тестувалось на:** NVIDIA RTX A4000 (48×128 ядер, SM86), Windows 10 x64

---

## Що змінено

Це **пряма заміна** оригінального `main.cpp`.  
Жодних інших файлів проєкту змінювати не потрібно — просто замінити і перекомпілювати.

### Додано: флаги `-s` / `-e` (режим чанку)

Оригінальна програма підтримувала лише `-r <bits>`, який завжди шукав  
**повний** бітовий діапазон (наприклад `-r 71` = весь 2^70 → 2^71-1).

Нові флаги дозволяють шукати в **будь-якому довільному відрізку (чанку)**:

| Флаг | Опис |
|------|------|
| `-s <hex>` | Початок чанку (hex, з префіксом `0x` або без) |
| `-e <hex>` | Кінець чанку (hex, з префіксом `0x` або без) |

`-s` та `-e` завжди використовуються разом.  
Флаг `-r` (оригінальний режим) повністю збережено і працює як раніше.

### Додано: функція `parseHex()`

Внутрішній хелпер для парсингу 256-бітних hex-значень (з префіксом `0x` або без)  
у тип `Int`, який використовує рушій програми.

---

## Використання

```bat
:: Оригінальний режим — повний діапазон пазлу
kk.exe -a 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU -r 71

:: Режим чанку — конкретний відрізок діапазону
kk.exe -a 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU -s 0x400000000000000000 -e 0x43ffffffffffffff

:: Режим чанку — без префіксу 0x
kk.exe -a 1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU -s 400000000000000000 -e 43ffffffffffffff

:: Всі оригінальні флаги працюють
kk.exe -a <addr> -r 71 -R          (випадковий режим)
kk.exe -a <addr> -r 71 -b          (резервне збереження / продовження)
kk.exe -a <addr> -r 71 -G 1        (ID пристрою GPU)
kk.exe -p <pubkey> -s <hex> -e <hex>
```

---

## Компіляція (Windows, CUDA 12, VS Build Tools)

Відкрий **x64 Native Tools Command Prompt** і виконай:

```bat
nvcc main.cpp Vanity.cpp SECP256K1.cpp Int.cpp IntMod.cpp IntGroup.cpp ^
     Point.cpp Timer.cpp Random.cpp Base58.cpp Bech32.cpp Wildcard.cpp ^
     GPU\GPUEngine.cu GPU\GPUGenerate.cpp ^
     hash\ripemd160.cpp hash\ripemd160_sse.cpp ^
     hash\sha256.cpp hash\sha256_sse.cpp hash\sha512.cpp ^
     -o kk.exe ^
     -O3 --use_fast_math ^
     -gencode=arch=compute_86,code=sm_86 ^
     -m64 -Xcompiler "/W0" -DWIN64 ^
     -Xlinker advapi32.lib
```

> Для інших відеокарт змінити `-gencode` архітектуру:  
> RTX A4000 / RTX 3090 / RTX 3080 → `compute_86,code=sm_86`  
> RTX 4090 / RTX 4080 → `compute_89,code=sm_89`  
> RTX 2080 Ti → `compute_75,code=sm_75`  
> GTX 1080 Ti → `compute_61,code=sm_61`

---

## Результати тестування на RTX A4000

| Режим | Швидкість |
|-------|-----------|
| Адресний (P2PKH Compressed) | ~1560 Mkey/s |
| Публічний ключ (-p) | ~2x швидше (без хешування) |

---

## Довідка по всіх флагах

```
kk.exe [-a <addr> | -p <pubkey>]  [діапазон]  [опції]

Ціль:
  -a <b58_addr>    Пошук приватного ключа для P2PKH Bitcoin-адреси (стиснутий)
  -p <pubkey>      Пошук приватного ключа для стиснутого публічного ключа (hex)

Діапазон (вибрати одне):
  -r <bits>        Повний бітовий діапазон: 2^(bits-1) до 2^bits-1
  -s <hex>         Початок чанку  (разом з -e)
  -e <hex>         Кінець чанку   (разом з -s)

Опції:
  -R               Випадковий режим
  -b               Резервне збереження / продовження (файл schedule_gpu0.dat)
  -G <id>          ID пристрою GPU (за замовчуванням: 0)
  -h, --help       Довідка

Клавіша 'p' = пауза / продовження     Ctrl+C = коректна зупинка
```

---

## Примітки

- Підтримуються тільки **Compressed P2PKH** адреси (пазли #51 і вище)
- Пазли #1–#50 використовують Uncompressed ключі — kk.exe їх не знайде
- Знайдені ключі автоматично зберігаються у файл `found.txt`
- Файл резервного збереження: `schedule_gpu0.dat` (створюється при флагу `-b`)
