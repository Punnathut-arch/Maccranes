from django import forms
from django.contrib import admin
from .models import (
    Category, SubCategory, Product, ProductImage, Usage, ProductSpec,VehicleType,ContactMessage
)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

class VehicleTypeM2MField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.code} — {obj.name}"

class ProductSpecForm(forms.ModelForm):
    vehicle_types_rel =VehicleTypeM2MField(
        queryset=VehicleType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="ขนาดรถ"
    )
    usages = forms.ModelMultipleChoiceField(
        queryset=Usage.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="ประเภทการใช้งาน"
    )

    class Meta:
        model = ProductSpec
        fields = ("product", "vehicle_types_rel", "usages")
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5
    # ---------- INLINE ---------- #
class ProductSpecInline(admin.StackedInline):
    model = ProductSpec
    form = ProductSpecForm   # ✅ เพิ่มบรรทัดนี้
    extra = 0
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline,ProductSpecInline] 
    list_display = ('name', 'brand', 'subcategory', 'price')
    list_filter = (
    ('category', admin.RelatedOnlyFieldListFilter),    # ← ใช้ category ตรง ๆ
    ('subcategory', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('name',)
@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProductSpec)
class ProductSpecAdmin(admin.ModelAdmin):
    form = ProductSpecForm
    list_display = ("product", "get_vehicle_types", "get_usages")
    filter_horizontal = ("usages",)

    def get_vehicle_types(self, obj):
        return ", ".join(obj.vehicle_types_rel.values_list('name', flat=True))
    get_vehicle_types.short_description = "ขนาดรถที่รองรับ"

    def get_usages(self, obj):
        return ", ".join(obj.usages.values_list("name", flat=True))
    get_usages.short_description = "ประเภทการใช้งาน"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    list_filter = ("created_at",)


