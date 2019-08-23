# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import os
import keyword
import json
import re
import logging

from tqdm import tqdm
import sqlite3
import yaml
import numpy as np

from django.db import models
from django.contrib.postgres.fields import ArrayField

from knowledgequest.constants import DATA_DIR, NLP

log = logging.getLogger(__name__)
PYTHON_KEYWORDS = set(keyword.kwlist)
PARTICIPANT_CHOICES = (
    ('FR', 'from'),
    ('TO', 'to'),
    ('CC', 'CC'),
    ('BC', 'BCC'),
)


class Address(models.Model):
    # id = models.AutoField(primary_key=True)

    address = models.TextField(blank=True, null=True)
    emailid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'knowledgequest'


class Email(models.Model):
    # id = models.AutoField(primary_key=True)

    # emailid: i.j.server.name
    i = models.BigIntegerField(blank=True, null=True)
    j = models.BigIntegerField(blank=True, null=True)
    server = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    participants = models.ManyToManyField(Address, through='Participant')
    # denormalized raw text from e-mail headers
    from_field = models.TextField(db_column='from', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    to = models.TextField(blank=True, null=True)
    bcc = models.TextField(blank=True, null=True)
    cc = models.TextField(blank=True, null=True)
    attendees = models.TextField(blank=True, null=True)

    content_transfer_encoding = models.TextField(blank=True, null=True)
    content_type = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    mime_version = models.TextField(blank=True, null=True)
    re = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    x_filename = models.TextField(blank=True, null=True)
    x_folder = models.TextField(blank=True, null=True)
    x_from = models.TextField(blank=True, null=True)
    x_origin = models.TextField(blank=True, null=True)
    x_to = models.TextField(blank=True, null=True)
    x_bcc = models.TextField(blank=True, null=True)
    x_cc = models.TextField(blank=True, null=True)
    charset = models.TextField(blank=True, null=True)
    default_type = models.TextField(blank=True, null=True)
    defects = models.TextField(blank=True, null=True)
    epilogue = models.TextField(blank=True, null=True)
    folder = models.TextField(blank=True, null=True)
    payload = models.TextField(blank=True, null=True)
    policy = models.TextField(blank=True, null=True)
    preamble = models.TextField(blank=True, null=True)
    unixfrom = models.TextField(blank=True, null=True)
    user = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'knowledgequest'

# TODO: Delete Reply table to normalize DB so that we only have a single Statement table
#       Create a Conversation DAG (directional graph)


class Reply(models.Model):
    text = models.TextField()
    usevec = ArrayField(base_field=models.FloatField(), size=512)
    docvec = ArrayField(base_field=models.FloatField(), size=300)

    class Meta:
        app_label = 'knowledgequest'


class Statement(models.Model):
    text = models.TextField()
    usevec = ArrayField(base_field=models.FloatField(), null=True, blank=True, size=512)
    docvec = ArrayField(base_field=models.FloatField(), null=True, blank=True, size=300)
    replies = models.ManyToManyField(Reply, through='Option')

    class Meta:
        app_label = 'knowledgequest'


class Option(models.Model):
    statement = models.ForeignKey(Statement, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    probability = models.FloatField()

    class Meta:
        app_label = 'knowledgequest'


class Participant(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    name = models.TextField(null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    kind = models.CharField(max_length=2, choices=PARTICIPANT_CHOICES)
    statements = models.ManyToManyField('Statement', blank=True)
    replies = models.ManyToManyField('Reply', blank=True)

    class Meta:
        app_label = 'knowledgequest'


def load_faq(faq_path=os.path.join(DATA_DIR, 'dsfaq_plus_faq_data_science_and_machine_learning.yml')):
    faq = None
    with open(faq_path, 'r') as instream:
        try:
            faq = yaml.safe_load(instream)
        except yaml.YAMLError as e:
            print(e)
            raise(e)
    for i, qa in enumerate(faq):
        if not isinstance(qa, dict):
            faq[i] = {}
            log.warning(f'qa #{i} was not a dict')
            continue
        for k in qa:
            if k.lower() != k:
                qa[k.lower()] = qa.pop(k)
        # if 'q' not in qa:
        #     log.warning(f'qa #{i} had no Question: {list(qa)} {qa[list(qa)[0]]}')
        #     qa['q'] = qa.pop('q_student', qa.pop('q_student2', qa.pop('q_teacher')))
        # if 'a' not in qa:
        #     log.warning(f'qa #{i} had no Answer: {list(qa)} {qa[list(qa)[0]]}')
        #     qa['a'] = qa.pop('a_teacher', qa.pop('a_teacher2', qa.pop('a_student')))
        #     continue

    return faq


def create_from_sqlite(
        path='/home/hobs/src/springboard/tannistha/enron_email.db',
        tables='Email Address'.split(),
        batch_size=999):
    with sqlite3.connect('/home/hobs/src/springboard/tannistha/enron_email.db') as con:
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()
        print("SQLite version: %s" % data)

        for table_name in tables:
            model = globals()[table_name]
            print(model)
            cur.execute('PRAGMA table_info({})'.format(table_name.lower()))
            rows = cur.fetchall()
            fields = [row[1] for row in rows]
            print('sqfields: ', fields)
            cur2 = con.cursor()
            # count = cur2.execute('select count(id) from {}'.format(table_name)).scalar()
            cur2 = con.cursor()
            cur2.execute('SELECT * FROM {}'.format(table_name.lower()))
            rows = cur2.fetchall()

            batch = []
            for i, row in tqdm(enumerate(rows), total=len(rows)):
                djfields = [(s.lower() + '_field' if s in PYTHON_KEYWORDS else s.lower()) for s in fields]
                if not i:
                    print('djfields: ', djfields)
                record = zip(djfields, row)
                record = dict([(djfield, value) for (djfield, value, sqfield) in zip(djfields, row, fields) if hasattr(model, djfield)])
                obj = model(**record)
                if not ((i + 1) % batch_size):
                    results = model.objects.bulk_create(batch, batch_size=batch_size)
                    batch = []
                batch.append(obj)
    return results


SENTENCE_SPEC_PATH = os.path.join(DATA_DIR, 'medical_sentences.json')
SENTENCE_SPEC = json.load(open(SENTENCE_SPEC_PATH, 'r'))


def generate_sentence(spec=SENTENCE_SPEC, sentence_id=None):
    """ Generate random sentence using word probabilities specified in SENTENCE_SPEC

    >>> spec = {
    ...     "answers":[[{"HDL":0.95,"good_cholesterol":0.05}, {"150": 0.01,"145": 0.01,"unk": 0.98}],
    ...     "sentences":["Patient LDL level is 100, ________ level is 50, and the total is ______ .",]
    ...     }
    >>> s = generate_sentence(spec=spec, sentence_id=0)  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    >>> s
    'Patient LDL level is 100, ... level is 50, and the total is ... .'
    >>> s[26:42] in ('HDL level is 50,', 'good_cholesterol')
    True
    >>> s[60:63] in ('150', '145', 'unk')
    True
    """
    sentences = spec['sentences']
    if sentence_id is None:
        sentence_id = np.random.randint(0, len(sentences))
    sentence = sentences[sentence_id]
    answer = spec['answers'][sentence_id]
    i_unk = 0
    tokens = []
    for i, tok in enumerate(NLP(sentence)):
        if re.match(r'^(_+|unk|\[MASK\])$', tok.text):
            possible_tokens, p = list(zip(*answer[i_unk].items()))
            tokens.append(np.random.choice(a=possible_tokens, p=p))
            i_unk += 1
