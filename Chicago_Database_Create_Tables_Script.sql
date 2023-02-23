------------------------------------------
--DDL statement for table 'HR' database--
--------------------------------------------

-- Drop the tables in case they exist

DROP TABLE CENSUS_DATA;
DROP TABLE CHICAGO_PUBLIC_SCHOOLS;
DROP TABLE CHICAGO_CRIME_DATA;

-- Create the tables

CREATE TABLE CENSUS_DATA (								

                          COMMUNITY_AREA_NUMBER CHAR(9) NOT NULL,
                          COMMUNITY_AREA_NAME VARCHAR(25) NOT NULL,
                          PERCENT_OF_HOUSING_CROWDED DECIMAL(10,2),
                          PERCENT_HOUSEHOLDS_BELOW_POVERTY DECIMAL(10,2),
                          PERCENT_AGED_16__UNEMPLOYED DECIMAL(10,2),
                          PERCENT_AGED_25__WITHOUT_HIGH_SCHOOL_DIPLOMA DECIMAL(10,2),
                          PERCENT_AGED_UNDER_18_OR_OVER_64 DECIMAL(10,2),
                          PER_CAPITA_INCOME DECIMAL(10,2),
                          HARDSHIP_INDEX DECIMAL(10,2),
                          PRIMARY KEY (EMP_ID)
                        );

CREATE TABLE CHICAGO_PUBLIC_SCHOOLS (
                            EMPL_ID CHAR(9) NOT NULL,
                            START_DATE DATE,
                            JOBS_ID CHAR(9) NOT NULL,
                            DEPT_ID CHAR(9),
                            PRIMARY KEY (EMPL_ID,JOBS_ID)
                          );

CREATE TABLE CHICAGO_CRIME_DATA (
                    JOB_IDENT CHAR(9) NOT NULL,
                    JOB_TITLE VARCHAR(30) ,
                    MIN_SALARY DECIMAL(10,2),
                    MAX_SALARY DECIMAL(10,2),
                    PRIMARY KEY (JOB_IDENT)
                  );