from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from core.models import Producer, ProductImages, Product, Category


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'get_logo')
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'description',)
    list_filter = ('user', 'created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('get_logo',)

    @admin.display(description=_('Logo'))
    def get_logo(self, producer):
        if producer.logo:
            return mark_safe(
                f'<img src="{producer.logo.url}" alt="{producer.name}" width="100px" />')
        return '-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('-created_at',)


class ProductImagesTabularInline(admin.TabularInline):
    model = ProductImages
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'producer', 'is_published', 'get_image')
    list_display_links = ('id', 'name',)
    list_editable = ('is_published',)
    search_fields = ('name', 'content',)
    list_filter = ('producer', 'rating', 'created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('get_image',)
    inlines = (ProductImagesTabularInline,)

    @admin.display(description=_('Image'))
    def get_image(self, product):
        if product.image:
            return mark_safe(
                f'<img src="{product.image.url}" alt="{product.name}" width="100px" />')
        return '-'

# Register your models here.
