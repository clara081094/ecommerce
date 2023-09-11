# Ecommerce documentation

## Introduction

This is the documentation for the Tech Challenge. This documentation provides access to the various APIs presented in the Ecommerce project.

## Table of Contents

- [Getting Started](#getting-started)
- [Endpoints](#endpoints)
  - [Resource 1](#resource-1)
  - [Resource 2](#resource-2)
  - [Resource 3](#resource-3)
  - [Resource 4](#resource-4)
- [Deploy](#deploy)

## Getting Started

To start using this API, you'll need to follow these steps:

1. **Authentication**: [This project do not use authentication]

## Endpoints

### Resource 1

- **Endpoint**: `/api/cart`
- **Description**: [This endpoint is used to create a cart by providing the `user_code` of an existing user.]
- **HTTP Method**: POST
- **Parameters**: None
- **Request**:
  - `user_code`: [Is the code of an existed user in table user]
- **Response**:
  - `HTTP Response`: 201 Created
  - `Body`:
      {
          "id": 1,
          "user": 1,
          "products": []
      }

### Resource 2

- **Endpoint**: `cart/<cart_id>/product`
- **Description**: [This endpoint is used to add an item to the cart. If the quantity is not specified, it defaults to 1]
- **HTTP Method**: POST
- **Parameters**: None
- **Request**:
  - `product_id`: [Is the id of an existed product in table product]
  - `quantity`: [Is the quantity for the selected product]
- **Response**:
  - `HTTP Response`: 201 Created
  - `Body`:
      {
          "id": 1,
          "product": {
              "id": 3,
              "name": "Personal Computer",
              "price": "220.00",
              "category_id": 2
          },
          "quantity": 5
      }
### Resource 3

- **Endpoint**: `cart/<cart_id>/product/<int:product_id>`
- **Description**: [This endpoint is used to modify the quantity of an existed product in a cart]
- **HTTP Method**: PUT
- **Parameters**: None
- **Request**:
  - `quantity`: [Is the new quantity for the selected product]
- **Response**:
  - `HTTP Response`: 201 Created
  - `Body`:
      {
          "id": 1,
          "product": {
              "id": 3,
              "name": "Personal Computer",
              "price": "220.00",
              "category_id": 2
          },
          "quantity": 2
      }

### Resource 4

- **Endpoint**: `order`
- **Description**: [This endpoint is used to create a cart by providing the `user_code` of an existing user.]
- **HTTP Method**: POST
- **Parameters**: None
- **Request**:
  - `user_code`: [Is the code of an existed user in table user]
- **Response**:
  - `HTTP Response`: 201 Created
  - `Body`:
      {
        "id": 1,
        "cart": {
            "id": 1,
            "user": 1,
            "products": [3]
        },
        "total_product": 2.0,
        "total_discount": 0.0,
        "total_shipping": 5.0,
        "total_order": 435.0
      }

## Deploy

To deploy the entire application, ensure that you have Docker and Docker Compose installed on your operating system. Once installed, navigate to the root directory of the project and run the following command: `docker-compose up -d`. 
This command initiates the deployment process, it starts both the Django project and a PostgreSQL container, making them readily available for be used. Additionally, the deployment includes a script that populates specific tables in the Ecommerce database, providing essential data for the application.
