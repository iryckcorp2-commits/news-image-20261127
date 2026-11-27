# The World Today

[![Bounty](https://img.shields.io/badge/bounty-news--image--20261127-blue)](https://make.fun/bounty/news-image-20261127)
[![Prize](https://img.shields.io/badge/prize-%24100-green)](https://make.fun/bounty/news-image-20261127)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

This program sums up the world news of Friday 27 November 2026 in a single
front-page image. One page, six stories, the day's headlines at a glance.

## How it works

The front page is pre-rendered as `entry.png` and shipped in this repository.
`main.py` copies that image to the output directory the harness expects:

```sh
python3 main.py
```

By default the image lands at `/output/entry.png`. Setting the
`MAKEFUN_OUTPUT_DIR` environment variable sends it somewhere else instead.
The copy is byte-for-byte identical to the `entry.png` shipped here, so the
front page you see in this repository is exactly the front page the program
produces.
The program uses only the Python standard library, so it runs on a bare
Python 3.13 interpreter with nothing extra installed.

## The six stories

The front page covers these stories from 27 November 2026:

- **Hormuz mine strikes** — tankers hit by mines near the Strait of Hormuz.
- **Houthi strikes on Saudi Arabia** — attacks on a refinery and Riyadh.
- **Russia grain ships near Odesa** — two grain carriers struck in the Black Sea.
- **Asia markets bounce** — stocks rebound across the region.
- **Trump GDP data probe** — the president demands an investigation into GDP figures.
- **Guinea-Bissau election delay** — the vote pushed back by about two years.
