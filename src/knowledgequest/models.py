# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from tqdm import tqdm
import sqlite3
import keyword

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


class Participant(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    kind = models.CharField(max_length=2, choices=PARTICIPANT_CHOICES)

    class Meta:
        app_label = 'knowledgequest'


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
            count = cur2.execute('select count(id) from {}'.format(table_name)).scalar()
            cur2 = con.cursor()
            cur2.execute('SELECT * FROM {}'.format(table_name.lower()))
            rows = cur2.fetchall()

            batch = []
            for i, row in tqdm(enumerate(rows), total=total):
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
