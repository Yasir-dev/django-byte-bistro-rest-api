# 🍕 ByteBistro 🍕 API

This is the backend API for the ByteBistro application. It's built with Django and Django Rest Framework as learning project for **Coursera Meta Back-End Developer Professional Certificate.**

## Installation

1. Clone the repository
2. Run `pipenv shell` to start your virtual environment.
3. Run `pipenv install` to install the required dependencies from the Pipfile.
4. Run `python manage.py makemigrations` to create new migrations based on the changes you have made to your models.
5. Run `python manage.py migrate` to apply and unapply migrations.
6. Run `python manage.py runserver` to start the development server.

## Creating Super User and Groups

1. To create a super user, run the following command: `python manage.py createsuperuser`. Follow the prompts to set a username, email, and password for the super user.

2. After creating the super user, start the development server again with `python manage.py runserver`.

3. Navigate to the admin route (`admin/`) in your web browser. Log in using the super user credentials you just created.

4. Once logged in, go to the Groups section and click on "Add Group +".

5. Create two groups: "Manager" and "Delivery Crew". Save each group after creation.


## API Endpoints

Here are the API endpoints provided by the ByteBistro application:

- `admin/`
- `api/logout-all-devices`
- `api/menu-items`
- `api/menu-items/category`
- `api/menu-items/<int:pk>`
- `api/groups/manager/users/`
- `api/groups/manager/users/<int:pk>/`
- `api/groups/delivery-crew/users/`
- `api/groups/delivery-crew/users/<int:pk>/`
- `api/cart/menu-items/`
- `api/orders/`
- `api/orders/<int:pk>`
- `api/login/`
- `api/token/refresh/`
- `api/token/blacklist/`

## Testing API Endpoints

You can use the [Insomnia API client](https://insomnia.rest/products/insomnia) for testing the endpoints.

To get started, download and install Insomnia from the provided link. Once installed, you can import the endpoint collection from the [Insomnia_byte_bistro_api.json](Insomnia_byte_bistro_api.json) file. This file contains pre-configured requests for all the API endpoints and can be used to quickly test and interact with the API.
