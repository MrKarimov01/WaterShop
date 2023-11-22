from django.shortcuts import redirect, render
from main.models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from main.forms import *
from django.http import HttpResponse


def PagenatorPage(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get("page")
    try:
        list = paginator.page(pages)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Foydalanuvchi muvaffaqiyatli kirdi, uning sesiyasini ochamiz
            login(request, user)
            return redirect('index')
        else:
            # Login yoki parol noto'g'ri
            messages.error(request, "Login yoki parolni noto'g'ri kiritdingiz. Iltimos, qaytadan urinib ko'ring!")
            return render(request, 'pages-sign-in.html', {'login_error': True})
    return render(request, 'pages-sign-in.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def reset_password_view(request):
    return render(request, 'pages-reset-password.html')


@login_required
def index_view(request):
    return render(request, "dashboard.html")


@login_required
def category_view(request):
    context = {
        "categories": Category.objects.all(),
    }
    return render(request, 'category.html', context)


@login_required
def select_category_view(request):
    context = {
        "categories": Category.objects.all(),
        "product": Product.objects.all(),
    }
    return render(request, 'select-category.html', context)


@login_required
def create_category_view(request):
    if request.method == 'POST' and request.POST.get('adding') == '001':
        name = request.POST.get("name")
        photo = request.FILES.get("photo")
        category = Category.objects.create(
            name=name,
            photo=photo,
        )
        category.save()
        return redirect("create-category")

    if request.method == 'POST' and request.POST.get('editing') == '002':
        name = request.POST.get("name")
        photo = request.FILES.get("photo")
        category = Category.objects.create(
            name=name,
            photo=photo,
        )
        category.save()
        return redirect("category_edit", category.pk)

    if request.method == 'POST':
        name = request.POST.get("name")
        photo = request.FILES.get("photo")
        category = Category.objects.create(
            name=name,
            photo=photo,
        )
        category.save()
        return redirect('category-page')
    return render(request, 'category.html')


@login_required
def category_by_product_view(request, pk):
    category = Category.objects.get(id=pk)
    products_in_selected_category = Product.objects.filter(category=category).order_by("-id")
    paginator = PagenatorPage(products_in_selected_category, 3, request)
    return render(request, 'category-by-product.html', context={'products': paginator, "dir": pk})


@login_required
def category_page_view(request):
    context = {
        'categories': Category.objects.all(),
    }
    return render(request, 'category-page.html', context)


@login_required
def category_edit_view(request, pk):
    form = get_object_or_404(Category, id=pk)
    if request.method == 'POST' and request.POST.get('editing') == '002':
        dform = CategoryForm(request.POST, request.FILES, instance=form)
        if dform.is_valid():
            dform.save()
        return redirect('category_edit', pk)
    elif request.method == 'POST' and request.POST.get('adding') == '001':
        dform = CategoryForm(request.POST, request.FILES, instance=form)
        if dform.is_valid():
            dform.save()
        return redirect('create-category', )
    elif request.method == 'POST':
        dform = CategoryForm(request.POST, request.FILES, instance=form)
        if dform.is_valid():
            dform.save()
        return redirect('category-page')
    return render(request, 'category-edit.html', context={'form': CategoryForm(instance=form), 'pk': pk})


@login_required
def delete_category_view(request, pk):
    Category.objects.get(id=pk).delete()
    return redirect('category-page')


@login_required
def create_product_view(request, pk):
    form = ProductForm()
    category = Category.objects.get(id=pk)
    context = {
        "form": form,
        "category": category,

    }
    if request.method == 'GET':
        return render(request, 'create-product.html', context)

    if request.method == 'POST' and request.POST.get('adding') == '001':
        a = Product.objects.create(
            category=Category.objects.get(id=pk),
            photo=request.FILES.get("photo"),
            name=request.POST.get("name"),
            liter=request.POST.get("liter"),
            price=request.POST.get("price"),

          )
        return redirect("create-product", pk)

    if request.method == 'POST' and request.POST.get('editing') == '002':
        a = Product.objects.create(
            category=Category.objects.get(id=pk),
            photo=request.FILES.get("photo"),
            name=request.POST.get("name"),
            liter=request.POST.get("liter"),
            price=request.POST.get("price"),

          )
        return redirect('product-edit', a.id)

    if request.method == 'POST':
        a = Product.objects.create(
            category=Category.objects.get(id=pk),
            photo=request.FILES.get("photo"),
            name=request.POST.get("name"),
            liter=request.POST.get("liter"),
            price=request.POST.get("price"),

        )
    return redirect("category-by-product", pk)


@login_required
def product_edit_view(request, pk):
    obj = get_object_or_404(Product, id=pk)

    # if request.method == 'GET':
    #     context = {'form': ProductForm(instance=obj), 'id': pk}
    #     return render(request, 'product.html', context)

    if request.method == 'POST' and request.POST.get('editing') == '002':
        form = ProductForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('product-edit', pk)

    elif request.method == 'POST' and request.POST.get('adding') == '001':
        form = ProductForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('create-product', pk)

    elif request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('category-by-product', obj.category.id)
    return render(request, 'product.html', context={'form': ProductForm(instance=obj), 'id': pk})


@login_required
def save_product_view(request, pk):
    product = Product.objects.get(id=pk)
    if product.is_valid():
        product.save()
    return redirect("category-by-product", pk)


@login_required
def delete_product_view(request, pk):
    Product.objects.get(id=pk).delete()
    return redirect('category-by-product', pk)


@login_required
def output_page_view(request):
    context = {
        'output': Output.objects.all().order_by("-id")
    }
    return render(request, 'output-page.html', context)


@login_required
def create_output_view(request):
    if request.method == 'POST' and request.POST.get('adding') == '001':
        price = request.POST.get("price")
        about_the_price = request.POST.get("about_the_price")
        output = Output.objects.create(
            price=price,
            about_the_price=about_the_price,
        )
        output.save()
        return redirect('create-output')

    if request.method == 'POST' and request.POST.get('editing') == '002':
        price = request.POST.get("price")
        about_the_price = request.POST.get("about_the_price")
        output = Output.objects.create(
            price=price,
            about_the_price=about_the_price,
        )
        output.save()
        return redirect("output-edit", output.pk)

    if request.method == 'POST':
        price = request.POST.get("price")
        about_the_price = request.POST.get("about_the_price")
        output = Output.objects.create(
            price=price,
            about_the_price=about_the_price,
        )
        output.save()
        return redirect('output-page')
    return render(request, 'output.html')


@login_required
def output_edit_view(request, pk):
    form = get_object_or_404(Output, id=pk)

    if request.method == 'POST' and request.POST.get('editing') == '002':
        form = OutputForm(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
        return redirect('output-edit', pk)

    elif request.method == 'POST' and request.POST.get('adding') == '001':
        form = OutputForm(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
        return redirect('create-output')

    elif request.method == 'POST':
        form = OutputForm(request.POST, request.FILES, instance=form)
        if form.is_valid():
            form.save()
        return redirect('output-page', )
    return render(request, 'output-edit.html', context={'form': OutputForm(instance=form), 'pk': pk})


@login_required
def delete_output_view(request, pk):
    Output.objects.get(id=pk).delete()
    return redirect('output-page')


@login_required
def order_page_view(request):
    context = {
        "order": Order.objects.all()
    }
    return render(request, 'order-page.html', context)


@login_required
def order_create_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            # Perform any additional actions after saving the order
            return redirect('order-page')  # Redirect to a success page
    else:
        form = OrderForm()

    return render(request, 'order-create.html', {'form': form})


@login_required
def order_edit_view(request, pk):
    obj = get_object_or_404(Order, id=pk)

    if request.method == 'POST' and request.POST.get('editing') == '002':
        form = OrderForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('order_edit', pk)

    elif request.method == 'POST' and request.POST.get('adding') == '001':
        form = OrderForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('order-create',)
    elif request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('order-page', )
    return render(request, 'order-edit.html', context={'form': OrderForm(instance=obj), 'id': pk})


@login_required
def order_delete_view(request, pk):
    Order.objects.get(id=pk).delete()
    return redirect('order-page', pk)


@login_required
def help_view(request):
    return render(request, 'help.html')


