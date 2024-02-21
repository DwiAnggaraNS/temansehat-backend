# TemanSehat Backend RESTful API Documentation

## 1. Introduction

Welcome to the documentation for the Backend RESTful API of the TemanSehat mobile app. This backend serves as the foundation for the TemanSehat mobile app, which is developed for the Google Solution Challenge. TemanSehat is a community mental health app designed to create a supportive space for individuals to express their thoughts and feelings openly. The app focuses on attentive listening, positive support, and providing a nurturing environment for users to build meaningful connections. To ensure a supportive and non-toxic community, the TemanSehat mobile app utilizes the Google Cloud Platform's REST API for Natural Language Processing (NLP) to assess sentiment in user comments.

**Note**: TemanSehat mobile app is integrated with Google Cloud Platform's REST API Natural Language Processing (NLP) in the Mobile App Frontend for NLP to evaluate sentiment in each post comment, fostering a supportive and non-toxic community.

## 2. Getting the Backend Repository

To access the Backend RESTful API repository, follow these steps:

- Clone the repository from GitHub:

    ```bash
    git clone https://github.com/your-username/teman-sehat-backend.git
    ```

## 3. Setting Up the Backend Server

To activate the backend server, follow these steps:

### 3.1. Install Dependencies

Navigate to the project folder and install the required dependencies from the `requirements.txt` file:

```bash
cd teman-sehat-backend
pip install -r requirements.txt
```

### 3.2. Create a Virtual Environment

Create a virtual environment to isolate dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

- **On Windows:**
    ```bash
    venv\Scripts\activate
    ```
- **On Unix or MacOS:**
    ```bash
    source venv/bin/activate
    ```

### 3.3. Configure `config.json`

Create a `config.json` file in the same directory as `config.py` and fill it with the following format:

```json
{
    "SECRET_KEY": "your_secret_key",
    "JWT_SECRET_KEY": "your_jwt_secret_key",
    "DATABASE_USER_PASSWORD": "your_database_password",
    "MAIL_PASSWORD": "your_mail_password"
}
```

### 3.4. Update `config.py`

Configure the `SQLALCHEMY_DATABASE_URI` in the `config.py` file with your database URL.

### 3.5. Run the Backend Server

Execute the `main.py` file to start the backend server:

```bash
python main.py
```

The backend server will now be active.

Feel free to reach out if you have any questions or encounter issues. Good luck with your TemanSehat project for the Google Solution Challenge!

## 4. API Documentation

### Sign Up
- **Endpoint:** `/api/users`
- **Method:** `POST`
- **Parameters:**
  - `username` (str)
  - `password` (str)
  - `email` (str)
- **Status Codes:**
  - Success: 200
  - Account creation failure: 500
  - Email already in use: 409
  - Username already taken: 404

### Login
- **Endpoint:** `/api/users/login`
- **Method:** `POST`
- **Parameters:**
  - `username` (str)
  - `password` (str)
  - `remember` (boolean)
- **Status Codes:**
  - Success: 200
  - Incorrect password: 401
  - Username not found: 404
- **Response:**
  - JWT token

### Edit Profile
- **Endpoint:** `/api/users`
- **Method:** `PUT`
- **Parameters:**
  - `user_id` (str, required)
  - `username` (str, optional)
  - `password` (str, required if `new_password` parameter is provided)
  - `new_password` (str, optional)
  - `pfp` (str base64, optional)
  - `bio` (str, optional)
  - `email` (str, optional)
- **Header:** JWT token
- **Status Codes:**
  - Success: 200
  - Incorrect password: 401
  - Email already in use: 409

### Get Account's Information
- **Endpoint:** `/api/users/<user_id>`
- **Method:** `GET`
- **Header:** JWT token
- **Status Codes:**
  - Success: 200
  - Account not found: 404
- **Response:**
  ```json
  {
    "username": "string",
    "bio": "string",
    "email": "string",
    "pfp": "string base64"
  }
  ```

### Delete Account
- **Endpoint:** `/api/users`
- **Method:** `DELETE`
- **Header:** JWT token
- **Parameters:**
  - `user_id` (str, required)
- **Status Codes:**
  - Success: 200
  - Account not found: 404

### Forgot Password
#### Step 1: Send Account Data
- **Endpoint:** `/api/users/forgotpw`
- **Method:** `POST`
- **Parameters:**
  - `username` (str, required)
  - `email` (str, required)
- **Status Codes:**
  - Success: 200
  - Account not found: 404
  - Email does not match username: 401
- **Response:**
  - Send a unique token to the user's email with a 5-minute expiration.

#### Step 2: Send Token to TemanSehat App
- **Endpoint:** `/api/users/forgotpw/sendtoken`
- **Method:** `POST`
- **Parameters:**
  - `token` from the user (str, required)
- **Status Codes:**
  - Success: 200
  - Token incorrect or expired: 404
- **Response:**
  - User ID of the account

#### Step 3: Change Password
- **Endpoint:** `/api/users/forgotpw`
- **Method:** `PUT`
- **Parameters:**
  - `new_password` (str, required)
- **Status Codes:**
  - Success: 200
  - Account not found: 404

### Post Daily Mood for User
- **Endpoint:** `/api/users/moods`
- **Method:** `POST`
- **Header:** JWT token
- **Parameters:**
  - `user_id` (str, required)
  - `feeling` (str, required)
  - `story` (str, required)
- **Status Codes:**
  - Success: 201
  - Failure: 500

### Get Mood History from Individual User
- **Endpoint:** `/api/users/moods/<user_id>`
- **Method:** `GET`
- **Header:** JWT token
- **Status Codes:**
  - Success: 200
  - Failure: 500
- **Response:**
  ```json
  {
    "mood_Id": {
      "feeling": "string",
      "story": "string",
      "mood_date": "date"
    },
    "mood_Id": {
      "feeling": "string",
      "story": "string",
      "mood_date": "date"
    },
    // and so on
  }
  ```

### Create Post
- **Endpoint:** `/api/users/posts`
- **Method:** `POST`
- **Header:** JWT token
- **Parameters:**
  - `user_id` (str, required)
  - `title` (str, required)
  - `desc` (str, required)
  - `pictures` (list of str base64, optional)
- **Status Codes:**
  - Success with image: 201
  - Success without image: 200
  - Account not found: 404

### Delete Post
- **Endpoint:** `/api/users/posts`
- **Method:** `DELETE`
- **Header:** JWT token
- **Parameters:**
  - `post_id` (str, required)
- **Status Codes:**
  - Success: 200
  - Post not found: 404

### Get All Posts from All Accounts
- **Endpoint:** `/api/users/posts`
- **Method:** `GET`
- **Header:** JWT token
- **Status Codes:**
  - Success:

 200
  - Failure: 500
- **Response:**
  ```json
  {
    "post_id": {
      "username": "string",
      "user_pfp": "string base64",
      "post_date": "2024-02-15 10:38:00",
      "title": "string",
      "desc": "string",
      "images": {
        "image_id": {
          "image": "string base64"
        },
        // and so on
      },
      "comment": {
        "comment_id": {
          "username": "string",
          "comment_desc": "string",
          "comment_date": "2024-02-15 21:15:00"
        },
        // and so on
      },
      "total_share": 0,
      "total_like": 0
    },
    // and so on
  }
  ```

### Get Post History from One User
- **Endpoint:** `/api/users/posts/<user_id>`
- **Method:** `GET`
- **Header:** JWT token
- **Status Codes:**
  - Success: 200
  - Failure: 500
- **Response:**
  ```json
  {
    "post_id": {
      "username": "string",
      "user_pfp": "string base64",
      "post_date": "2024-02-15 10:38:00",
      "title": "string",
      "desc": "string",
      "images": {
        "image_id": {
          "image": "string base64"
        },
        // and so on
      },
      "comment": {
        "comment_id": {
          "username": "string",
          "comment_desc": "string",
          "comment_date": "2024-02-15 21:15:00"
        },
        // and so on
      },
      "total_share": 0,
      "total_like": 0
    },
    // and so on
  }
  ```

### Like Post
- **Endpoint:** `/api/users/posts/likes`
- **Method:** `POST`
- **Header:** JWT token
- **Parameters:**
  - `user_id` (str, required)
  - `post_id` (str, required)
  - `like` (boolean, True = like, False = unlike)
- **Status Codes:**
  - Success: 200
  - Failure: 500

### Share Post
- **Endpoint:** `/api/users/posts/shares`
- **Method:** `POST`
- **Header:** JWT token
- **Parameters:**
  - `user_id` (str, required)
  - `post_id` (str, required)
  - `share` (boolean, True = share)
- **Status Codes:**
  - Success: 200
  - Failure: 500

### Post Comment on a Post
- **Endpoint:** `/api/users/posts/comments`
- **Method:** `POST`
- **Header:** JWT token
- **Parameters:**
  - `user_id` (str, required)
  - `post_id` (str, required)
  - `comment_desc` (str, required)
- **Status Codes:**
  - Success: 200
  - Account or post not found: 404
