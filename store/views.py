from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm

def home(request):
    categories = Category.objects.all().order_by('name')
    products = Product.objects.filter(in_stock=True).order_by('-created_at')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Limited page numbers for pagination controls
    total_pages = paginator.num_pages
    current_page = page_obj.number
    if total_pages <= 7:
        page_range = range(1, total_pages + 1)
    else:
        if current_page <= 4:
            page_range = list(range(1, 6)) + ['...', total_pages]
        elif current_page > total_pages - 4:
            page_range = [1, '...'] + list(range(total_pages-4, total_pages+1))
        else:
            page_range = [1, '...'] + list(range(current_page-1, current_page+2)) + ['...', total_pages]

    return render(request, 'store/home.html', {
        'categories': categories,
        'page_obj': page_obj,
        'page_range': page_range,
    })

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all().order_by('name')
    products = Product.objects.filter(in_stock=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products.order_by('-created_at'), 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_pages = paginator.num_pages
    current_page = page_obj.number
    if total_pages <= 7:
        page_range = range(1, total_pages + 1)
    else:
        if current_page <= 4:
            page_range = list(range(1, 6)) + ['...', total_pages]
        elif current_page > total_pages - 4:
            page_range = [1, '...'] + list(range(total_pages-4, total_pages+1))
        else:
            page_range = [1, '...'] + list(range(current_page-1, current_page+2)) + ['...', total_pages]

    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
        'page_range': page_range,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/product_detail.html', {'product': product})

@require_POST
def add_to_cart(request, product_id):
    qty = int(request.POST.get('quantity', 1))
    Cart(request).add(product_id, quantity=qty)
    messages.success(request, 'Added to cart.')
    return redirect('store:cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})

@require_POST
def update_cart(request, product_id):
    qty = int(request.POST.get('quantity', 1))
    Cart(request).add(product_id, quantity=qty, override=True)
    return redirect('store:cart_view')

def remove_from_cart(request, product_id):
    Cart(request).remove(product_id)
    return redirect('store:cart_view')

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
                paid=True,
            )
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            messages.success(request, f'Thanks! Your order #{order.id} was placed.')
            return redirect('store:home')
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {'form': form, 'cart': cart})
