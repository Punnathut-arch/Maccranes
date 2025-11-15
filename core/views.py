from django.shortcuts import render, get_object_or_404 ,redirect
from django.db.models import Prefetch
from .models import Category, Product, ProductSpec, Usage,VehicleType,ContactMessage
def home(request):
    return render(request, 'home.html')
def knowledge(request):
    return render(request, 'knowledge.html')
def contact(request):
    return render(request, 'contact.html')

def product(request):
    categories = Category.objects.prefetch_related(
        Prefetch(
            'products_direct',
        queryset=Product.objects.filter(subcategory__isnull=True)
        ),
        'subcategories__products'
    ).all()
    
    # --- รับค่าฟิลเตอร์ ---
    selected_vehicles = request.GET.getlist("vehicle")          # ex. ["4B","6B"]
    selected_usages_raw = request.GET.getlist("usage")          # ex. ["1","3"]
    selected_usages = [int(x) for x in selected_usages_raw]     # ✅ แปลงเป็น int
    has_filters = bool(selected_vehicles or selected_usages)  # ✅ เลือกอะไรสักอย่างหรือยัง

    # --- base queryset ---
    products = (
        Product.objects.all()
        .prefetch_related(Prefetch("specs", queryset=ProductSpec.objects.prefetch_related("usages","vehicle_types_rel")))
    )
    if selected_vehicles:
        products = products.filter(specs__vehicle_types_rel__code__in=selected_vehicles)
    
    products = products.distinct()

    vehicle_choices = list(
        VehicleType.objects.order_by("sort_order", "name").values_list('code','name'))

    # --- กรองตาม usage (M2M) ---
    if selected_usages:
        products = products.filter(specs__usages__in=selected_usages)

    products = products.distinct()
    context = {
        "sections": categories,  # เก็บหมวดไว้ใช้ใน template เดิม
        "products": products,    # เก็บสินค้าสำหรับการกรอง
        "usages": Usage.objects.order_by("name"),
        "vehicle_choices": vehicle_choices,
        "has_filters": has_filters, 
        "selected_vehicles": selected_vehicles,
        "selected_usages": [int(x) for x in selected_usages] if selected_usages else [],
    }

    return render(request, "product.html", context)

    # return render(request, 'product.html', {'sections': categories})
def product_detail(request, id):
    p = get_object_or_404(Product, id=id)
    related = Product.objects.filter(category=p.category).exclude(id=p.id)
    gallery = list(p.images.all()) or []
    return render(request, 'product_dt.html',{
        'product': p,
        'related': related,
        'gallery': gallery,
    })
def category_list(request, cat_id):
    cat = get_object_or_404(Category, id=cat_id)
    items = Product.objects.filter(category=cat)
    return render(request, 'category_list.html', {'category': cat, 'products': items})

def contact(request):
    success = False
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        if name and message:  # กันกรณีกรอกว่าง
            ContactMessage.objects.create(
                name=name,
                email=email or None,
                subject=subject or None,
                message=message,
            )
            success = True

    return render(request, "contact.html", {"success": success})