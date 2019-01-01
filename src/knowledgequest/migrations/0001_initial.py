# Generated by Django 2.1.4 on 2018-12-31 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, null=True)),
                ('emailid', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'address',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i', models.BigIntegerField(blank=True, null=True)),
                ('j', models.BigIntegerField(blank=True, null=True)),
                ('server', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('from_field', models.TextField(blank=True, db_column='from', null=True)),
                ('to', models.TextField(blank=True, null=True)),
                ('bcc', models.TextField(blank=True, null=True)),
                ('cc', models.TextField(blank=True, null=True)),
                ('attendees', models.TextField(blank=True, null=True)),
                ('content_transfer_encoding', models.TextField(blank=True, null=True)),
                ('content_type', models.TextField(blank=True, null=True)),
                ('date', models.TextField(blank=True, null=True)),
                ('mime_version', models.TextField(blank=True, null=True)),
                ('re', models.TextField(blank=True, null=True)),
                ('subject', models.TextField(blank=True, null=True)),
                ('time', models.TextField(blank=True, null=True)),
                ('x_filename', models.TextField(blank=True, null=True)),
                ('x_folder', models.TextField(blank=True, null=True)),
                ('x_from', models.TextField(blank=True, null=True)),
                ('x_origin', models.TextField(blank=True, null=True)),
                ('x_to', models.TextField(blank=True, null=True)),
                ('x_bcc', models.TextField(blank=True, null=True)),
                ('x_cc', models.TextField(blank=True, null=True)),
                ('charset', models.TextField(blank=True, null=True)),
                ('default_type', models.TextField(blank=True, null=True)),
                ('defects', models.TextField(blank=True, null=True)),
                ('epilogue', models.TextField(blank=True, null=True)),
                ('folder', models.TextField(blank=True, null=True)),
                ('payload', models.TextField(blank=True, null=True)),
                ('policy', models.TextField(blank=True, null=True)),
                ('preamble', models.TextField(blank=True, null=True)),
                ('unixfrom', models.TextField(blank=True, null=True)),
                ('user', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'email',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('FR', 'from'), ('TO', 'to'), ('CC', 'CC'), ('BC', 'BCC')], max_length=2)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledgequest.Address')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledgequest.Email')),
            ],
        ),
        migrations.AddField(
            model_name='email',
            name='participants',
            field=models.ManyToManyField(through='knowledgequest.Participant', to='knowledgequest.Address'),
        ),
    ]