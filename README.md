# TransfereGov PAC scraper

A one-file Selenium script that opens [TransfereGov](https://idp.transferegov.sistema.gov.br/idp/) as a guest, goes to **Propostas → Seleção PAC**, and downloads the Excel export from each page of the proposal list.

There is no app, API, or extra modules. Everything lives in `transfere_scraping.py`. The only commit (`12c77b0`, 9 Jul 2024) is titled **“Two bugs to fix”** — those bugs are still in the script (see [Known issues](#known-issues)).

## Repo map

```
web_scraping_gov_br/
└── transfere_scraping.py   # the whole project: browser automation + Excel downloads
```

| Where | What it is |
| --- | --- |
| Lines 8–11 | `click_next_button` — clicks the RichFaces pager “next” control when the visible page range ends (10, 20, 30, …) |
| Lines 13–17 | Chrome options (small window; headless is commented out) |
| Lines 19–36 | Login-as-guest and navigation to the PAC list, then first Excel download |
| Lines 38–61 | Loop over pages 2–60: click a page, download Excel, jump the pager when needed |
| Line 62 | Comment documenting the two bugs |

Unused imports at the top (`requests`, `BeautifulSoup`) look like leftovers from an earlier attempt. The live path is Selenium only.

## What it was trying to collect

**TransfereGov** is the Brazilian federal platform for voluntary transfers (convênios / PAC). After **Acesso livre** (no login), the script opens the PAC proposal table and clicks the Excel link on each page:

`formListarPropostaPac:dtListarPropostaPac:excelLink`

Chrome then saves the files to the browser’s default download folder (not a folder inside this repo).

The loop is hardcoded to pages **2 through 60**. Page 1 is downloaded before the loop. Pages whose number ends in `0` are skipped on purpose (see below).

## How the flow works

```
Chrome
  → https://idp.transferegov.sistema.gov.br/idp/
  → click “Acesso livre”  (class tg_btn_a)
  → menu “Propostas”
  → “Seleção PAC”
  → download Excel on page 1
  → for page 2..60:
        if page ends with 1  → already landed here after “next”; just download
        if internal counter ends with 0  → skip download, click Next, reset counter
        else  → click the page number link, then download
```

The table uses a **RichFaces data scroller** (`richDataScrollerInactiveStyleClass`). Only about 10 page numbers are visible at a time, and the link text includes a trailing comma (`"2,"`, `"3,"`, …). That is why the XPath is built from `page_text` instead of a simple integer.

The extra counter `i` tracks position inside the current 10-page window so the script can hit the Next span (`richDataScroller_3`) instead of a page that is no longer on screen.

## Setup and run

Needs Python 3, Google Chrome, and a matching ChromeDriver (Selenium 4 can manage the driver itself).

```bash
pip install selenium
python transfere_scraping.py
```

A Chrome window should open, walk the menus, and start downloading Excel files. Headless mode is present but commented out (`#options.add_argument('--headless')`).

The site and its DOM IDs may have changed since mid-2024. If locators fail, inspect the live page and update the IDs / XPaths in the script.

## Known issues

These are the two problems called out in the commit message and in the last comment:

1. **Pages ending in 0 are never downloaded** (10, 20, 30, …). The branch that clicks Next also `continue`s without clicking `excelLink`. The print is: `nao faz download do arquivo que o numero acaba em 0`.
2. **Chrome closes around page 20** (`fecha inesperadamente quando chega no 20`). Likely a stale element, a pager ID that changes after the second “next”, or the site killing the session. There is no retry or wait-for-element logic — only `sleep()`.

Other rough edges:

- No `requirements.txt`, no `.gitignore`, no output directory.
- Fixed sleep timings; no explicit waits (`WebDriverWait`).
- Page range `2..61` is hardcoded; it will miss extra pages or idle on fewer.
- Download location is whatever Chrome uses by default.

## If you pick this up again

A reasonable next pass would be: wait for the table instead of sleeping, download the current page *before* clicking Next (so 10/20/30 are included), and stop when the Next control is disabled instead of assuming 60 pages.
