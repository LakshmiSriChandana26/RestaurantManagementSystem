# Generated by Django 5.0.2 on 2024-02-20 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_fooditem_restaurant_reviews_tablereservation_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='cart',
        ),
        migrations.AddField(
            model_name='payments',
            name='carts',
            field=models.ManyToManyField(blank=True, related_name='related_%(class)s', to='user.cart'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('deleted', 'Deleted')], default='pending', max_length=100),
        ),
    ]
