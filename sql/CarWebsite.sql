CREATE TABLE IF NOT EXISTS userinfo (
	userID INT NOT NULL,
	firstName VARCHAR(32) NOT NULL,
	lastName VARCHAR(32) NOT NULL,
	email VARCHAR(256) PRIMARY KEY,
	DOB DATE NOT NULL,
	--urrentDate DATE DEFAULT SYSDATE,
	--CONSTRAINT ageCheck CHECK((ROUND((DOB-currentDate)/365)) = 18),
	password VARCHAR(32) NOT NULL,
	confirmPassword VARCHAR(32) NOT NULL,
	CONSTRAINT passwordMatch CHECK(password = confirmPassword)
)

CREATE TABLE IF NOT EXISTS car (
	carMake VARCHAR(32) NOT NULL,
	carModel VARCHAR(32) NOT NULL,
	year DATE,
	mileage INT,
	availability DATE,
	carVIN VARCHAR(32) PRIMARY KEY,
	email VARCHAR(256) REFERENCES userinfo(email)
)


CREATE TABLE IF NOT EXISTS rental (
	borrowerEmail VARCHAR(256) NOT NULL,
	ownerEmail VARCHAR(256) NOT NULL,
	carVIN VARCHAR(32) NOT NULL,
	dateTimeBorrowed DATETIME DEFAULT NOW(),
	dateTimeDue DATETIME NOT NULL,
	dateTimeReturned DATETIME NOT NULL,
	dateTimeDue DATETIME NOT NULL,
	CONSTRAINT chk_dateDue CHECK (dateTimeDue >= dateTimeBorrowed),
	FOREIGN KEY carVIN REFERENCES 
)





