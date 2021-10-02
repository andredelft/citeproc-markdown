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
  title The Anthropocene  # Forgot a colon!
  type: article-journal
  volume: '41'
```

```csl-json5
[
  {
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
    // because of the dash, 'container-title' has to be wrapped in quotes
    container-title: "Global Change Newsletter",
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
