# cep-web-service
A Flask web service to handle CEP data
[![Build Status](https://travis-ci.org/IuryAlves/cep-web-service.svg?branch=master)](https://travis-ci.org/IuryAlves/cep-web-service) [![Coverage Status](https://coveralls.io/repos/IuryAlves/cep-web-service/badge.svg?branch=master&service=github)](https://coveralls.io/github/IuryAlves/cep-web-service?branch=master) [![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)


# Installing

* Install python 3
* Install virtualenv

        pip install virtualenv

* Create a virtualenv

        virtualenv venv --python=python3
        source venv/bin/activate
        
* Install requirements

        pip install -r requirements/requirements.txt
        
##### You will also need to install mongodb. [Here](https://docs.mongodb.org/manual/installation/) is some good documentation about mongo installation.

After the installation you will need to create a folder to mongo store the data, usually is in /data/db

       sudo mkdir -p /data/db # unix only
       
And Start mongo

       sudo mongod
       
If you don't have sudo permissions or don't want use sudo, you can specify the ```--dbpath``` to mongo
        
        mkdir -p data/db # in any directory you like
        mongod --dbpath data/db


## Running

With virtualenv active do

    python cep_web_service/run.py
    
**By default the project runs on port** ```5000``` **and host** ```localhost```

You can change this configuration by modifying the ```cep_web_service/settings.py``` file

The same is valid for mongo instance

## API

**Title**
----
  Creates a new document with info about a zipcode

* **URL**

        /zipcode/ 

* **Method:**
    
         `POST`

* **Data Params**
* 
    **Required:**
 
           `zip_code=[string]`

* **Success Response:**
 
      * **Code:** 201 CREATED
 
* **Error Response:**

      * **Code:** 422 UNPROCESSABLE ENTRY
      * **Content:**
                {
                    "message": "zip code 14020214260 is invalid"
                }
      
      OR
      
      * **Code:** 400 BAD REQUEST

* **Sample Call:**

        curl --data="zip_code=14020260" localhost:5000/zipcode/
        
**Title**
----
  Gets a zip code document or a list of zipcodes documents

* **URL**

        /zipcode/

* **Method:**
    
         GET
         
*  **URL Params**

    **Optional: If limit param is provided**
 
           zip_code=[string]

* **Data Params**

    **Optional: if zip_code param is provided**
 
           limit=[integer]

* **Success Response:**
      
      If zip_code
      
      * **Code:** 200 OK
      * **Content:** 
      
        {
            "address": "Avenida Presidente Vargas", 
            "city": "Ribeirão Preto", 
            "neighborhood": "Jardim América", 
            "state": "São Paulo", 
            "zip_code": "14020260"
        }
        
      If limit
      
      * **Code:** 200 OK
      * **Content:** 
      
                [
            {
                "address": null, 
                "city": "São Paulo", 
                "neighborhood": "Bela Vista", 
                "state": "São Paulo", 
                "zip_code": "01310909"
            }, 
            {
                "address": "Avenida Presidente Vargas", 
                "city": "Ribeirão Preto", 
                "neighborhood": "Jardim América", 
                "state": "São Paulo", 
                "zip_code": "14020260"
            }
         ]

        
* **Error Response:**

      * **Code:** 400 BAD REQUEST
      * **Content:**
                {
                    "message": "You must provide the limit or zip_code."
                }
         
      OR
   
      * **Code:** 404 NOT FOUND
      * **Content:**
                {
                    "message": "zip code 3232 not found."
                }


* **Sample Call:**

        curl localhost:5000/zipcode/14020260
        curl localhost:5000/zipcode/?limit=10
        

* **Notes:**

If the quantity of documents is lower than the limit, the server will return all the documents


**Title**
----
  Deletes a zipcode document

* **URL**

        /zipcode/

* **Method:**
    
         DELETE
         
*  **URL Params**

    **Required:**
 
           zip_code=[string]


* **Success Response:**
            
      * **Code:** 204 NO CONTENT
        
        
* **Error Response:**

      * **Code:** 400 BAD REQUEST
      * **Content:**
                {
                    "message": "You must provide a zip_code."
                }
         
      OR
   
      * **Code:** 404 NOT FOUND
      * **Content:**
                {
                    "message": "zip code 3232 not found."
                }
    

* **Sample Call:**

        curl -X DELETE localhost:5000/zipcode/14020260
