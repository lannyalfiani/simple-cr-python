# simple-cr-python

## Overview
A simple Create and Read (hence cr) python REST API project with Postgre. Architecture design chosen is REST and monolithic , as it uses JSON as the data response and the system is quite simple.

_Disclaimer: This is the first time ever I'm using python (learned on the go)_

---

## How to Use
1. Clone this project
2. Create a new virtual environment in python3 
    ```
      python3.10 -m venv venv
    ```
3. Activate the virtual environment
    ```
        source venv/bin/activate
    ```
3. Install all dependencies 
    ```
      pip install -r requirements.txt
    ```
4. Create a database in postgre with `product` as the name
    - Once you run the project, the migration and table creation will run by itself
5. Create a `.env` file
    - Copy paste the content from `.env.template` file
    - Fill in `SECRETKEY` as anything you wish (no need to change anything for the rest)
6. Run the project
    ```
      python app.py
    ```
7. Try the available endpoints (refer to api documentation)


---

Notes: Docker is also available.
