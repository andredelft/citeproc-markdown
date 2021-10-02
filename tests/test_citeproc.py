import pytest
from markdown import markdown
from pathlib import Path

FILE_DIR = Path(__file__).parent
OUTPUT_DIR = FILE_DIR / 'output'

# Ensure OUTPUT_DIR exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture
def csl_blocks():
    with open(FILE_DIR / 'csl-blocks.md') as f:
        return f.read()


@pytest.fixture
def malformed_csl_blocks():
    with open(FILE_DIR / 'malformed-csl-blocks.md') as f:
        return f.read()


def test_citeproc(csl_blocks, malformed_csl_blocks):
    html = markdown(
        csl_blocks,
        extensions=['citeproc'],
        extension_configs={
            'citeproc': {'surpress_errors': False}
        }
    )
    with open(OUTPUT_DIR / 'citeproc.html', 'w') as f:
        f.write(html)

    # Malformed CSL block
    html = markdown(
        malformed_csl_blocks,
        extensions=['citeproc']
    )
    with open(OUTPUT_DIR / 'malformed-citeproc.html', 'w') as f:
        f.write(html)

    # Malformed CSL block (fenced code return)
    html = markdown(
        malformed_csl_blocks,
        extensions=['citeproc', 'fenced_code'],
        extension_configs={
            'citeproc': {'fenced_code_on_fail': True}
        }
    )
    with open(OUTPUT_DIR / 'malformed-citeproc-fc.html', 'w') as f:
        f.write(html)
