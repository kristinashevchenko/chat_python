**Pet shelter documentation**

**1. Run:**

`python manage.py makemigrations`

`python manage.py migrate`
   
Create superuser using next command:`python manage.py createsuperuser`

To run app use next command: `python manage.py runserver`

**2. Create volunteer using POST request:**

Add Header:


    key: Authorization
    value: Token <superuser_token>

url: http://127.0.0.1:8000/api/volunteers/register

body example: 

    {
        "username": "Kate_volont",
        "password": "12356Kate",
        "email": "kate_volont@mail.com"
    }
              
**3. Create customer using POST request:**

url: http://127.0.0.1:8000/api/customers/register

body example: 

    {
        "username": "Kate_cust",
        "password": "12356Kate",
        "email": "kate_cust@mail.com"
    }

**4. Add animal type using POST request:**

Add Header:

    key: Authorization
    value: Token <volunteer_token>
    
url: http://127.0.0.1:8000/api/animals

body example: 

    {
       "animal_type": "Cat"
    }
              
**5. Add pet using POST request:**

Add Header:
    
    key: Authorization
    value: Token <volunteer_token>
    
url: http://127.0.0.1:8000/api/pets

Date format: DD-MM-YYYY

Type is animal_type id

If you don't know exact date, set 01-01 as DD-MM

Sex: type 'F' to set Female, 'M' to set Male

Fields: name, type, date_of_appear, date_of_birth, sex, has_vaccination, is_sterilized, is_prioritized, additional_info, photo_url, breed

body example: 

    {
        "name": "Cassy",
        "type": "1",
        "date_of_appear": "15-11-2020",
        "date_of_birth": "25-01-2018",
        "sex": "F"
    }

**6. To update pet information use PUT request:**

Add Header:
    
    key: Authorization
    value: Token <volunteer_token>
    
url: http://127.0.0.1:8000/api/pets/<pet_id>

Update/add smth to body: 

    {
        "name": "Cassy",
        "type": "1",
        "date_of_appear": "29-11-2020",
        "date_of_birth": "25-01-2018",
        "sex": "F",
        "breed": "Scottish"
    }
    
**7. To show all pets use GET request:**
    
URL: http://127.0.0.1:8000/api/pets

**8. To sort pets use GET request:**
    
URL with one param: http://127.0.0.1:8000/api/pets?key=value

URL: http://127.0.0.1:8000/api/pets?key=value&key=value
    
E.g:

    sex=M
    sort_age=ASC
    sort_date=DESC
    type=Cat
    

**9. To create request on pet use POST request:**

Add Header:
    
    key: Authorization
    value: Token <customer_token>
    
url: http://127.0.0.1:8000/api/pet_request

Date format: DD-MM-YYYY

Fields: pet (pet_id), date_arrive, comment, status

Status can be: 

    'A' - Active,
    'C' - Closed,
    'N' - Non-appearance

Body example:
    
    {
        "pet": "1",
        "date_arrive": "05-01-2021"
    }
    

**10. To show all requests use GET request:**

Add Header:
    
    key: Authorization
    value: Token <volunteer_token>
    
URL: http://127.0.0.1:8000/api/pet_request
