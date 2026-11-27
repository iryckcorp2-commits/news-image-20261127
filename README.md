[![make.fun - news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/iryckcorp2-commits/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/iryckcorp2-commits/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

# The World Today — 27 November 2026

A newspaper front page for Friday, 27 November 2026, drawn entirely in
code. Six stories defined the day: two tankers hit mines in the Strait of
Hormuz, Houthi strikes on Saudi energy assets and Riyadh, Russian strikes
on two grain ships near Odesa, Asian shares bouncing as Nvidia slid, Trump
demanding a probe of GDP data released before the midterms, and
Guinea-Bissau delaying its elections by about two years. The image uses no
photos at all: the masthead, rules, story cards and every letter are rendered
by a small Python program with a hand-built bitmap font and its own PNG
encoder, so the output is byte-identical on every run.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png`, a 1024x1024 PNG under 1 MiB.
