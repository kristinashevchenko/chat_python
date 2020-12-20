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
    
**4. Create superuser using POST request:**

Add Header:


    key: Authorization
    value: Token <superuser_token>

url: http://127.0.0.1:8000/api/superusers/register

body example: 

    {
        "username": "Kate_admin",
        "password": "12356Kate",
        "email": "kate_admin@mail.com"
    }
    
**5. Login user using POST request:**

url: http://127.0.0.1:8000/api/customers/login

or

url: http://127.0.0.1:8000/api/volunteers/login

or

url: http://127.0.0.1:8000/api/superusers/login

body example: 

    {
        "username": "Kate_cust",
        "password": "12356Kate"
    }
    
**6. Logout user using POST request:**

Add Header:


    key: Authorization
    value: Token <user_token>

url: http://127.0.0.1:8000/api/customers/logout

or

url: http://127.0.0.1:8000/api/volunteers/logout

or

url: http://127.0.0.1:8000/api/superusers/logout

**7. Update/delete/get customer/volunteer using PUT(PATCH)/DELETE/GET request:**

Add Header:

    key: Authorization
    value: Token <superuser_token>
    
url (GET): http://127.0.0.1:8000/api/customers

or

url (GET): http://127.0.0.1:8000/api/volunteers

or

url (PUT, PATCH, GET, DELETE): http://127.0.0.1:8000/api/customers/<customer_id>

or

url (PUT, PATCH, GET, DELETE): http://127.0.0.1:8000/api/volunteers/<volunteer_id>

body example: 

    {
       "email": "2@1.com"
    }

**8. Add/update/delete/get animal type using POST/PUT(PATCH)/DELETE/GET request:**

Add Header:

    key: Authorization
    value: Token <volunteer_token>
    
url (POST, GET): http://127.0.0.1:8000/api/animals

url (PUT, PATCH, GET, DELETE): http://127.0.0.1:8000/api/animals/<animal_id>

body example: 

    {
       "animal_type": "Cat"
    }
              
**9. Add pet using POST request:**

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

**10. To update pet information use PUT/PATCH request:**

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
    
**11. To show all pets or one pet use GET request:**

Add Header:
    
    key: Authorization
    value: Token <user_token>
    
URL: http://127.0.0.1:8000/api/pets

or

URL: http://127.0.0.1:8000/api/pets/<pet_id>

**12. To sort pets use GET request with query params:**
    
URL with one param: http://127.0.0.1:8000/api/pets?key=value

URL: http://127.0.0.1:8000/api/pets?key=value&key=value
    
E.g:

    sex=M
    sort_age=ASC
    sort_date=DESC
    type=Cat
    

**13. To create request on pet use POST request:**

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
    
**14. To update pet request use PUT/PATCH request:**

Add Header:
    
    key: Authorization
    value: Token <volunteer_token>
    
url: http://127.0.0.1:8000/api/pet_request/<pet_request_id>

Body example:
    
    {
        "pet": "2",
        "date_arrive": "06-01-2021"
    }
    

**15. To show all requests or one request use GET request:**

Add Header:
    
    key: Authorization
    value: Token <volunteer_token>
    
URL: http://127.0.0.1:8000/api/pet_request

or 

URL: http://127.0.0.1:8000/api/pet_request/<pet_request_id>


**16. To delete pet request use DELETE request. You can delete requests only with 'C'/'N' status:**

Add Header:
    
    key: Authorization
    value: Token <volunteer_token>
    
URL: http://127.0.0.1:8000/api/pet_request/<pet_request_id>
