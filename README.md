# citeproc-markdown

[Python markdown](https://github.com/Python-Markdown/markdown) extension to convert a CSL YAML block in markdown to a styled bibliography in the HTML output. Requires a [citeproc-js server](https://github.com/zotero/citeproc-js-server) in order to work.

## Example

### Markdown source

````markdown
# The origins of the term 'Anthropocene'

The term _anthropocene_ has been coined by Crutzen and Stoermer in the year 2000.

```bibl
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

### HTML output

```html
<h1>The origins of the term 'Anthropocene'</h1>
<p>The term <em>anthropocene</em> has been coined by Crutzen and Stoermer in the year 2000.</p>
<div class="csl-bib-body">
  <div class="csl-entry">Crutzen, P.J., and E.F. Stoermer. 2000. “The ‘Anthropocene.’” <i>Global Change Newsletter</i> 41: 17–18.</div>
</div>
```
