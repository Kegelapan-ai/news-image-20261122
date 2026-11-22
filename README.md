# The Day in the World — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Kegelapan-ai/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Kegelapan-ai/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Built for the make.fun bounty: https://make.fun/bounty/news-image-20261122

An entry for the [make.fun bounty “Sum up 22 November's world news in one
image”](https://make.fun/bounty/news-image-20261122): one picture that sums
up Sunday 22 November 2026, drawn as a one-page newspaper front page. The
date is printed large at the top, so the picture stands on its own — a
viewer who missed the day can tell what happened from the image alone.

## The six stories

Every claim in the picture was checked against live reporting published on
22 November 2026. Where reports disagreed, the picture uses the cautious
figure or drops the number.

1. **COP31 collapses — no deal.** After two weeks in Antalya, Türkiye, and
   two days of overtime, the UN climate summit ended on Sunday with no
   final pact. The draft deal did not mention fossil fuels at all, the EU
   refused to endorse it, and UN Secretary-General António Guterres called
   the outcome “deeply disappointing”. It became the longest COP ever.
   Sources: UN News, CNN, AP.
2. **Drone flattens flats near Kyiv; 14 missing.** A Russian drone struck
   a five-storey block in Dymer, north of Kyiv, on Sunday morning. Nine
   people were rescued; 14 were still unaccounted for. President Zelenskyy
   said Russia fired 165 missiles at Ukraine in one week. Source: Reuters.
3. **Iran hits Bahrain; US denies jet claim.** Bahrain said two people
   were hurt when an Iranian strike hit a civilian site. Iran claimed it
   hit US Patriot radars; US Central Command denied Iran's claim that it
   damaged a US F-16 jet. Sources: Reuters, AND Magazine morning brief.
4. **Factory fire kills 3; dozens missing (Indonesia).** Rescuers searched
   a burned-out candy factory in Cikande, Banten, on Sunday. Three workers
   were killed and 36 were still missing; the cause has not been announced.
   Source: Reuters.
5. **Boat toll rises to 24 after funeral trip (Nigeria).** At least 24
   people died when a crowded boat carrying mourners to a funeral capsized
   in Bayelsa State. The toll rose on Sunday as more bodies were found;
   24 survivors were rescued. Source: Reuters.
6. **NATO calls emergency talks after missiles land in Poland.** NATO
   ambassadors meet in Brussels on Monday after Russian missiles and a
   drone came down in south-east Poland. NATO chief Mark Rutte said the
   alliance will defend “every inch” of Polish territory. Sources:
   EU Today, Polish Press Agency.

Also in the footer strip: Shuri Castle's rebuilt main hall celebrated in
Okinawa on Sunday, seven years after the 2019 fire (AP); two more tankers
struck near the Strait of Hormuz on Saturday (UKMTO, via AND Magazine);
the EU–Indonesia trade deal signed on Saturday after a decade of talks
(EU/press reporting); and the Wall Street Journal's report that President
Trump's bid to meet North Korea's Kim Jong Un failed.

## Deliberately left out

- **21 November stories with no new 22 November development.** The capture
  of cartel boss “El Chapo Isidro” in Sinaloa, the Russian missile strike
  on Kryvyi Rih, the Russian cargo ship fire in the Gulf of Finland, the
  EU–Indonesia signing itself, and the ICJ's Rohingya genocide verdict
  (19 November) all belong to earlier days, so none of them leads the page.
  The EU–Indonesia deal appears only in the footer, dated Saturday.
- **Unverified claims.** Iran's claim of destroying two US Patriot radars
  and of downing US drones is reported as a claim, not as fact; CENTCOM's
  denial of the F-16 claim is stated alongside it. No casualty figure is
  used where the sources conflicted — Indonesian police put the factory
  missing near 50 while the rescue agency said 36, so the picture uses the
  rescue agency's 36 and the headline says “dozens missing”.
- **Market numbers.** Friday's stock falls (S&P 500, Nasdaq) were 20–21
  November news, not 22 November, so they are not in the picture.

## How it is made

`build_image.py` draws the front page with Pillow only: DejaVu fonts from
the system, fixed colours and positions, no clock, no randomness, no
network. It writes `image.png` (1024×1024, about 140 KB). `main.py` is the
competition entry point (Python standard library only): it copies
`image.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, defaulting to
`/output/entry.png`.

## Build and run

```sh
python3 build_image.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs of `main.py` write byte-identical files (same SHA-256 as
`image.png`), and re-running `build_image.py` reproduces `image.png`
exactly. The image was viewed and checked for legibility, overlaps and
clipping before this was finished.

## License

MIT — see `LICENSE`.
