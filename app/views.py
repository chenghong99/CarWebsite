from datetime import datetime
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
from matplotlib.style import context


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
    

##To test out
def signup(request):

    if request.method == 'POST':
        # Ensure password matches confirmation
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        DOB = request.POST.get('DOB')
        email = request.POST.get('email').lower()
        number = request.POST.get('number')
        password = request.POST.get('psw')
        confirm_password = request.POST.get('psw-repeat')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'app/signup.html')

        with connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO customer VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                [first_name, last_name, username, DOB, password, confirm_password, email, number])

            except Exception as e:
                err = str(e)
                message = err
            
                if 'duplicate key value violates unique constraint "customer_pkey"' in err:
                    message = 'Customer email already exists'
                elif 'duplicate key value violates unique constraint "customer_username_key"' in err:
                    message = 'Customer username already exists'
                elif 'duplicate key value violates unique constraint "auth_user_username_key"' in err:
                    message = 'Customer username already exists'
                elif 'new row for relation "customer" violates check constraint "customer_email_check"' in err:
                    message = 'Please enter a valid email address!'
                elif 'new row for relation "customer" violates check constraint "customer_mobile_number_check"' in err:
                    message = 'Please enter a valid phone number'
                elif 'new row for relation "customer" violates check constraint "customer_dob_check"' in err:
                    message = 'Age below 18'
                messages.error(request, message)
                return render(request, 'app/signup.html')
            user = User.objects.create_user(email, password = password)
            user.save()
            messages.success(request, 'Account has been successfully registered!')
            return redirect('login')
    return render(request, 'app/signup.html')

@login_required(login_url= 'login')
def profile(request):
    """Shows the profile page"""
    email = request.user.username
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customer WHERE email = %s", [email])
        cust = cursor.fetchone()
    context ={'first_name' : cust[0], 'last_name' : cust[1], 'username' : cust[2],
    'dob' : cust[3], 'email' : cust[6], 'number' : cust[7]}

    return render(request,'app/profile.html', context)

@login_required(login_url = 'login')
def editpersonalinfo(request):
    """Shows the editpersonalinfo page"""
    email = request.user.username
    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customer WHERE email = %s", [email])
        cust = cursor.fetchone()
    context ={'first_name' : cust[0], 'last_name' : cust[1], 'username' : cust[2], 'phonenumber' : cust[7]}

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        phonenumber = request.POST.get('phonenumber')
        context['first_name'] = first_name
        context['last_name'] = last_name
        context['username'] = username
        context['phonenumber'] = phonenumber
	
        if first_name == cust[0] and last_name == cust[1] and username == cust[2] and phonenumber == cust[7]:
            messages.error(request, 'New profile is identical to the old one!') 
            return render(request, 'app/change_profile.html', context)
	
        with connection.cursor() as cursor:
            try:
                cursor.execute("UPDATE customer SET first_name = %s, last_name = %s, username = %s, mobile_number = %s WHERE email = %s", [first_name, last_name, username, phonenumber, email])
		
            except Exception as e:
                string = str(e)
                message = string
		
                if 'new row for relation "customer" violates check constraint "customer_mobile_number_check"' in string:
                    message = 'Please enter a valid Singapore number!'
		
                elif 'out of range for type integer' in string:
                    message = 'Please enter a valid Singapore number!'

                elif 'out of range for type integer' in string:
                    message = 'Please enter a valid Singapore number!'

                elif 'duplicate key value violates unique constraint "customer_username_key"' in string:
                    message = 'Customer username taken!'
		
                messages.error(request, message) 
                return render(request, 'app/editpersonalinfo.html', context)
	
            messages.success(request, 'Profile has been successfully updated!')
            return redirect('profile')    

    return render(request,'app/editpersonalinfo.html', context)

def editpersonalcarinfo(request):
    """Shows the editpersonalcarinfo page"""

    return render(request,'app/editpersonalcarinfo.html')

def editrentalcarinfo(request):
    """Shows the editrentalcarinfo page"""

    return render(request,'app/editrentalcarinfo.html')

@login_required(login_url = 'login')
def addcar(request):
    if request.method == 'POST':
        # Ensure password matches confirmation
        email = request.user.username
        car_vin = request.POST.get('car_vin')
        carmake = request.POST.get('carmake')
        carmodel = request.POST.get('model')
        year = request.POST.get('year')
        mileage = request.POST.get('mileage')
        rate = request.POST.get('rate')

        with connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO listings VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                [car_vin, carmake, carmodel, year, mileage, rate, email])
            except Exception as e:
                err = str(e)
                message = err
            
                if 'new row for relation "listings" violates check constraint "listings_mileage_check"' in err:
                    message = 'Invalid milaeage'
                elif 'new row for relation "listings" violates check constraint "listings_rate_check"' in err:
                    message = 'Invalid rate'
                elif 'new row for relation "listings" violates check constraint "listings_year_check"' in err:
                    message = 'Invalid year'
                messages.error(request, message)
                return render(request, 'app/addcar.html')
            messages.success(request, 'Car succesfully listed')
            return redirect('addcar')
    return render(request, 'app/addcar.html')
