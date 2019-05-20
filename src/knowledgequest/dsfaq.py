import re
import copy

import pandas as pd
import yaml

from nlpia import loaders

import logging
logger = logging.getLogger(__name__)


def dict_lines(d, indent=2):
    lines = []
    for k, v in d.items():
        lines.append(" " * indent + "{}: {}".format(k, yaml.dump(v).rstrip('\n').rstrip('.')))
    return lines


def collect_multiline_quotes(lines, eol='\n'):
    """ Take list of lines and concatenate tripple-quoted multiline strings.

    >>> s = "line0 = \"\"\"let's start line1\nline2\n\nline4\n\"\"\"\n"
    >>> lines = s.split('\n')
    >>> collect_multiline_quotes(lines)
    ['line0 = \"\"\"\nline1\n\nline3\n\"\"\"', '']
    >>> s = "line0 = \"\"\"let's have 2 tripple quotes\"\"\" and \"\"\"line1\nline2\n\nline4\n\"\"\"\n"
    >>> lines = s.split('\n')
    >>> collect_multiline_quotes(lines)
    """
    multiline = ''
    multilines = []
    quotechar = None
    for line in lines:
        line = line.rstrip()
        if quotechar:
            multiline += line + eol
            if line[-3:] == quotechar:
                quotechar = None
                multilines.append(multiline.rstrip(eol))
            elif line.endswith("'''") or line.endswith('"""'):
                logger.warn('Possibly improperly terminated multiline quote: {}'.format(multiline))
        else:
            for qc in ["'''", '"""']:
                if qc in line:
                    multiline = line + eol
                    # print('Started a fresh multiline quote: {}'.format(multiline))
                    quotechar = qc
                    break
            # if multiline quote started and ended within the same line, stop the quote:
            if quotechar and multiline.endswith(quotechar) and not (multiline.count(quotechar) % 2):
                multiline = multiline.replace(quotechar, quotechar + eol).rstrip()
                quotechar = None
            if not quotechar:
                multilines.append(line)
                multiline = ''
    return multilines


def clean_yaml(filename='dsfaq.yml', eol='\n'):
    """ FIXME: TEST || Attempts to return a valid yaml string with deduped dictionary keys

    Attempts to deal with multiple answers (duplicate keys) within a single dictionary for a FAQ item.
    """
    try:
        with open(filename, 'rt') as fin:
            lines = fin.read().splitlines()
    except IOError:
        lines = filename.splitlines()
    print(f'Loading {len(lines)} lines...')
    multilines = collect_multiline_quotes(lines, eol=eol)
    del lines
    clean_lines = []
    for i, multiline in enumerate(multilines):
        print(i)
        multiline = multiline.strip()
        multiline = escape_quotes(multiline)
        print(multiline)
        obj = yaml.load(multiline, Loader=yaml.loader.FullLoader)
        print(obj)
        print()
        print()
        d = {}
        if multiline.rstrip() == '-' or (isinstance(obj, list) and len(obj) <= 1 and obj[0] is None):
            if len(d):
                clean_lines.append('-')
                clean_lines.extend(dict_lines(d))
            else:
                d = {}
        elif isinstance(obj, dict) and len(obj) == 1 and list(obj.keys())[0] in d:
            newd = {}
            if len(d):
                newd = copy.deepcopy(d)
                clean_lines.append('-')
                clean_lines.extend(dict_lines(d))
            d = newd
            d.update(obj)
    return '\n'.join((multiline.rstrip('\n') for multiline in clean_lines))


def find_key_and_value(s):
    """ Find a double or single-quoted string at the end of a string (quote char must be last)

    >>> s = 'A: "Both. Start with the dataset, don\'t close the quote'
    >>> k, v = find_key_and_value(s)
    >>> k
    'A'
    >>> v
    '"Both. Start with the dataset, don\'t close the quote'
    """
    s = s.strip()
    match = re.match(r'([^:]+):\s*(.*)$', s)
    if match:
        return match.groups()
    return None, None


def find_prefix_and_quote(s):
    """ Find a double or single-quoted string at the end of a string (quote char must be last)

    >>> s = 'Q: "The conclusion to my capstone starts with "The above plots show feature importances." What do you think?"  \n'
    >>> prefix, quote = find_prefix_and_quote(s)
    >>> prefix
    'Q: '
    >>> quote[:40]
    '"The conclusion to my capstone starts wi'
    >>> quote[:70]
    '"The conclusion to my capstone starts with "The above plots show that '
    >>> find_prefix_and_quote("Don't stop. Move along. They've nothing to see here.")
    >>> find_prefix_and_quote('noquote: "Not a proper yaml quote! (quote char doesn't terminate the str)".')
    """
    s = s.strip()
    k, v = find_key_and_value(s)
    if not (k and v and isinstance(v, str)):
        return None, None
    quotechar = v[0]
    if quotechar in '"\'':
        if v[-1] != quotechar:
            v = v + quotechar
        return (k + ': ', v)
        # match = re.match(r'([^{quotechar}]*)({quotechar}.*{quotechar})$'.format(quotechar=quotechar), s)
        # return match.groups()
    return None, None


def escape_quotes(s):
    """ Within the quoted value string of a yaml key-value pair, escape any internal quote characters

    >>> s = 'Q: "The conclusion to my capstone starts with "The above plots show feature importances." What do you think?"  \n'
    >>> s2 = escape_quotes(s)
    >>> s2
    'Q: "The conclusion to my capstone starts with \\"The above plots show feature importances.\\" What do you think?"'
    >>> yaml.load(s2, Loader=yaml.loader.FullLoader)
    {'Q': 'The conclusion to my capstone starts with "The above plots show feature importances." What do you think?'}
    """
    prefix, quote = find_prefix_and_quote(s)
    if quote is None:
        return s
    quotechar = quote[-1]
    quote = quote[1:-1]
    # make this idempotent with a regex replace
    quote = quote.replace('\\' + quotechar, quotechar)
    quote = quote.replace('\\' + quotechar, quotechar)
    quote = quote.replace(quotechar, '\\' + quotechar)
    quote = quotechar + quote + quotechar
    print(prefix)
    print(quote)
    return ''.join([prefix, quote])


def load_yaml(filename='dsfaq.yml'):
    r""" Convert yaml to DataFrame

    FIXME: deal with multiple answers for one question

    >>> load_yaml('dsfaq.yml').head(3)
                                                    a                                                  q
    0  Personally I find it hard to know ahead of tim...  How to use chi squared test in feature selection?
    1  There are numerous cost/loss functions you can...  What's the benefits of using log loss vs accur...
    2  Like other pipeline design challenges, I do ou...  How to detect outliers in a data set and how t...
    """
    try:
        with open(filename, 'rt') as fin:
            lod = yaml.load(fin, Loader=yaml.loader.FullLoader)
    except IOError:
        lod = yaml.load(filename, Loader=yaml.loader.FullLoader)

    df = pd.DataFrame(lod)
    replacer_dict = dict(zip(df.columns, loaders.clean_columns(df.columns)))
    # clean_lod = []
    for i, d in enumerate(lod):
        newd = {}
        for k in d:
            newd[replacer_dict[k]] = d[k]
        lod[i] = newd
    return pd.DataFrame(lod)
