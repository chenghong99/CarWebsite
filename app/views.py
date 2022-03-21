from datetime import datetime
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    """Shows the main page"""

    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM customers WHERE customerid = %s", [request.POST['id']])

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers ORDER BY customerid")
        customers = cursor.fetchall()

    result_dict = {'records': customers}

    return render(request,'app/index.html',result_dict)

# Create your views here.
def view(request, id):
    """Shows the main page"""
    
    ## Use raw query to get a customer
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        customer = cursor.fetchone()
    result_dict = {'cust': customer}

    return render(request,'app/view.html',result_dict)

# Create your views here.
def add(request):
    """Shows the main page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [request.POST['customerid']])
            customer = cursor.fetchone()
            ## No customer with same id
            if customer == None:
                ##TODO: date validation
                cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                           request.POST['dob'] , request.POST['since'], request.POST['customerid'], request.POST['country'] ])
                return redirect('index')    
            else:
                status = 'Customer with ID %s already exists' % (request.POST['customerid'])


    context['status'] = status
 
    return render(request, "app/add.html", context)

# Create your views here.
def edit(request, id):
    """Shows the main page"""

    # dictionary for initial data with
    # field names as keys
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE customers SET first_name = %s, last_name = %s, email = %s, dob = %s, since = %s, country = %s WHERE customerid = %s"
                    , [request.POST['first_name'], request.POST['last_name'], request.POST['email'],
                        request.POST['dob'] , request.POST['since'], request.POST['country'], id ])
            status = 'Customer edited successfully!'
            cursor.execute("SELECT * FROM customers WHERE customerid = %s", [id])
            obj = cursor.fetchone()


    context["obj"] = obj
    context["status"] = status
 
    return render(request, "app/edit.html", context)

# Create your views here.
# Bug cannot insert into table
def login(request):
    """Shows the login page"""

    page = 'login'
    if request.user.is_authenticated:
        return redirect(index)

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request,'app/login.html', context)

   # Create your views here.
# def login(request):
#     """Shows the login page"""
#     context = {} 
#     status = ''

#     if request.POST:
#         ## Check if customerid is already in the table
#         with connection.cursor() as cursor:

#             cursor.execute("SELECT * FROM customer WHERE email = %s AND password = %s", [request.POST['email']], [request.POST['email']])
#             customer = cursor.fetchone()
#             ## No customer with same id
#             if customer != None:
#                 ##TODO: age validation
#                 cursor.execute("INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s)"
#                         , [request.POST['firstName'], request.POST['lastName'], request.POST['username'],
#                            request.POST['DOB'] , request.POST['psw'], request.POST['psw-repeat'], request.POST['email'] ])
#                 return redirect('index')    
#             else:
#                 status = 'Customer with email %s already exists' % (request.POST['email'])


#     context['status'] = status
#     return render(request,'app/signup.html', context)


    # Create your views here.
def signup(request):
    """Shows the login page"""
    context = {} 
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM customer WHERE email = %s", [request.POST['email']])
            customer = cursor.fetchone()
            ## No customer with same id
            date_time_obj = datetime.fromisoformat(request.POST['DOB'])
            datetime.fromisoformat(request.POST['DOB'])
            if request.POST['psw'] != request.POST['psw-repeat']:
                status = 'Password do not match'
            # elif ((datetime.now().date - date_time_obj).days // 365 < 18):
            #     status = 'Age limt less than 18'
            elif customer == None:
                ##TODO: age validation
                cursor.execute("INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST['firstName'], request.POST['lastName'], request.POST['username'],
                           request.POST['DOB'] , request.POST['psw'], request.POST['psw-repeat'], request.POST['email'] ])
                return redirect('index')    
            else:
                status = 'Customer with email %s already exists' % (request.POST['email'])


    context['status'] = status
    return render(request,'app/signup.html', context)

def profile(request):
    """Shows the profile page"""

    return render(request,'app/profile.html')

def editpersonalinfo(request):
    """Shows the editpersonalinfo page"""

    return render(request,'app/editpersonalinfo.html')

def editpersonalcarinfo(request):
    """Shows the editpersonalcarinfo page"""

    return render(request,'app/editpersonalcarinfo.html')

def editrentalcarinfo(request):
    """Shows the editrentalcarinfo page"""

    return render(request,'app/editrentalcarinfo.html')

    
