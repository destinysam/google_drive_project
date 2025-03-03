## Welcome 


## Steps to setup project

### 1. Let's clone the project first

```
git clone https://github.com/destinysam/google_drive_project.git
```

### 2. Setup Environment(Linux) using virtualenv and activate environment

```
python3 -m venv env
source env/bin/activate
```

### 3. Now let's install project requirements

```
pip install -r requirements.txt
```

### 4. Let's setup env.development file for local use ('development' for local and 'production' for production)

```
export DJANGO_ENV=development
```

### 5. Update all configurations for .env.development

### 6. Run makemigrations to check database changes

```
python3 manage.py makemigrations
```

### 7. Migrate the database changes

```
python3 manage.py migrate
```

### 8. Finally, our project is ready to serve

```
python3 manage.py runserver
```

## API's

Note: {{local}},{{heroku}} where   local=http://127.0.0.1:8000 (local) and heroku=https://enfundproject-c7c26273b6ed.herokuapp.com (deployed)
represents our host address 


### 1. For google Oauth2 login use(Best use browser)

#### Request method POST

```
{{local}}/auth/login/
```

### 2. To upload file to google drive

#### Request method POST


```
{{local}}/upload/
```

####   Query Params

```
user : example@gmail.com (use email of the current user which you used to login above)
```

#### form-data

```
file : choose any file to upload
```

### 3. To List Drive Files

#### Request method GET

```
{{local}}/list_drive_files/
```

#### Query params

```
user : example@gmail.com (use email of the current user which you used to login above)
```

### 4. Download files from google drive (please spacify the google drive file id before sending request)

#### Request method GET

```
{{local}}/download_drive_file/<GOOGLE_DRIVE_FILE_ID/
```

#### Query params

```
user : example@gmail.com (use email of the current user which you used to login above)
```

### 5. Finally messaging api(Best use browser)

#### Request method GET

Note: To test messaging between two or more users.You can open the same url in two tabs or two browsers(Best use case) once you open, a popup will be shown
to enter the room name.Use same room name to start chating.

```
{{local}}/chat/
```
###  Postman Collection Link

```
https://drive.google.com/file/d/1_t6xihAOp2waNtR2TU3wuYmK8H51DoBw/view?usp=sharing
```
### App deployed at Heroku

```
https://enfundproject-c7c26273b6ed.herokuapp.com
```



Thanks for reading
