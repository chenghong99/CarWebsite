# Car Rental Website


Repository for the CarRental application with Django and Heroku with Raw SQL.

Envisioned app:
The application is a platform that allows car owners to rent out their cars to other users when they don't need it.
At any point in time, when car owners know that they would not need to use their cars, they can create an account and register the cars that they would like to rent out on the platform, with an option to state the dates that their cars would not be available for rental.
Users are able to freely browse the cars that are on the platform. 
Users must be logged into an account to make a rental booking but need not be logged in to browse listings.
Bookings can be made at any time in advance for the listing of the user's choice, at a daily rate.
Dates that are unavailable for rental of a particular car would be blocked out for the user.
The user must indicate the pick-up and drop-off dates for the car when making a booking.
The user will receive a confirmation of the car rental and the car owner would receive a notification that their car has been rented out. 
After a rental has been confirmed, the availability of the car is updated.
Administrators have access to all customer details, the cars listed in the database, the current car rentals as well as the rental due date.
Administrators can also create, modify and delete all entries.


Our website will have 4 main screens/features namely the login/sign-up, profile page, home page, admin page:
login/signup
Users will be able to create an account and log in. There will be 2 fields for the login page (username textbox, password textbox)
At the sign up page there will be 6 fields all in textbox (email, DOB, address (for pick up), username, password and confirm password) 
There will also be constraints here that ensures everything is not null and the email and username are unique
We can also ensure registered users are above the age of 18 by adding a check constraint.
Profile page
At the profile page users can list their cars for others to rent and also modify their listings
Car listings include the following features: Car make, model, year, mileage, availability
Users will also be able to see the details of their current rentals at the profile page (including total rental fee, pick-up and drop-off date, car VIN)
Users can also see their details and modify their details in the profile page.
Home page
At the home page users get to search for cars they would like to rent on certain days. (The results shown are only those listed as available in the database)
After finding their desired car the users can book the car. (Upon booking the car it will be listed as unavailable on the selected date/s in the database)
Administrator page
Access to all user details, car listings , current car rentals, rental due date. (In the form of a table)
Administrators can also create, modify and delete all entries.


