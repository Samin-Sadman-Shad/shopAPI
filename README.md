# shopAPI
Services
Manager:

The manager can assign users to the manager group.
Users can access the manager group with an admin token.
The manager can add shopping items.
The manager can add categories for shopping items.
Managers can log in.
Managers can update the item of the day (Featured item).
Managers can assign users as the delivery crew.
Managers can assign orders placed by customers to the delivery crew.
Customer:

Customers can log in using their username and password and get JWT access tokens to register.
Customers can browse all categories.
Customers can browse all the shopping items at once.
Customers can browse shopping items by category, price, and title of the item.
Customers can paginate menu items, categories.
Customers can sort items by price.
Customers can add menu items to the cart.
Customers can access previously added items in the cart.
Customers can place orders.
Customers can browse their own orders.
Delivery Crew:

The delivery crew can access orders assigned to them.
The delivery crew can update an order as delivered.


Api Endpoints for consumption:
User registration and token generation endpoints
You can use Djoser in your project to automatically create the following endpoints and functionalities for you.

| Endpoint                 | Role                          | Method | Purpose                                                |
|--------------------------|-------------------------------|--------|--------------------------------------------------------|
| /api/users               | No role required              | POST   | Creates a new user with name, email, and password      |
| /api/users/users/me/     | Anyone with a valid user token | GET    | Displays only the current user                         |
| /token/login/            | Anyone with a valid username and password | POST | Generates access tokens that can be used in other API calls in this project |


| Endpoint                   | Role           | Method                | Purpose                                                  |
|----------------------------|----------------|-----------------------|----------------------------------------------------------|
| /api/menu-items            | Customer, Delivery Crew | GET                   | Lists all menu items. Return a 200 – Ok HTTP status code |
| /api/menu-items            | Customer, Delivery Crew | POST, PUT, PATCH, DELETE | Denies access and returns 403 – Unauthorized HTTP status code |
| /api/menu-items/{menuItem} | Customer, Delivery Crew | GET                   | Lists single menu item                                   |
| /api/menu-items/{menuItem} | Customer, Delivery Crew | POST, PUT, PATCH, DELETE | Returns 403 - Unauthorized                               |
|                            |                |                       |                                                          |
| /api/menu-items            | Manager        | GET                   | Lists all menu items                                     |
| /api/menu-items            | Manager        | POST                  | Creates a new menu item and returns 201 - Created        |
| /api/menu-items/{menuItem} | Manager        | GET                   | Lists single menu item                                   |
| /api/menu-items/{menuItem} | Manager        | PUT, PATCH             | Updates single menu item                                 |
| /api/menu-items/{menuItem} | Manager        | DELETE                | Deletes menu item                                        |

| Endpoint                           | Role    | Method | Purpose                                                                                     |
|------------------------------------|---------|--------|---------------------------------------------------------------------------------------------|
| /api/groups/manager/users           | Manager | GET    | Returns all managers                                                                       |
| /api/groups/manager/users           | Manager | POST   | Assigns the user in the payload to the manager group and returns 201-Created              |
| /api/groups/manager/users/{userId}  | Manager | DELETE | Removes this particular user from the manager group and returns 200 – Success if everything is okay. If the user is not found, returns 404 – Not found |
| /api/groups/delivery-crew/users     | Manager | GET    | Returns all delivery crew                                                                   |
| /api/groups/delivery-crew/users     | Manager | POST   | Assigns the user in the payload to delivery crew group and returns 201-Created HTTP        |
| /api/groups/delivery-crew/users/{userId} | Manager | DELETE | Removes this user from the manager group and returns 200 – Success if everything is okay. If the user is not found, returns 404 – Not found |

| Endpoint                 | Role      | Method | Purpose                                              |
|--------------------------|-----------|--------|------------------------------------------------------|
| /api/cart/menu-items     | Customer  | GET    | Returns current items in the cart for the current user token |
| /api/cart/menu-items     | Customer  | POST   | Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items |
| /api/cart/menu-items     | Customer  | DELETE | Deletes all menu items created by the current user token |

| Endpoint                  | Role           | Method | Purpose                                                                                                                         |
|---------------------------|----------------|--------|---------------------------------------------------------------------------------------------------------------------------------|
| /api/orders               | Customer       | GET    | Returns all orders with order items created by this user                                                                        |
| /api/orders               | Customer       | POST   | Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user. |
| /api/orders/{orderId}     | Customer       | GET    | Returns all items for this order id. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code. |
| /api/orders               | Manager        | GET    | Returns all orders with order items by all users                                                                               |
| /api/orders/{orderId}     | Customer       | PUT, PATCH | Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1. If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery. If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered. |
| /api/orders/{orderId}     | Manager        | DELETE | Deletes this order                                                                                                              |
| /api/orders               | Delivery crew  | GET    | Returns all orders with order items assigned to the delivery crew                                                                |
| /api/orders/{orderId}     | Delivery crew  | PATCH  | A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order. |
