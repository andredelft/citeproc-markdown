import pytest
from markdown import markdown
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / 'output'

# Ensure OUTPUT_DIR exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MARKDOWN_CSL_BLOCKS = """
```csl-yaml
- id: crutzenAnthropocene2000
  author:
    - family: Crutzen
      given: P.J.
    - family: Stoermer
      given: E.F.
  container-title: Global Change Newsletter
  issued:
    raw: "2000"
  page: 17-18
  title: The “Anthropocene”
  type: article-journal
  volume: '41'
```

```csl-json5
[
  {
    // I can put a comment here!
    id: "crutzenAnthropocene2000",
    author: [
      {
        family: "Crutzen",
        given: "P.J.",
      },
      {
        family: "Stoermer",
        given: "E.F.",
      },
    ],
    "container-title": "Global Change Newsletter",
    issued: {
      raw: "2000",
    },
    page: "17-18",
    title: "The 'Anthropocene'",
    type: "article-journal",
    volume: "41",
  },
]
```

```csl-json
[
  {
    "id": "crutzenAnthropocene2000",
    "author": [
      {
        "family": "Crutzen",
        "given": "P.J."
      },
      {
        "family": "Stoermer",
        "given": "E.F."
      }
    ],
    "container-title": "Global Change Newsletter",
    "issued": {
      "raw": "2000"
    },
    "page": "17-18",
    "title": "The “Anthropocene”",
    "type": "article-journal",
    "volume": "41"
  }
]
```
"""

MARKDOWN_MALFORMED_CSL_BLOCK = """
```csl-json
[
  {
    "id": "crutzenAnthropocene2000",
    "author": [
      {
        "family": "Crutzen",
        "given": "P.J."
      },
      {
        "family": "Stoermer",
        "given": "E.F."
      }
    ],
    "container-title": "Global Change Newsletter,
    "issued": {
      "raw": "2000"
    },
    "page": "17-18",
    "title": "The “Anthropocene”",
    "type": "article-journal",
    "volume": "41"
  },
]
```
"""


@pytest.fixture
def markdown_csl_blocks():
    return MARKDOWN_CSL_BLOCKS


@pytest.fixture
def markdown_malformed_csl_block():
    return MARKDOWN_MALFORMED_CSL_BLOCK


def test_citeproc(markdown_csl_blocks, markdown_malformed_csl_block):
    html = markdown(
        markdown_csl_blocks,
        extensions=['citeproc'],
        extension_configs={
            'citeproc': {'surpress_errors': False}
        }
    )
    with open(OUTPUT_DIR / 'citeproc.html', 'w') as f:
        f.write(html)

    # Malformed CSL block
    html = markdown(
        markdown_malformed_csl_block,
        extensions=['citeproc']
    )
    with open(OUTPUT_DIR / 'malformed-citeproc.html', 'w') as f:
        f.write(html)

    # Malformed CSL block (fenced code return)
    html = markdown(
        markdown_malformed_csl_block,
        extensions=['citeproc', 'fenced_code'],
        extension_configs={
            'citeproc': {'fenced_code_on_fail': True}
        }
    )
    with open(OUTPUT_DIR / 'malformed-citeproc-fc.html', 'w') as f:
        f.write(html)
