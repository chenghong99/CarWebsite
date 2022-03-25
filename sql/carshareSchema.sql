CREATE TABLE IF NOT EXISTS customer(
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    username VARCHAR(64) UNIQUE NOT NULL,
    dob DATE NOT NULL CHECK((DATE_PART('year', CURRENT_DATE) - DATE_PART('year', dob) > 18)),
    password VARCHAR(32) NOT NULL,
    confirmPassword VARCHAR(32) NOT NULL ,
    CONSTRAINT pw_match CHECK(confirmPassword = password),
    email VARCHAR(256) PRIMARY KEY CHECK (email LIKE '%_@_%._%'),
    mobile_number INT NOT NULL CHECK ((mobile_number BETWEEN 30000000 AND 39999999) OR
									  (mobile_number BETWEEN 60000000 AND 69999999) OR
									  (mobile_number BETWEEN 80000000 AND 89999999) OR
									  (mobile_number BETWEEN 90000000 AND 98999999))
);

CREATE TABLE IF NOT EXISTS listings (
  car_vin VARCHAR(17) NOT NULL,
  carmake VARCHAR(64) NOT NULL,
  model VARCHAR(64) NOT NULL,
  year INT NOT NUll CHECK (year>0),
  mileage NUMERIC NOT NULL CHECK (mileage >0),
  rate NUMERIC NOT NULL CHECK (rate>0),
  owner VARCHAR(256) REFERENCES customer(email) ON DELETE CASCADE,
  PRIMARY KEY (owner,car_vin)
);


CREATE TABLE IF NOT EXISTS unavailable(
    car_vin VARCHAR(17),
    owner VARCHAR(256),
    FOREIGN KEY(owner,car_vin) REFERENCES listings(owner,car_vin) ON DELETE CASCADE,
    unavailable DATE NOT NULL,
    PRIMARY KEY(car_vin,unavailable)
);

CREATE TABLE IF NOT EXISTS rentals(
    owner VARCHAR(256) REFERENCES customer(email) DEFERRABLE,
    renter VARCHAR(256) REFERENCES customer(email) DEFERRABLE,
    car_vin VARCHAR(17),
    pick_up DATE,
    drop_off DATE NOT NULL,
    CONSTRAINT chk_date CHECK (pick_up <= drop_off),
    rental_fee NUMERIC NOT NULL,
    PRIMARY KEY (car_vin,pick_up),
    FOREIGN KEY (owner,car_vin) REFERENCES listings(owner,car_vin)
);