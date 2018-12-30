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
keywords = set(keyword.kwlist)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.TextField(blank=True, null=True)
    emailid = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'address'
        app_label = 'knowledgequest'


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    i = models.BigIntegerField(blank=True, null=True)
    j = models.BigIntegerField(blank=True, null=True)
    server = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    attendees = models.TextField(blank=True, null=True)
    bcc = models.TextField(blank=True, null=True)
    cc = models.TextField(blank=True, null=True)
    content_transfer_encoding = models.TextField(blank=True, null=True)
    content_type = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    from_field = models.TextField(db_column='from', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    mime_version = models.TextField(blank=True, null=True)
    re = models.TextField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    to = models.TextField(blank=True, null=True)
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
        managed = True
        db_table = 'email'
        app_label = 'knowledgequest'


def create_from_sqlite(path='/home/hobs/src/springboard/tannistha/enron_email.db', tables='Email Address'.split()):
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
            cur2.execute('SELECT * FROM {}'.format(table_name.lower()))
            rows = cur2.fetchall()
            for i, row in tqdm(enumerate(rows)):
                djfields = [(s.lower() + '_field' if s in keywords else s.lower()) for s in fields]
                if not i:
                    print('djfields: ', djfields)
                record = zip(djfields, row)
                record = dict([(djfield, value) for (djfield, value, sqfield) in zip(djfields, row, fields) if hasattr(model, djfield)])
                results = model.objects.get_or_create(**record)
    

