import sys
import time

import pandas as pd
from stackauth import StackAuth
import stackexchange as se
# from stackexchange import Site, StackOverflow

DEFAULT_USER_ID = 623735  # hobs
DEFAULT_SITE = 'stackoverflow'
IGNORE_FIELDS = set(['json', 'json_ob', 'site'])


def get_site(site=DEFAULT_SITE, user_id=DEFAULT_USER_ID):
    return se.Site(site.lower().strip()) if isinstance(site, str) else site


def get_accounts(total=20, site='stackoverflow', user_id=None):
    site = get_site(site)
    user_id = user_id or DEFAULT_USER_ID
    stack_auth = StackAuth()
    accounts = stack_auth.associated(site, user_id)
    reputation = {}
    
    for account in accounts:
        # print('  %s: %s / %d reputation' % ('hobs', account.on_site.name, account.reputation))

        reputation[account.reputation] = account.on_site.name

    print('Most reputation on: %s' % reputation[max(reputation)])
    return pd.DataFrame(sorted(reputation.items(), reverse=True), columns='reputation site'.split())


def good_vars(obj):
    return dict([(k, v) for k, v in vars(obj).items() if not k.startswith('_') and not k in IGNORE_FIELDS])


def good_dict(d):
    good = {}
    if hasattr(d, 'keys') and callable(d.keys):
        for k in d.keys():
            if not isinstance(k, (str, int, float)):
                continue
            v = d[k]
            if isinstance(v, (str, int, float)) or v is None:
                good[k] = v 
            elif isinstance(v, (tuple, list)):
                good[k] = tuple([good_dict(obj) for obj in v])
            elif isinstance(v, dict):
                good[k] = good_dict(v)
            elif hasattr(v, 'fetch'):
                good[k] = tuple([good_dict(obj) for obj in v])
    else:
        good = d
    return good


def fetch_related():
    """ Need a function to automatically fetch or empty "<unfetched sequence: Comment>" "<unfetched sequence: PostRevision>" etc """
    pass


def get_site(site=DEFAULT_SITE, user_id=DEFAULT_USER_ID):
    return se.Site(site.lower().strip()) if isinstance(site, str) else site


def get_questions(total=10, site='stackoverflow', sleep=3.14, **kwargs):
    stack_auth = StackAuth()
    site = se.Site(site.lower().strip()) if isinstance(site, str) else site
    defaults = dict(pagesize=10, body=True, comments=True) 
    defaults.update(kwargs)
    questions = []
    answers = []
    for q in site.questions(**defaults):
        print(q.title)
        qdict = good_vars(q)
        for k in qdict.keys():
            obj = qdict[k]
            if hasattr(obj, 'fetch') and callable(obj.fetch):
                obj = tuple(list(obj.fetch() or []))
                if obj:
                    qdict[k] = tuple([good_vars(v) if hasattr(v, '__dict__') else v for v in obj])
            elif isinstance(obj, list):
                qdict[k] = tuple([good_vars(v) if hasattr(v, '__dict__') else v for v in obj])
        qans = list(qdict.pop('answers', []))
        qdict['answers'] = [ans['id'] for ans in qans]
        qdict['accepted_answer'] = [ans['id'] for ans in qans if ans['is_accepted']]
        qdict['accepted_answer'] = qdict['accepted_answer'][0] if qdict['accepted_answer'] else None
        answers.extend(qans)
        questions.append(qdict)
        if len(questions) >= total:
            break
        if not len(questions) % defaults['pagesize']:
            print('Sleeping for {} seconds'.format(sleep))
            time.sleep(sleep)
    return questions, answers


if __name__ == '__main__':
    if len(sys.argv) > 1:
        total = int(sys.argv[1])
        accounts = get_accounts()
        questions, answers = get_questions(total=total)
        answers = pd.DataFrame(answers)
        answers.to_csv('answers.csv')
        questions = pd.DataFrame(questions)
        questions.to_csv('questions.csv')

    # print(get_questions())
    # print('Using stackOverflow user %d\'s accounts:' % user_id)
