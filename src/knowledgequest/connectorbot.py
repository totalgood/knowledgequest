import os
import json
import praw
import time

for k, v in os.environ.items():
    if k.startswith('REDDIT_BOT_'):
        locals()[k] = v

SUBREDDIT_NAMES = ['space', 'science', 'python', 'books', 'Futurology', 'etymology', 'learnmachinelearning', 'learnpython',
    'todayilearned', 'rust', 'chemistry', '3Blue1Brown', 'academia', 'atheism', 'agi', 'AcademicPsychology', 'aiclass', 'algorithms', 
    'algotrading', 'androiddev', 'anonymous', 'Art', 'AskAcademia', 'AskNetsec', 'askscience', 'bbc', 'BBCNEWS', 'BioAGI', 'bioinformatics',
    'booksuggestions', 'California', 'canada', 'CanadianAI', 'cellular_automata', 'cogneuro', 'cogsci', 'compneuroscience', 'conlangs',
    'Crypto_Currency_News', 'CS224n', 'CSEducation', 'data', 'datasets', 'datascience', 'DataScienceGuide', 'datasciencenews', 'DataScienceSimplified',
    'DataScienceTech', 'DeepBrainChain', 'deeplearning', 'DepthHub', 'DistributedApps', 'DistributedComputing', 'EarhPorn', 'django', 'ECE', 'Economics',
    'economy', 'nlp', 'nlpbot']


REDDIT_BOT_NAME = os.environ['REDDIT_BOT_NAME']
REDDIT_BOT_CLIENT_ID = os.environ['REDDIT_BOT_CLIENT_ID']
REDDIT_BOT_SECRET = os.environ['REDDIT_BOT_SECRET']
REDDIT_BOT_UN = os.environ['REDDIT_BOT_UN']
REDDIT_BOT_PW = os.environ['REDDIT_BOT_PW']

MAX_COMMENTS = 99

if __name__ == '__main__':
    bot = praw.Reddit(user_agent=f'{REDDIT_BOT_NAME} v0.0.1',
                      client_id=f'{REDDIT_BOT_CLIENT_ID}',
                      client_secret=f'{REDDIT_BOT_SECRET}',
                      user_name=f'{REDDIT_BOT_UN}',
                      password=f'{REDDIT_BOT_PW}')
    while True:
        for subname in SUBREDDIT_NAMES:
            try:
                subreddit = bot.subreddit(subname)
                print(f'Subscribed to {subname}')
                comments = subreddit.stream.comments()
            except:
                print(f'Unable to subscribe to {subname}')
            records = []
            for i, c in enumerate(comments):
                c.author_fullname = getattr(c, 'author_fullname', '') 
                print(f'Retrieved {i}:{c.author_fullname}: {c.body[:60]}')
                records.append(dict((k,v) for (k, v) in c.__dict__.items() if 
                        not k.startswith('_') and 
                        isinstance(v, (str, int, bool, float, list, tuple, dict))))
                if len(records) >= MAX_COMMENTS:
                    break
            with open(f'connectorbot_{subname}.json', 'at') as fout:
                fout.write(json.dumps(records, indent=2))
        time.sleep(10*60)

"""
for comment in comments:
    break
>> comment
{'_mod': None,
 '_replies': [],
 '_submission': None,
 '_reddit': <praw.reddit.Reddit at 0x10edd9ac8>,
 'subreddit_id': 't5_mouw',
 'approved_at_utc': None,
 'edited': False,
 'mod_reason_by': None,
 'banned_by': None,
 'author_flair_type': 'text',
 'removal_reason': None,
 'link_id': 't3_an9xgr',
 'author_flair_template_id': None,
 'likes': None,
 'user_reports': [],
 'saved': False,
 'id': 'efrtbwg',
 'banned_at_utc': None,
 'mod_reason_title': None,
 'gilded': 0,
 'archived': False,
 'no_follow': False,
 'author': Redditor(name='Ach4t1us'),
 'num_comments': 7,
 'can_mod_post': False,
 'send_replies': True,
 'parent_id': 't3_an9xgr',
 'score': 1,
 'author_fullname': 't2_9lf9z',
 'over_18': False,
 'approved_by': None,
 'mod_note': None,
 'controversiality': 0,
 'body': 'Shitting bricks is real, sorry',
 'link_title': 'Researchers in Australia have discovered a way to bake bio-solid bricks out of human waste, solving several environmental issues all while meeting safety standards.',
 'downs': 0,
 'author_flair_css_class': None,
 'name': 't1_efrtbwg',
 'author_patreon_flair': False,
 'collapsed': False,
 'author_flair_richtext': [],
 'is_submitter': False,
 'body_html': '<div class="md"><p>Shitting bricks is real, sorry</p>\n</div>',
 'gildings': {'gid_1': 0, 'gid_2': 0, 'gid_3': 0},
 'collapsed_reason': None,
 'stickied': False,
 'can_gild': True,
 'subreddit': Subreddit(display_name='science'),
 'author_flair_text_color': None,
 'score_hidden': True,
 'permalink': '/r/science/comments/an9xgr/researchers_in_australia_have_discovered_a_way_to/efrtbwg/',
 'num_reports': None,
 'link_permalink': 'https://www.reddit.com/r/science/comments/an9xgr/researchers_in_australia_have_discovered_a_way_to/',
 'report_reasons': None,
 'link_author': 'jacker494',
 'author_flair_text': None,
 'link_url': 'https://www.smithsonianmag.com/smart-news/flushing-toilet-first-step-making-these-better-bricks-180971408/',
 'created': 1549365885.0,
 'created_utc': 1549337085.0,
 'subreddit_name_prefixed': 'r/science',
 'distinguished': None,
 'author_flair_background_color': None,
 'mod_reports': [],
 'quarantine': False,
 'subreddit_type': 'public',
 'ups': 1,
 '_fetched': True,
 '_info_params': {}}

>> print(json.dumps(dict((k,v) for (k, v) in comment.__dict__.items() if 
                         not k.startswith('_') and 
                         isinstance(v, (str, int, bool, float, list, tuple, dict))), indent=2))                                                                                                
{
  "subreddit_id": "t5_mouw",
  "edited": false,
  "author_flair_type": "text",
  "link_id": "t3_an9xgr",
  "user_reports": [],
  "saved": false,
  "id": "efrtbwg",
  "gilded": 0,
  "archived": false,
  "no_follow": false,
  "num_comments": 7,
  "can_mod_post": false,
  "send_replies": true,
  "parent_id": "t3_an9xgr",
  "score": 1,
  "author_fullname": "t2_9lf9z",
  "over_18": false,
  "controversiality": 0,
  "body": "Shitting bricks is real, sorry",
  "link_title": "Researchers in Australia have discovered a way to bake bio-solid bricks out of human waste, solving several environmental issues all while meeting safety standards.",
  "downs": 0,
  "name": "t1_efrtbwg",
  "author_patreon_flair": false,
  "collapsed": false,
  "author_flair_richtext": [],
  "is_submitter": false,
  "body_html": "<div class=\"md\"><p>Shitting bricks is real, sorry</p>\n</div>",
  "gildings": {
    "gid_1": 0,
    "gid_2": 0,
    "gid_3": 0
  },
  "stickied": false,
  "can_gild": true,
  "score_hidden": true,
  "permalink": "/r/science/comments/an9xgr/researchers_in_australia_have_discovered_a_way_to/efrtbwg/",
  "link_permalink": "https://www.reddit.com/r/science/comments/an9xgr/researchers_in_australia_have_discovered_a_way_to/",
  "link_author": "jacker494",
  "link_url": "https://www.smithsonianmag.com/smart-news/flushing-toilet-first-step-making-these-better-bricks-180971408/",
  "created": 1549365885.0,
  "created_utc": 1549337085.0,
  "subreddit_name_prefixed": "r/science",
  "mod_reports": [],
  "quarantine": false,
  "subreddit_type": "public",
  "ups": 1
}
"""

