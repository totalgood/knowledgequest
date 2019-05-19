import yaml
from nlpia import loaders
import pandas as pd
import copy


def dict_lines(d, indent=2):
    lines = []
    for k, v in d.items():
        lines.append(" "*indent + "{}: {}".format(k, yaml.dump(v).rstrip('\n').rstrip('.')))
    return lines


def clean_yaml(filename='dsfaq.yml'):
    """ FIXME: TEST || Attempts to return a valid yaml string with deduped dictionary keys

    Attempts to deal with multiple answers (duplicate keys) within a single dictionary for a FAQ item.
    """
    try:
        with open(filename, 'rt') as fin:
            lines = load(fin).splitlines()
    except IOError:
        lines = filename.splitlines()
    clean_lines = []
    for i, line in enumerate(open('dsfaq.yml', 'rt')):
        print(i)
        print(line.strip())
        obj = yaml.load(line.strip())
        print(obj)
        print()
        print()
        d = {}
        if line.rstrip() == '-' or (isinstance(obj, list) and len(obj) <= 1 and obj[0] is None):
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
        return '\n'.join((line.rstrip('\n') for line in clean_lines))


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
            lod = yaml.load(fin)
    except IOError:
        lod = yaml.load(filename)

    df = pd.DataFrame(lod)
    replacer_dict = dict(zip(df.columns, loaders.clean_columns(df.columns)))
    # clean_lod = []
    for i, d in enumerate(lod):
        newd = {}
        for k in d:
            newd[replacer_dict[k]] = d[k]
        lod[i] = newd
    return pd.DataFrame(lod)
