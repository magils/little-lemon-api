# Little Lemon API


# IMPORTANT - READ THIS BEFORE YOU DO ANYTHING!!!

### - THIS PROJECT USES JWT AUTH, NOT DRF TOKEN, THE AUTH ENPDOINT IS `http://localhost:8000/api/auth/jwt/create/` AND THE AUTH HEADER IS `Bearer <JWT-TOKEN>`.

### AUTH PAYLOAD:
```
{
    "username": "manager_1",
    "password": "sweet-l3m0n!"
}
```

### RESPONSE:

```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4Nzc5NTM2OSwiaWF0IjoxNjg3NzA4OTY5LCJqdGkiOiI1MTFmNmZjMjE0OTQ0ODg2YjA2YzRmOTQ2NjdlMWFiMCIsInVzZXJfaWQiOjN9.HWF1bywj0RugGvojXrfc2_yMhNO--8NGECDFJD4pNik",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg3NzE2MTY5LCJpYXQiOjE2ODc3MDg5NjksImp0aSI6IjQ2YzFhZjY1Y2FkOTQ2NTE4Yjc3ODVmY2NmODU0MDQ4IiwidXNlcl9pZCI6M30.cIZWA20jIqQUtBkCURMdOpA5WDJSw4VqJ4h-CPs7Hf4"
}
```

### USE THE TOKEN ON `access` PROPERTY. 

### - USE POSTMAN AND IMPORT THE COLLECTION. ALL ENDPOINTS ARE CREATED AND CLASSIFIED BY TYPE: AUTH, MENUITEMS, ORDERS, GROUP,CART, ETC.

### - IF YOU USE THE POSTMAN COLLECTION INCLUDED, YOU ONLY NEED TO EXECUTE ANY OF THE `Get Token for ` ENDPOINTS IN THE `Auth` FOLDER AND IT WILL AUTOMATICALLY SET THE HEADER FOR ALL REQUESTS. IF NOT, YOU NEED TO SET THE AUTHORIZATION HEADER IN ALL REQUESTS FOR EACH USER.


Resources:

- Postman collection with all endpoints
- Database with loaded Menu items and users


### How to use it

- Create venv and install `requeriments.txt`
- Import Postman collection into Postman.
- Run the API

### Test users 
- delivery_1
- delivery_2
- manager_1
- manager_2
- customer_1
- admin

### NOTE: `admin` user is the same for django admin portal.

Password for all of them:  `sweet-l3m0n!`
