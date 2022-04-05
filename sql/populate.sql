--POPULATE CUSTOMER TABLE
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Martyn', 'Van der Spohr', 'mvanderspohr0', '8/10/2001', 'b0tbG1wm7YzZ', 'b0tbG1wm7YzZ', 'mvanderspohr0@google.ca',96539517);
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Ben', 'McVeigh', 'bmcveigh1', '3/3/2001', 'PWdKZvjhJ', 'PWdKZvjhJ', 'bmcveigh1@fema.gov',96539517);
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Clair', 'Scutter', 'cscutter2', '10/12/2001', 'ZKyyUGrahIkf', 'ZKyyUGrahIkf', 'cscutter2@vinaora.com',96539517);
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Marinna', 'Greathead', 'mgreathead3', '10/12/2001', 'faROy6iNYg0w', 'faROy6iNYg0w', 'mgreathead3@chronoengine.com',96539517);
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Keith', 'Sprulls', 'ksprulls4', '6/2/2001', 'V7fwCF8s', 'V7fwCF8s', 'ksprulls4@fda.gov',96539517);
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Arlin', 'Dimond', 'adimond5', '1/1/2002', 'HwjmCMgNKBG', 'HwjmCMgNKBG', 'adimond5@twitpic.com',96539517);
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Jerri', 'Esel', 'jesel6', '3/9/2002', '4MbgJ9COTBOL', '4MbgJ9COTBOL', 'jesel6@squidoo.com',96539517);
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Jarred', 'Gailor', 'jgailor7', '10/2/2001', 'RMgzpcr', 'RMgzpcr', 'jgailor7@rediff.com',96539517);
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Saunders', 'Bompass', 'sbompass8', '8/9/2001', 'wShpblV', 'wShpblV', 'sbompass8@cnet.com',96539517);
insert into customer (first_name, last_name, username, dob, password, confirmpassword, email, mobile_number) values ('Amy', 'Warry', 'awarry9', '1/11/2002', 'ZZvye03xvN8', 'ZZvye03xvN8', 'awarry9@statcounter.com',96539517);

insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('3N1AB6AP3AL362912', 'Isuzu', 'Ascender', 2007, 80643, 50026, 'ksprulls4@fda.gov');
insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('5UMDU93557L734848', 'Volvo', 'XC70', 2007, 51820, 19742, 'ksprulls4@fda.gov');
insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('1N6AD0CU3FN047703', 'Nissan', 'Titan', 2004, 78648, 53456, 'adimond5@twitpic.com');
insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('3FADP0L3XBR853159', 'Dodge', 'Ram 50', 1993, 38823, 16470, 'jgailor7@rediff.com');
insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('5N1AR2MM8FC452719', 'Subaru', 'Tribeca', 2011, 70290, 35423, 'jgailor7@rediff.com');
insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('WAUSFAFL2BA782648', 'Volkswagen', 'Cabriolet', 2002, 34712, 86578, 'sbompass8@cnet.com');
insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('WA1LMBFE7ED541878', 'Hyundai', 'Elantra', 2003, 44723, 23456, 'sbompass8@cnet.com');
insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('JN8AS1MU7AM855309', 'Chrysler', 'Town & Country', 1993, 47443, 35895, 'sbompass8@cnet.com');
insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('5N1AN0NU1CN694265', 'Chevrolet', 'Suburban 1500', 1995, 19175, 45717, 'awarry9@statcounter.com');
insert into listings (car_vin, carmake, model, year, mileage, rate, owner) values ('JN8AZ2KRXBT327366', 'Audi', 'TT', 2011, 59961, 62219, 'awarry9@statcounter.com');

insert into unavailable (car_vin, owner, unavailable) values ('3N1AB6AP3AL362912', 'ksprulls4@fda.gov', '2022-12-14');
insert into unavailable (car_vin, owner, unavailable) values ('3N1AB6AP3AL362912', 'ksprulls4@fda.gov', '2023-01-24');
insert into unavailable (car_vin, owner, unavailable) values ('3N1AB6AP3AL362912', 'ksprulls4@fda.gov', '2023-01-10');
insert into unavailable (car_vin, owner, unavailable) values ('JN8AZ2KRXBT327366', 'awarry9@statcounter.com', '02/03/2023');
insert into unavailable (car_vin, owner, unavailable) values ('JN8AZ2KRXBT327366', 'awarry9@statcounter.com', '2022-09-22');
insert into unavailable (car_vin, owner, unavailable) values ('5N1AN0NU1CN694265', 'awarry9@statcounter.com', '2022-09-23');
insert into unavailable (car_vin, owner, unavailable) values ('5N1AN0NU1CN694265', 'awarry9@statcounter.com', '2022-08-04');
insert into unavailable (car_vin, owner, unavailable) values ('WA1LMBFE7ED541878', 'sbompass8@cnet.com', '2022-12-23');
insert into unavailable (car_vin, owner, unavailable) values ('WAUSFAFL2BA782648', 'sbompass8@cnet.com', '2022-12-07');
insert into unavailable (car_vin, owner, unavailable) values ('WAUSFAFL2BA782648', 'sbompass8@cnet.com', '2022-08-17');

insert into rentals (owner,renter,car_vin,pick_up,drop_off,rental_fee)
values
('awarry9@statcounter.com','ksprulls4@fda.gov','JN8AZ2KRXBT327366','2022-09-17','2022-09-17',62219),
('sbompass8@cnet.com','ksprulls4@fda.gov','JN8AS1MU7AM855309','2022-09-17','2022-09-17',35895),
('jgailor7@rediff.com','ksprulls4@fda.gov','5N1AR2MM8FC452719','2022-09-17','2022-09-17',35423);

insert into rentals (owner,renter,car_vin,pick_up,drop_off,rental_fee)
values
('awarry9@statcounter.com','ksprulls4@fda.gov','JN8AZ2KRXBT327366','2022-09-17','2022-09-17',62219),
('sbompass8@cnet.com','ksprulls4@fda.gov','JN8AS1MU7AM855309','2022-09-17','2022-09-17',35895),
('jgailor7@rediff.com','ksprulls4@fda.gov','5N1AR2MM8FC452719','2022-09-17','2022-09-17',35423);

insert into rentals (owner,renter,car_vin,pick_up,drop_off,rental_fee)
values
('chenghong123@gmail.com', 'chenghong1234@gmail.com', '5N1AN0NU1CN694264', '2022-09-17','2022-09-17', 100);

