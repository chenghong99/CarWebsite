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
import datetime


# Create your views here.
##Cheng Hong
def index(request):
    """Shows the main page"""

    return render(request,'app/index.html')

#Cheng Hong
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

                if email == "useradmin@carwebsite.com":
                    return redirect("admin")
                else:
                    return redirect("index")
        else:
            messages.error(request, 'Wrong password')
            return render(request, 'app/login.html')
    
     return render(request,'app/login.html')


## Cheng Hong
def logout_page(request):
    logout(request)
    return redirect('login')
    

##Cheng Hong
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


#Cheng Hong
@login_required(login_url= 'login')
def profile(request):
    """Shows the profile page"""
    email = request.user.username
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customer WHERE email = %s", [email])
        cust = cursor.fetchone()
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM listings WHERE owner = %s", [email])
            car = cursor.fetchall()
            context ={'first_name' : cust[0], 'last_name' : cust[1], 'username' : cust[2],
            'dob' : cust[3], 'email' : cust[6], 'number' : cust[7], "records" : car}
        except:
            context ={'first_name' : cust[0], 'last_name' : cust[1], 'username' : cust[2],
            'dob' : cust[3], 'email' : cust[6], 'number' : cust[7], "records" : ["NA","NA","NA","NA","NA"]}

    return render(request,'app/profile.html', context)


##Cheng Hong
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

##Cheng Hong
def editpersonalcarinfo(request, car_vin):
    """Shows the editpersonalcarinfo page"""
    email = request.user.username
    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listings WHERE car_vin = %s", [car_vin])
        car = cursor.fetchone()
        context ={'car_make' : car[1], 'car_model' : car[2],
         'year' : car[3] , 'mileage' : car[4], 'rate' : car[5]}

    if request.method == 'POST':
        car_make = request.POST.get('car_make')
        car_model = request.POST.get('car_model')
        year = request.POST.get('year')
        mileage = request.POST.get('mileage')
        rate = request.POST.get('rate')
        context['car_make'] = car_make
        context['car_model'] = car_model
        context['year'] = year
        context['mileage'] = mileage
        context['rate'] = rate
	
        # if first_name == cust[0] and last_name == cust[1] and username == cust[2] and phonenumber == cust[7]:
        #     messages.error(request, 'New profile is identical to the old one!') 
        #     return render(request, 'app/change_profile.html', context)
	
        with connection.cursor() as cursor:
            try:
                cursor.execute("UPDATE listings SET carmake = %s, model = %s, year = %s, mileage = %s, rate = %s WHERE car_vin = %s", 
                [car_make, car_model, year, mileage, rate, car_vin])
		
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
                return render(request, 'app/editpersonalcarinfo', context)
	
            messages.success(request, 'Profile has been successfully updated!')
            return redirect('profile')

    return render(request,'app/editpersonalcarinfo.html', context)


#Cheng Hong
def editrentalcarinfo(request):
    """Shows the editrentalcarinfo page"""

    return render(request,'app/editrentalcarinfo.html')

def admin(request):
    return render(request, 'app/admin.html')

##Cheng Hong
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


##Peng Hao
def admin(request):
    ## Delete customer
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM customer WHERE email = %s", [request.POST['email']]) ## gotta make sure the constraint satisfied...foreign key
                ## can cursor.execute include multiple queries???? COZ NEED DELETE FROM TABLE BEFORE CAN DELETE FROM MASTERTABLE
                ## DO I NEED TO MAKE SURE THAT?? COZ SCHEMA GOT ON DELETE CASCADE
                #################################################################################################################################

    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customer ORDER BY email")
        personalinfo = cursor.fetchall()

    result_dict = {'records': personalinfo}

    return render(request,'app/admin.html',result_dict)


##PengHao
def addpersonalinfo(request):

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
            return render(request, 'app/addpersonalinfo.html')

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
                return render(request, 'app/addpersonalinfo.html')
            user = User.objects.create_user(email, password = password)
            user.save()
            messages.success(request, 'Account has been successfully registered!')
            return redirect('admin')
    return render(request, 'app/addpersonalinfo.html')


def editpersonalinfoPH(request, email):
    """Shows the editpersonalinfo page"""
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
            return render(request, 'app/editpersonalinfoPH.html', context)
	
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
                return render(request, 'app/editpersonalinfoPH.html', context)
	
            messages.success(request, 'Profile has been successfully updated!')
            return redirect('admin')    

    return render(request,'app/editpersonalinfoPH.html', context)

def personalcarinfoPH(request):
    """Shows the personalcarinfo page"""
    
    ## Delete listing
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM listings WHERE owner = %s AND car_vin = %s", [request.POST['owner'],request.POST['car_vin']]) ## gotta make sure the constraint satisfied...foreign key
                ## can cursor.execute include multiple queries???? COZ NEED DELETE FROM TABLE BEFORE CAN DELETE FROM MASTERTABLE
                ## DO I NEED TO MAKE SURE THAT?? COZ SCHEMA GOT ON DELETE CASCADE
                #################################################################################################################################
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listings ORDER BY owner")
        personalcarinfo = cursor.fetchall()

    result_dict = {'records': personalcarinfo}
    
    return render(request,'app/personalcarinfoPH.html',result_dict) 


def editpersonalcarinfoPH(request,owner,car_vin):
    """Shows the editpersonalcarinfo page"""
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM listings WHERE owner = %s AND car_vin = %s", [owner,car_vin])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE listings SET car_vin = %s, carmake = %s, model = %s, year = %s, mileage = %s, rate = %s, owner = %s WHERE owner = %s AND car_vin = %s"
                    , [request.POST.get('car_vin'), request.POST.get('carmake'), request.POST.get('model'),
                        request.POST.get('year') , request.POST.get('mileage'), request.POST.get('rate'), request.POST.get('owner'), owner,car_vin])
            status = 'Listing edited successfully!'
            cursor.execute("SELECT * FROM listings WHERE owner = %s AND car_vin = %s", [owner,car_vin])
            obj = cursor.fetchone()

    context["obj"] = obj
    context["status"] = status

    return render(request,'app/editpersonalcarinfoPH.html',context)

def addpersonalcarinfoPH(request):
    """Shows the addpersonalcarinfo page"""
    context = {}
    status = ''
    
    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO listings VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        , [request.POST.get('car_vin'), request.POST.get('carmake'), request.POST.get('model'),
                          request.POST.get('year'), request.POST.get('mileage'), request.POST.get('rate'), request.POST.get('owner')])
            
          ##### all these below is for tables with the check constraints to catch the constraint errors  
            except Exception as e:
                string = str(e)
                message = ""
                if 'duplicate key value violates unique constraint "rentals_pkey"' in string:  
                    message = 'The email has already been used by another user!' ## maybe please input the correct year! or correct number for mileage!
                elif 'new row for relation "rentals" violates check constraint "rentals_pick_up_check"' in string: ###### need go see correct error msg
                    message = 'Please check that drop_off date is not before pick_up date!'
                elif 'new row for relation "rentals" violates check constraint "users_mobile_number_check"' in string:
                    message = 'Please enter a valid Singapore number!'####################################### to edit
                messages.error(request, message)
                return render(request, "addpersonalcarinfoPH.html")
            return redirect('personalcarinfoPH') ##### i added this so it routes to personalcarinfo.html after

    context['status'] = status

    return render(request,'app/addpersonalcarinfoPH.html')


def unavailablecarinfoPH(request):
    """Shows the unavailablecarinfo page"""
    
    ## Delete unavailable
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM unavailable WHERE car_vin = %s AND unavailable = %s", [request.POST['car_vin'],request.POST['unavailable']])
                
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM unavailable ORDER BY unavailable")
        unavailablecarinfo = cursor.fetchall()

    result_dict = {'records': unavailablecarinfo}
    
    return render(request,'app/unavailablecarinfoPH.html',result_dict)

def editunavailablecarinfoPH(request,car_vin, unavailable):
    """Shows the editpersonalcarinfo page"""
    context ={}

    # fetch the object related to passed id
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM unavailable WHERE car_vin = %s AND unavailable = %s", [car_vin,datetime.datetime.strptime(unavailable,'%b %d %Y').strftime('%m/%d/%Y')])
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE unavailable SET car_vin = %s, owner = %s, unavailable = %s WHERE car_vin = %s AND unavailable = %s"
                    , [request.POST.get('car_vin'), request.POST.get('owner'), request.POST.get('unavailable'),car_vin, unavailable])
            status = 'Unavailable edited successfully!'
            cursor.execute("SELECT * FROM unavailable WHERE car_vin = %s AND unavailable = %s", [car_vin,datetime.datetime.strptime(unavailable,'%b %d %Y').strftime('%m/%d/%Y')])
            obj = cursor.fetchone()

    context["obj"] = obj
    context["status"] = status

    return render(request,'app/editunavailablecarinfoPH.html',context)


def addunavailablecarinfoPH(request): ############################# to change to try and except method like addrentalcarinfo
    """Shows the addpersonalcarinfo page"""
    context = {}
    status = ''
    
    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO unavailable VALUES (%s, %s, %s)"
                        , [request.POST.get('car_vin'), request.POST.get('owner'), request.POST.get('unavailable')])
            
          ##### all these below is for tables with the check constraints to catch the constraint errors  
            except Exception as e:
                string = str(e)
                message = ""
                if 'duplicate key value violates unique constraint "rentals_pkey"' in string:  
                    message = 'The email has already been used by another user!' #### maybe "car_vin with unavailablility on this date alr exists!"
                elif 'new row for relation "rentals" violates check constraint "rentals_pick_up_check"' in string: ###### need go see correct error msg
                    message = 'Please check that drop_off date is not before pick_up date!'#### maybe "owner and car_vin doesnt exist in listings table!"
                messages.error(request, message)
                return render(request, "addunavailablecarinfoPH.html")
            return redirect('unavailablecarinfoPH') ##### i added this so it routes to unavailablecarinfo.html after 

    context['status'] = status

    return render(request,'app/addunavailablecarinfoPH.html')

def rentalcarinfoPH(request):
    """Shows the rentalcarinfo page"""
    
    ## Delete rental
    if request.POST:
        if request.POST['action'] == 'delete':
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM rentals WHERE car_vin = %s AND pick_up = %s", [request.POST['car_vin'],request.POST['pick_up']])
                
    ## Use raw query to get all objects
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rentals ORDER BY pick_up")
        rentalcarinfo = cursor.fetchall()

    result_dict = {'records': rentalcarinfo}
    
    return render(request,'app/rentalcarinfoPH.html',result_dict)

def editrentalcarinfoPH(request,car_vin, pick_up): #<input type="hidden" name="car_vin" value="{{cust.2}}"/>      in rentalcarinfo.html
                                                     #<input type="hidden" name="unavailable" value="{{cust.3}}"/>
                                                     
    """Shows the editrentalcarinfo page"""
    context ={}

    # fetch the object related to passed car_vin and unavailable
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM rentals WHERE car_vin = %s AND pick_up = %s", [car_vin,datetime.datetime.strptime(pick_up,'%b %d %Y').strftime('%m/%d/%Y')]) 
        obj = cursor.fetchone()

    status = ''
    # save the data from the form

    if request.POST:
        ##TODO: date validation
        with connection.cursor() as cursor:
            cursor.execute("UPDATE rentals SET owner = %s, renter = %s, car_vin = %s, pick_up = %s, drop_off = %s, rental_fee = %s WHERE car_vin = %s AND pick_up = %s"
                    , [request.POST.get('owner'), request.POST.get('renter'), request.POST.get('car_vin'), request.POST.get('pick_up'),request.POST.get('drop_off'),
                      request.POST.get('rental_fee'), car_vin, pick_up])
            status = 'Rental edited successfully!'
            cursor.execute("SELECT * FROM rentals WHERE car_vin = %s AND pick_up = %s", [car_vin,datetime.datetime.strptime(pick_up,'%b %d %Y').strftime('%m/%d/%Y')])
            obj = cursor.fetchone()

    context["obj"] = obj
    context["status"] = status

    return render(request,'app/editrentalcarinfoPH.html',context)

def addrentalcarinfoPH(request):
    """Shows the addrentalcarinfo page"""
    context = {}
    status = ''

    if request.POST:
        ## Check if customerid is already in the table
        with connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO rentals VALUES (%s, %s, %s, %s, %s, %s )"
                        , [request.POST.get('owner'), request.POST.get('renter'), request.POST.get('car_vin'),
                          request.POST.get('pick_up'), request.POST.get('drop_off'), request.POST.get('rental_fee')])
            
          ##### all these below is for tables with the check constraints to catch the constraint errors  
            except Exception as e:
                string = str(e)
                message = ""
                if 'duplicate key value violates unique constraint "rentals_pkey"' in string:  
                    message = 'Pick-up date for this Car VIN already exists!' ####################################### to edit
                elif 'new row for relation "rentals" violates check constraint "rentals_pick_up_check"' in string: ###### need go see correct error msg
                    message = 'Please check that drop_off date is not before pick_up date!'
                elif 'new row for relation "rentals" violates check constraint "users_mobile_number_check"' in string:
                    message = 'Please enter a valid Singapore number!'####################################### to edit
                messages.error(request, message)
                return render(request, "addrentalcarinfoPH.html")
            return redirect('rentalcarinfoPH') ##### i added this so it routes to rentalcarinfo.html after 
            
    context['status'] = status

    return render(request,'app/addrentalcarinfoPH.html')