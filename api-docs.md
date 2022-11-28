# Daftar endpoint yang tersedia

1. GET /
2. POST /products
3. GET /products?query={object}&sort={tipe-sort}
    1. GET /products?query=date_added&sort=newest
    2. GET /products?query=price&sort=lowest
    3. GET /products?query=price&sort=highest
    4. GET /products?query=name&sort=a-z
    5. GET /products?query=name&sort=z-a

---

## 1. GET /
### Description
- To check if the server is running
#### Response
_Response 200 - OK_
- Body
    ```json
      {
          "message": "Hello World, server is up!"
      }
  ```


## 2. POST /products
### Description
- Add a new prodict

#### Request

- Body
    ```json
    {
        "name": String,
        "price": Integer,
        "description": String,
        "quantity": Integer
    }
    ```


#### Response
_Response 201 - Created_
- Body
    ```json
      {
          "message": "Success adding {name} as a new product",
      }
  ```
_Response 400 - Bad Request_
- Body
  ```json
    {
        "message": "Please fill in all required fields!"
    }
    ```


 <br> 

---

 <br> 

## 2. GET /products?query={object}&sort={tipe-sort}

1. Sort products from newest to oldest
    - **/products?query=date_added&sort=newest**
2. Sort products from lowest price
    - **/products?query=price&sort=lowest**
3. Sort products from highest price
    - **/products?query=price&sort=highest**
4. Sort products by its name (a-z)
    - **/products?query=name&sort=a-z**
5. Sort products by its name (z-a)
    - **/products?query=name&sort=z-a**

#### Response
_Response 200 - OK_
- Body
    ```json
      [
        {
          "date_added": String,
          "description": String,
          "id": Integer,
          "name": String,
          "price": Integer,
          "quantity": Integer
        },
        ...
      ]
  ```
---

## Global Error
#### Response
_500 - Internal Server Error_
- Body
    ```json
    {
        "message": "Something went wrong! {error message}"
    }
    ```

_400 - Bad request_
- Body
    ```json
    {
        "message": "Bad request, query string is not recognised!"
    }
    ```