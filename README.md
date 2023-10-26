<div align="center">
<img width="30%" src="https://github.com/mahmoudhaney/Jobs/assets/83553963/b6d3c7b7-1f2f-4981-8c1b-5552eb0546cc">
</div>

## Introduction
Whether you're just starting out in your career, looking for a change, or trying to advance to the next level, we have thousands of jobs to choose from in various industries and locations.

Our easy-to-use search tools make finding jobs matching your skills and interests simple. And with our advanced filtering options, you can narrow down your search results to find the perfect job for you.

Once you've found a few jobs you're interested in, you can easily apply online or contact the employer directly. We also offer a variety of resources to help you prepare for your job search, including resume and cover letter writing tips, interview advice, and more.

## Features
- Users
  - Thousands of jobs to choose from
  - Easy-to-use search tools
  - Advanced filtering options
  - Easy online applications and update or withdraw them
  - Operations on your own profile (Edit Profile, Change Password, Reset Password, etc.)
- Admins
  - Operations on Jobs Categories (Post, Edit, Update, Delete, etc.)
  - Operations on Jobs (Post, Edit, Update, Delete, etc.)
  - List all job Applications.

## Technologies
- `Django 4.2.5`
- `django-filter 23.3`
- `Pillow 10.0.1`
- `python-decouple 3.8`
- `django-rest-passwordreset 1.3.0`
- DB `sqlite` - `sqlparse 0.4.4`


## Setup

- Clone the repository using the command below:
```bash
git clone https://github.com/mahmoudhaney/Jobs.git

```

- Move into the directory where the applications installed 

- Create a virtual environment:
```bash
# Let's install virtualenv first
pip install virtualenv

# Then we create our virtual environment
virtualenv env_name

```

- Activate the virtual environment:
```bash
env_name\scripts\activate

```

- Install the requirements:
```bash
pip install -r requirements.txt

```

- To run the App, we use:
```bash
python manage.py runserver

```

> ⚠ Then, the development server will be started at http://127.0.0.1:8000/

#

## How To Use
After running the server you can use [Postman](https://www.postman.com/downloads/) to try the APIs
1. Open Postman
2. Import the [APIs File](JobBoard.postman_collection.json) into your workspace
3. Use APIs to add some Users, Categories, Jobs, and Applications
#### Example
If you want to Register, then navigate to the Endpoit Signup, set the required fields, and then click send
![image](https://github.com/mahmoudhaney/Jobs/assets/83553963/422f2b7d-a481-4b91-8742-8f8b48ea9fdc)

> ⚠ You can choose whatever you want to run the System APIs

## Copyrights
> ⚠ Copyright ©2023 All rights reserved

