# Generated by Django 3.2.5 on 2021-08-21 19:49

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20210811_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='has_sizes',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('XS', 'X-Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'X-Large')], max_length=11, null=True),
        ),
    ]
