from django.db import models

# ─────────────────────────────
# 1. หมวดหลัก (เช่น เครนพับรถบรรทุก / ปั๊มไฮดรอลิค)
# ─────────────────────────────
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='หมวดสินค้า')

    class Meta:
        verbose_name_plural = "หมวดสินค้า (Category)"

    def __str__(self):
        return self.name

# ─────────────────────────────
# 2. หมวดย่อย (เช่น Fassi / Hiab / Palfinger)
# ─────────────────────────────
class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='หมวดหลัก')
    name = models.CharField(max_length=100, verbose_name='หมวดย่อย / แบรนด์')

    class Meta:
        verbose_name_plural = "หมวดย่อย (SubCategory)"

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
# ─────────────────────────────
# 3. สินค้า (Product)
# ─────────────────────────────
class Product(models.Model):
    category = models.ForeignKey(
        'Category', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products_direct'
        )
    subcategory = models.ForeignKey(
        'SubCategory', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
        )
    name = models.CharField(max_length=200, verbose_name='ชื่อสินค้า')
    brand = models.CharField(max_length=200, null=True, blank=True, verbose_name='ยี่ห้อ')
    description = models.TextField(blank=True, verbose_name='รายละเอียดสินค้า')
    price = models.CharField(max_length=50, null=True, blank=True, verbose_name='ราคา')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='รูปสินค้า')

    def __str__(self): return f"{self.product.name} image"

    def save(self, *args, **kwargs):
        # ถ้ามี subcategory แต่ยังไม่มี category → ตั้ง category อัตโนมัติ
        if self.subcategory and not self.category:
         self.category = self.subcategory.category
        super().save(*args, **kwargs)
    
    
    class Meta:
        verbose_name_plural = "สินค้า (Product)"
        ordering = ['subcategory', 'name']

    def __str__(self):
        return self.name
    

# ---------- 2. ProductImage Model (ใหม่) ----------
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        null=True, blank=True
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    alt = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return f"Image of {self.product.name if self.product else 'No Product'}"
    
class VehicleType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    class Meta:
        ordering = ["sort_order","name"]
        verbose_name = "ขนาดรถ"
        verbose_name_plural = "ขนาดรถ (Vehicle size )"
        def __str__(self):
         return f"{self.code} - {self.name}"
class Usage(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="ประเภทการใช้งาน")
    class Meta:
        verbose_name_plural = "ประเภทการใช้งาน (Usage)"
    def __str__(self):
        return self.name

# --- สเปคของสินค้า (ปรับให้เลือกได้หลายค่า) ---
class ProductSpec(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='specs', verbose_name='สินค้า')

    vehicle_types_rel = models.ManyToManyField(VehicleType,blank=True, verbose_name='ขนาดรถที่รองรับ')
    usages = models.ManyToManyField(Usage,blank=True, verbose_name='ประเภทการใช้งาน')

    class Meta:
        verbose_name_plural = "สเปคสินค้า (Product Spec)"

    def __str__(self):
        return self.product.name

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject or 'ไม่มีหัวข้อ'}"

