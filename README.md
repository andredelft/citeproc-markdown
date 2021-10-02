# citeproc-markdown

[Python markdown](https://github.com/Python-Markdown/markdown) extension to convert a CSL data block in markdown to a styled bibliography in the HTML output. Requires a [citeproc-js server](https://github.com/zotero/citeproc-js-server) in order to work.

## Example

### Markdown source

````markdown
# The origins of the term _anthropocene_

The term _anthropocene_ has been coined by Crutzen and Stoermer in the year 2000.

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
````

We use a fenced code block to store the CSL data. The data language is defined directly after the first backticks as `csl-<language>`, where `<language>` is the language the bibliographic data is stored in. Supported values are `yaml`, `json` and `json5`.

### Python conversion snippet

```python
from markdown import markdown
markdown(
    content, extensions=['citeproc'],
    extension_configs={
        'citeproc': {
            'citeproc_endpoint': 'DEFINE_ENDPOINT_HERE'
        }
    }
)
```

Alternatively, the endpoint can also be defined through the environment variable `CITEPROC_ENDPOINT`, either in memory or in a `.env` or `settings.ini` file in the working directory.

### HTML output

```html
<h1>The origins of the term <em>anthropocene</em></h1>
<p>The term <em>anthropocene</em> has been coined by Crutzen and Stoermer in the year 2000.</p>
<div class="csl-bib-body">
  <div class="csl-entry">Crutzen, P.J., and E.F. Stoermer. 2000. “The ‘Anthropocene.’” <i>Global Change Newsletter</i> 41: 17–18.</div>
</div>
```
