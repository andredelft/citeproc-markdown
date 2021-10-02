import re
import yaml
import json
import json5
import requests
from ratelimit import limits, sleep_and_retry
from markdown import Extension
from markdown.preprocessors import Preprocessor
import decouple

from requests.exceptions import HTTPError


class CiteprocConversionError(Exception):
    pass


@sleep_and_retry
@limits(
    calls=decouple.config('RATE_LIMIT_CALLS', default=5, cast=int),
    period=decouple.config('RATE_LIMIT_PERIOD', default=1, cast=int)
)
def format_bibliography(data, citation_style, citeproc_endpoint=None):
    """
    POST request to CITEPROC_ENDPOINT to format data as a bibliography in
    CITATION_STYLE.
    """

    if not citeproc_endpoint:
        raise ValueError('No citeproc endpoint defined')

    r = requests.post(
        citeproc_endpoint,
        json={'items': data},
        params={
            'style': citation_style,
            'responseformat': 'html'
        }
    )

    try:
        r.raise_for_status()
    except HTTPError:
        raise CiteprocConversionError(
            f'Citeproc endpoint returned HTTP {r.status_code} error: '
            + r.content.decode()
        )

    return r.content.decode()


class CSLYAMLPreprocessor(Preprocessor):

    LANGUAGE_PROCESSORS = {
        'yaml': {
            'loader': yaml.safe_load,
            'exception': yaml.YAMLError
        },
        'json': {
            'loader': json.loads,
            'exception': json.JSONDecodeError
        },
        'json5': {
            'loader': json5.loads,
            'exception': ValueError
        }
    }
    LANGUAGES = LANGUAGE_PROCESSORS.keys()

    RE_CSL_BLOCK = re.compile(
        fr'''
            (?P<fence>^(?:~{{3,}}|`{{3,}}))[ ]*  # opening fence
            csl-(?P<language>{"|".join(LANGUAGES)})  # data language
            \n                                  # newline (end of opening fence)
            (?P<data>.*?)(?<=\n)                # the bibliographic data
            (?P=fence)[ ]*$                     # closing fence
        ''',
        flags=re.MULTILINE | re.DOTALL | re.VERBOSE
    )

    def __init__(self, md, configs, **kwargs):
        super().__init__(md)
        self.configs = configs

    def _add_to_stash(self, m):
        language_processor = self.LANGUAGE_PROCESSORS[m['language']]

        try:
            data = language_processor['loader'](m['data'])

            styled_bibl = format_bibliography(
                data, citation_style=self.configs['citation_style'],
                citeproc_endpoint=self.configs['citeproc_endpoint']
            )
        except (CiteprocConversionError, language_processor['exception']) as e:
            if self.configs['surpress_errors']:
                return self._return_codeblock(m)
            else:
                raise e
        else:
            placeholder = self.md.htmlStash.store(styled_bibl)

        return placeholder

    def _return_codeblock(self, m):
        if self.configs['fenced_code_on_fail']:
            return "{fence}{language}\n{data}\n{fence}".format(**m.groupdict())
        else:
            return '\n'.join([f'    {line}' for line in m['data'].split('\n')])

    def run(self, lines):
        text = '\n'.join(lines)
        text = self.RE_CSL_BLOCK.sub(self._add_to_stash, text)
        return text.split('\n')


class CiteprocExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'citation_style': [
                'chicago-author-date',
                'Citation style that the bibliographies will be converted into.'
            ],
            'surpress_errors': [
                True,
                (
                    'Only return codeblock when an error is raised and '
                    'surpress the error.'
                )
            ],
            'fenced_code_on_fail': [
                False,
                (
                    'Format the returned codeblock according to the the '
                    'fenced_code markdown extension.'
                )
            ]
        }

        citeproc_help_text = 'Citeproc endpoint where the HTTP requests will go'

        try:
            self.config['citeproc_endpoint'] = [
                decouple.config('CITEPROC_ENDPOINT'),
                citeproc_help_text
            ]
        except decouple.UndefinedValueError:
            self.config['citeproc_endpoint'] = ['', citeproc_help_text]

        Extension.__init__(self, **kwargs)

    def extendMarkdown(self, md):
        configs = self.getConfigs()

        if not configs.get('citeproc_endpoint'):
            print(
                'Warning: no citeproc_endpoint is defined in the citeproc '
                'extension config or as environment variable '
                'CITEPROC_ENDPOINT, hence the citeproc extension '
                'processors will not be registered.'
            )
        else:
            md.registerExtension(self)
            md.preprocessors.register(
                CSLYAMLPreprocessor(md, configs),
                'csl_yaml', 26  # Before FencedBlockPreprocessor
            )
