from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from django.core.validators import MaxValueValidator, MinValueValidator

from account.models import User


class TimeStampAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('дата добавление'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('дата изменения'))

    class Meta:
        abstract = True


class Producer(TimeStampAbstract):
    class Meta:
        verbose_name = _('producer')
        verbose_name_plural = _('producers')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('name of the consumer'), unique=True, max_length=250)
    logo = ResizedImageField(upload_to='producers_logo/', force_format='WEBP',
                             quality=90, verbose_name=_('logo'), null=True, blank=True)
    description = models.TextField(_('description'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'), related_name='producer')

    def __str__(self):
        return f'{self.name} - {self.user}'


class Category(TimeStampAbstract):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('name of category'), unique=True, max_length=250)

    def __str__(self):
        return f'{self.name}'


class Product(TimeStampAbstract):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('-created_at', '-updated_at')

    name = models.CharField(_('name of product'), max_length=250)
    content = models.TextField(_('content'))
    rating = models.IntegerField(_('rating'), validators=[MinValueValidator(1), MaxValueValidator(5)], default=4)
    producer = models.ForeignKey(Producer, on_delete=models.PROTECT, related_name='products', verbose_name=_('producer'))
    is_published = models.BooleanField(_('Is published'), default=True)
    price = models.DecimalField(_('price'), decimal_places=1, max_digits=6, default=0.0)

    @property
    def image(self):
        return self.images.first()

    def __str__(self):
        return f'{self.name}'


class ProductImages(TimeStampAbstract):
    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')
        ordering = ('-created_at', '-updated_at')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'), related_name='images')
    image = ResizedImageField(upload_to='product_images/', force_format='WEBP', quality=90, verbose_name=_('image'))

# Create your models here.
