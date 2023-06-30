## /login

This endpoint handles user authentication. If the request method is GET, it renders the login page. If the request method is POST, it initiates the authentication process and redirects the user to the authentication page.

### Methods

    GET: Renders the login page.
    POST: Initiates the authentication process and redirects the user to the authentication page.

## /userdata [GET]

This endpoint returns the JSON data of the user.

### Authentication

The user must be logged in to access this endpoint.

### Methods

    GET: Returns the JSON data of the user.

## /pfp [GET]

This endpoint returns the profile picture of the user as an image file.

### Authentication

The user must be logged in to access this endpoint.

### Methods

    GET: Returns the profile picture of the user as an image file.

## /doors [GET]

This endpoint returns a list of openable doors.

### Authentication

The user must be logged in to access this endpoint.

### Methods

    GET: Returns a list of openable doors.

## /doors/(door) [GET]

This endpoint opens a specific door.

### Authentication

The user must be logged in to access this endpoint.
Parameters

    door: Specifies the door to open.


### Methods

    GET: Opens the specified door.

## /tasks [GET]

This endpoint returns the tasks assigned to the user.

### Authentication

The user must be logged in to access this endpoint.

### Methods

    GET: Returns the tasks assigned to the user.

## /atasks [GET]

This endpoint returns all tasks assigned by the user.

### Authentication

The user must be logged in to access this endpoint.

### Methods

    GET: Returns all tasks assigned by the user.

## /create_task [POST]

This endpoint creates a new task.

### Authentication

The user must be logged in to access this endpoint.
Parameters

The endpoint expects a form with the following fields:

    assigned_to (user_id): Specifies the user ID to whom the task is assigned.
    description: Specifies the description of the task.
    deadline: Specifies the deadline of the task in the format "%Y-%m-%dT%H:%M".


### Methods

    POST: Creates a new task.

## /marktaskdone [POST]

This endpoint marks a task as done.

### Authentication

The user must be logged in to access this endpoint.
Parameters

The endpoint expects a form with the following fields:

    task_id: Specifies the ID of the task to mark as done.


### Methods

    POST: Marks the task as done.

## /add_experience [POST]

This endpoint adds experience to a completed task.

### Authentication

The user must be logged in to access this endpoint.
Parameters

The endpoint expects a form with the following fields:

    task_id: Specifies the ID of the task to which experience is added.
    experience: Specifies the experience to add.


### Methods

    POST: Adds experience to the task.

## /get_users [GET]

This endpoint returns information about all users.

### Authentication

The user must be logged in and have admin privileges to access this endpoint.

### Methods

    GET: Returns information about all users.

## /add_news [POST]

This endpoint adds news by creating a new entry.
### Authentication

The user must be logged in and have admin privileges to access this endpoint.
### Parameters

The endpoint expects a form with the following fields:

    topic: Specifies the topic of the news.
    title: Specifies the title of the news.
    content: Specifies the content of the news.
    image: Specifies the image file associated with the news.

### Methods

    POST: Adds news by creating a new entry.

## /del_news [POST]

This endpoint deletes news by removing the specified entry.
### Authentication

The user must be logged in and have admin privileges to access this endpoint.
### Parameters

The endpoint expects a form with the following fields:

    news_id: Specifies the ID of the news to delete.

### Methods

    POST: Deletes the specified news entry.

## /news [GET]

This endpoint retrieves news entries.

### Authentication

No authentication is required to access this endpoint.

### Methods

    GET: Retrieves news entries.

## /get_news_image/(news_id) [GET]

This endpoint retrieves the image associated with the specified news entry.

### Authentication

No authentication is required to access this endpoint.

### Parameters

    news_id: Specifies the ID of the news entry.

### Methods

    GET: Retrieves the image associated with the specified news entry.

