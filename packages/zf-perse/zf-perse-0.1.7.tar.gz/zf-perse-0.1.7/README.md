# Perse

[![PyPI version](https://badge.fury.io/py/zf-perse.svg)](https://badge.fury.io/py/zf-perse)

<p align="center">
  <img src="https://zf-static.s3.us-west-1.amazonaws.com/perse-logo128.png" alt="Perse"/>
</p>

Perse converts `HTML` to `JSON` using a mix of traditional html parsing and LLM based data extraction.

### Features

It's core features includes:

- Identify important fields to extract from html
- Building a JSON schemas that handles nested fields
- Process html tokens and fill the JSON schema object

It performs a few optimizations after fetching the html while preventing any accidental removal of important data.

These optimizations includes:

- Removal of styling, scripting and svg tags
- Collapsing Tags (e.g. divs) with only one child

## Comparison

There are a few other libraries but none of them provide a solution for reliable data extraction from html.

### HTML to JSON

[html2json](https://pypi.org/project/html-to-json/) library is a simple html to json converter that doesn't handle nested fields, nor does it remove unnecessary tags.

When ran on exactly the same html, Perse provides a more structured and cleaner output and at least 50% less verbose output.

<table>
<tr>
<th>HTML to JSON</th>
<th>Perse</th>
</tr>
<tr>
<td>
    <img src="https://zf-static.s3.us-west-1.amazonaws.com/perse-output-htmltojson.png" width="250px" alt="rate_1.0">
</td>
<td>
    <img src="https://zf-static.s3.us-west-1.amazonaws.com/perse-output-perse.png" width="250px" alt="rate_1.0">
</td>
</tr>
</table>

## Installation

```bash
pip install zf-perse
```

## Usage

```bash
export PERSE_OPENAI_API_KEY="your-openai-api-key"
```

### CLI

```bash
perse --url https://example.com
```

### Python

```python
from perse import perse

url = "https://example.com"
html = requests.get(url).text
j = perse(html)
print(j)
```

## Example

## Google's Homepage

```bash
$ perse --url https://google.com

{
  "title": "Google",
  "image": "/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
  "nav_links": [
    {
      "link_text": "About",
      "link_url": "https://about.google/?fg=1&utm_source=google-SG&utm_medium=referral&utm_campaign=hp-header"
    },
    {
      "link_text": "Store",
      "link_url": "https://store.google.com/SG?utm_source=hp_header&utm_medium=google_ooo&utm_campaign=GS100042&hl=en-SG"
    }
  ],
  "logo": "/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
  "search_form": {
    "search_query": "",
    "submit_button": "Google Search",
    "lucky_button": "I'm Feeling Lucky"
  },
  "footer_languages": [
    {
      "language_name": "\u4e2d\u6587(\u7b80\u4f53)",
      "language_url": "https://www.google.com/setprefs?sig=0_FYvV2GBLTXBgHB1mWB1S3fkaxOc%3D&hl=zh-CN&source=homepage&sa=X&ved=0ahUKEwj3ip2pw8iIAxUy1zgGHYB0DtkQ2ZgBCBc"
    },
    {
      "language_name": "Bahasa Melayu",
      "language_url": "https://www.google.com/setprefs?sig=0_FYvV2GBLTXBgHB1mWB1S3fkaxOc%3D&hl=ms&source=homepage&sa=X&ved=0ahUKEwj3ip2pw8iIAxUy1zgGHYB0DtkQ2ZgBCBg"
    },
    {
      "language_name": "\u0ba4\u0bae\u0bbf\u0bb4\u0bcd",
      "language_url": "https://www.google.com/setprefs?sig=0_FYvV2GBLTXBgHB1mWB1S3fkaxOc%3D&hl=ta&source=homepage&sa=X&ved=0ahUKEwj3ip2pw8iIAxUy1zgGHYB0DtkQ2ZgBCBk"
    }
  ],
  "footer_links": [
    {
      "footer_link_text": "Advertising",
      "footer_link_url": "https://www.google.com/intl/en_sg/ads/?subid=ww-ww-et-g-awa-a-g_hpafoot1_1!o2&utm_source=google.com&utm_medium=referral&utm_campaign=google_hpafooter&utm_fg=1"
    },
    {
      "footer_link_text": "Business",
      "footer_link_url": "https://www.google.com/services/?subid=ww-ww-et-g-awa-a-g_hpbfoot1_1!o2&utm_source=google.com&utm_medium=referral&utm_campaign=google_hpbfooter&utm_fg=1"
    },
    {
      "footer_link_text": "How Search works",
      "footer_link_url": "https://google.com/search/howsearchworks/?fg=1"
    },
    {
      "footer_link_text": "Privacy",
      "footer_link_url": "https://policies.google.com/privacy?hl=en-SG&utm_fg=1"
    },
    {
      "footer_link_text": "Terms",
      "footer_link_url": "https://policies.google.com/terms?hl=en-SG&utm_fg=1"
    }
  ]
}
```

### Zeff Muks's Homepage

```bash
$ perse --url https://zeffmuks.com

{
  "title": "Zeff Muks",
  "description": "Antifragile Entropy Assassin \ud83e\udd77",
  "og_data": {
    "type": "website",
    "title": "Zeff Muks",
    "description": "Antifragile Entropy Assassin \ud83e\udd77",
    "url": "https://zeffmuks.com/",
    "image": "https://www.zeffmuks.com/images/ZeffMuks-1920.png",
    "site_name": "Zeff Muks"
  },
  "twitter_data": {
    "card": "summary_large_image",
    "site": "@zeffmuks",
    "title": "Zeff Muks",
    "description": "Antifragile Entropy Assassin \ud83e\udd77",
    "image": "https://www.zeffmuks.com/images/ZeffMuks-1920.png"
  },
  "user_section": {
    "header": {
      "profile_image_url": "/images/ZeffMuks-6912.png",
      "title": "Antifragile Entropy Assassin \ud83e\udd77",
      "signature": ""
    },
    "builds": [
      {
        "date": "08/30/2024",
        "name": "Cursor Git",
        "description": "Enhanced Git for Cursor AI Editor",
        "download_link": "https://zf-static.s3.us-west-1.amazonaws.com/cursor-git-0.1.12.vsix",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/cursor-git-logo128.png",
        "alternative_link": ""
      },
      {
        "date": "08/18/2024",
        "name": "PyZF",
        "description": "Enhancements for Python",
        "download_link": "https://pypi.org/project/PyZF",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/pyzf-logo128.png",
        "alternative_link": ""
      },
      {
        "date": "08/05/2024",
        "name": "Xanthus",
        "description": "X (formerly Twitter) Assistant",
        "download_link": "https://pypi.org/project/zf-xanthus",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/xanthus-logo128.png",
        "alternative_link": ""
      },
      {
        "date": "07/24/2024",
        "name": "Jenga",
        "description": "Fast JSON5 Python Library",
        "download_link": "https://pypi.org/project/zf-jenga",
        "preview_image": "",
        "alternative_link": ""
      },
      {
        "date": "07/12/2024",
        "name": "Pegasus",
        "description": "Next Generation Tech Stack",
        "download_link": "https://zf-static.s3.us-west-1.amazonaws.com/pegasus.zip",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/pegasus-logo128.png",
        "alternative_link": ""
      },
      ...
      {
        "date": "11/01/2023",
        "name": "Z",
        "description": "Next Generation Content Platform",
        "download_link": "https://x.com/zeffmuks/status/1718507463321010429",
        "preview_image": "https://zf-static.s3.us-west-1.amazonaws.com/z-logo128.png",
        "alternative_link": "https://alpha.thez.ai/try"
      }
    ]
  }
}
```

## License

[MIT License](./LICENSE)
