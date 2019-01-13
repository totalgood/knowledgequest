import sys
import time

import pandas as pd
from stackauth import StackAuth
from stackexchange import Site, StackOverflow


def get_accounts(user_id=623735, total=20, sleep=3.14, **kwargs):
    stack_auth = StackAuth()
    so = Site(StackOverflow)
    accounts = stack_auth.associated(so, user_id)
    reputation = {}
    
    for account in accounts:
        print('  %s: %s / %d reputation' % ('hobs', account.on_site.name, account.reputation))

        reputation[account.reputation] = account.on_site.name

    print('Most reputation on: %s' % reputation[max(reputation)])
    return 


def get_questions(total=20, sleep=3.14, **kwargs):
    so = StackOverflow()
    defaults = dict(pagesize=10) 
    defaults.update(kwargs)
    questions = []
    while len(questions) < total:
        for q in so.questions(**defaults):
            print(vars(q))
            print(q.title)
            questions.append(q.__dict__)
        time.sleep(sleep)
    return pd.DataFrame(questions)


if __name__ == '__main__':
    user_id = 623735 if len(sys.argv) < 2 else int(sys.argv[1])
    # print('Using stackOverflow user %d\'s accounts:' % user_id)
