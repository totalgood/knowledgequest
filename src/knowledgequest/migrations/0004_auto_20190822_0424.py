# Generated by Django 2.2.4 on 2019-08-22 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgequest', '0003_auto_20190822_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='replies',
            field=models.ManyToManyField(blank=True, to='knowledgequest.Reply'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='statements',
            field=models.ManyToManyField(blank=True, to='knowledgequest.Statement'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='replies',
            field=models.ManyToManyField(through='knowledgequest.Option', to='knowledgequest.Reply'),
        ),
    ]
