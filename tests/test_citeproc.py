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


@pytest.fixture
def markdown_csl_blocks():
    return MARKDOWN_CSL_BLOCKS


def test_citeproc(markdown_csl_blocks):
    html = markdown(markdown_csl_blocks, extensions=['citeproc'])
    with open(OUTPUT_DIR / 'citeproc.html', 'w') as f:
        f.write(html)
