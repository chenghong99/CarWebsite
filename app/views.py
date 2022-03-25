from datetime import datetime
from tkinter import EXCEPTION
from tokenize import String
from django.shortcuts import render, redirect
from django.db import connection
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login as loginform
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib.auth import login as auth_login


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
# def login(request):
#     """Shows the login page"""

#     page = 'login'
#     if request.user.is_authenticated:
#         return redirect(index)

#     if request.method == "POST":
#         email = request.POST.get("email").lower()
#         password = request.POST.get("password")

#         try:
#             user = User.objects.get(email=email)
#         except:
#             messages.error(request, 'User does not exist')

#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Username OR password does not exit')

#     context = {'page': page}
#     return render(request,'app/login.html', context)

# def login(request):
#      """Shows the login page"""

#      return render(request,'app/login.html')

   # Create your views here.
# def login(request):
#     """Shows the login page"""
#     context = {} 
#     status = ''

#     if request.POST:
#         ## Check if customerid is already in the table
#         with connection.cursor() as cursor:
#             email = request.POST["uname"]
#             password = request.POST["psw"]

#             cursor.execute("SELECT * FROM customer WHERE email = %s", email,)
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

def login(request):
     """Shows the login page"""
     if request.user.is_authenticated:
        email = request.user.username
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customer WHERE email = %s", [email])
            customer = cursor.fetchone()
            return redirect('index')
    
     if request.method == 'POST':
        email = request.POST.get('uname').lower()
        password = request.POST.get('psw')
        # To delete: flush the user table
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT * FROM customer")
        #     res = [item for item in cursor.fetchall()]
        #     print(res)
        try: 
            user = User.objects.get(username = email)
        except Exception as e:
            print(e)
            messages.error(request, 'Invalid email address')
            return render(request, 'app/login.html')  
        user = authenticate(request, username = email, password = password)
        if user != None:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer WHERE email = %s", [email])
                loginform(request, user)
                return redirect("index")
        else:
            messages.error(request, 'Wrong password')
            return render(request, 'app/login.html')
    
     return render(request,'app/login.html')

def logout_page(request):
    logout(request)
    return redirect('login')
    
# def login(request):
# 	if request.method == "POST":
# 		form = AuthenticationForm(request, data=request.POST)
# 		if form.is_valid():
# 			username = form.cleaned_data.get('username')
# 			password = form.cleaned_data.get('password')
# 			user = authenticate(username=username, password=password)
# 			if user is not None:
# 				auth_login(request, user)
# 				messages.info(request, f"You are now logged in as {username}.")
# 				return redirect("index")
# 			else:
# 				messages.error(request,"Invalid username or password.")
# 		else:
# 			messages.error(request,"Invalid username or password.")
# 	form = AuthenticationForm()
# 	return render(request=request, template_name="login.html", context={"login_form":form})


# def login(request):
#     email = request.POST.get('uname').lower()
#     password = request.POST.get('psw')
#         # try: 
#         #     user = User.objects.get(username = email)
#         # except:
#         #     messages.error(request, 'Invalid email address')
#         #     return render(request, 'app/login.html')  
#     user = authenticate(request, username = email, password = password)
#     if user != None:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM customer WHERE email = %s", [email,])
#             customer = cursor.fetchone()
#             login(request, user)
#             return redirect("index")
#     else:
#         messages.error(request, 'Wrong password')
#         return render(request, 'app/login.html')
#     return render(request,'app/login.html')
    


    # Create your views here.
# def signup(request):
#     """Shows the login page"""
#     context = {} 
#     status = ''

#     if request.POST:
#         ## Check if customerid is already in the table
#         with connection.cursor() as cursor:

#             cursor.execute("SELECT * FROM customer WHERE email = %s", [request.POST['email']])
#             customer = cursor.fetchone()
#             ## No customer with same id
#             date_time_obj = datetime.fromisoformat(request.POST['DOB'])
#             datetime.fromisoformat(request.POST['DOB'])
#             if request.POST['psw'] != request.POST['psw-repeat']:
#                 status = 'Password do not match'
#             # elif ((datetime.now().date - date_time_obj).days // 365 < 18):
#             #     status = 'Age limt less than 18'
#             elif customer == None:
#                 ##TODO: age validation
#                 cursor.execute("INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s)"
#                         , [request.POST['firstName'], request.POST['lastName'], request.POST['username'],
#                            request.POST['DOB'] , request.POST['psw'], request.POST['psw-repeat'], request.POST['email'] ])
#                 return redirect('index')    
#             else:
#                 status = 'Customer with email %s already exists' % (request.POST['email'])


#     context['status'] = status
#     return render(request,'app/signup.html', context)

##To test out
def signup(request):

    if request.method == 'POST':
        # Ensure password matches confirmation
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        DOB = request.POST.get('DOB')
        email = request.POST.get('email').lower()
        password = request.POST.get('psw')
        confirm_password = request.POST.get('psw-repeat')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'app/signup.html')

        with connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                [first_name, last_name, username, DOB, password, confirm_password, email])

            except Exception as e:
                err = str(e)
                message = err

                if 'duplicate key value violates unique constraint "users_pkey' in err:
                    message = 'Customer email already exists'
                elif 'new row for relation "customer" violates check constraint "customer_email_check"' in err:
                    message = 'Please enter a valid email address!'
                messages.error(request, message)
                return render(request, 'app/signup.html')
            user = User.objects.create_user(email, password = password)
            user.save()
            messages.success(request, 'Account has been successfully registered!')
            return redirect('index')
    return render(request, 'app/signup.html')

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

    
