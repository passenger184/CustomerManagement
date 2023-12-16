from django.shortcuts import render, redirect
from .models import *
from .forms import CustomerForm, OrderForm, CreateUserForm
from django.forms import inlineformset_factory  # this lets us to create multiple forms with in one form
from .filters import OrderFilter

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
# from django.contrib.auth.models import Group

# from django.contrib.auth.forms import UserCreationForm
# Create your views here.

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Custmor.objects.all()
    
    total_customers = customers.count()
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {
        'orders': orders,
        'customers': customers ,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
    }
    
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Custmor.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {'customer': customer, 'orders': orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Custmor, Order, fields=('product', 'status'), extra=10 ) # extra is how many field you want in form arguments are paret child and child sets u want to pass
    customer = Custmor.objects.get(id=pk)
    formset = OrderFormSet( queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})  #initial means able to see at first
    if request.method=="POST":
        # print("printing", request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    
    context = {'formset':formset}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method=="POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'delete.html', context)



@unauthenticated_user
def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)   
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            
            # Custmor.objects.create(  #assigning customer automatically to user
            #     user=user,
            #     name=user.username,
            # )
            
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    
    context = {
        'form':form
    }
    return render(request, 'register.html', context)


@unauthenticated_user
def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.info(request, 'Username or Password is Incorrect')
    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userView(request):
    orders = request.user.custmor.order_set.all()
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context={
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending
        }
    return render(request, 'user.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def settings_pro(request):
    customer = request.user.custmor
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    
    context = {'form':form}
    return render(request, 'settings.html', context)

























