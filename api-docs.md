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
- Mengecek server berjalan
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
- Menambahkan produk

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

1. Mengurutkan berdasarkan produk terbaru
    - **/products?query=date_added&sort=newest**
2. Mengurutkan berdasarkan harga produk termurah
    - **/products?query=price&sort=lowest**
3. Mengurutkan berdasarkan harga produk termahal
    - **/products?query=price&sort=highest**
4. Mengurutkan berdasarkan nama produk (a-z)
    - **/products?query=name&sort=a-z**
5. Mengurutkan berdasarkan nama produk (z-a)
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