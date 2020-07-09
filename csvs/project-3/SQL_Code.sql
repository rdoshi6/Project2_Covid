

/* Create Database */

CREATE DATABASE covid_tracking;

/* Select Databse */

USE covid_tracking;

/* CREATE Counties Data Table */

-- Define table schema
CREATE TABLE counties_data (
	Date Date,
    County VARCHAR(50),
    State VARCHAR(50),
    FIPS CHAR(5),
    Cases INT,
    Deaths INT
);

-- Import Data Using Import Wizard Tool Into Counties_Data table

-- Check Table
select *
from counties_data
limit 10;


/* Create Time Series Data Table */

-- Define table schema - unipivoted (final destination)
CREATE TABLE time_series_data (
	UID VARCHAR(10),
    iso2 VARCHAR(2),
    iso3 VARCHAR(3),
    code3 VARCHAR(3),
    FIPS VARCHAR(10),
    Admin2 VARCHAR(41),
    Province_State VARCHAR(24),
    Country_Region VARCHAR(2),
    Latitude FLOAT,
    Longitude FLOAT,
    Combined_Key VARCHAR(55),
    Date DATE,
    Cases INT
);

-- Import Data Using Import Wizard Tool Into Time_Series_Data table

-- Check Table
select *
from time_series_data
limit 10;
