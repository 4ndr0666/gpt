openapi: 3.0.0
info:
  title: Pastebin API
  description: API for interacting with Pastebin, including creating pastes, fetching user details, and more.
  version: 1.0.0
servers:
  - url: https://pastebin.com/api
    description: Pastebin API for standard actions
paths:
  /api_post.php:
    post:
      summary: Perform standard Pastebin actions
      operationId: performStandardActions
      description: |
        Perform actions such as creating a paste, deleting a paste, getting user info, and fetching raw paste data.
        Specify the action through the `api_option` parameter.
      requestBody:
        required: true
        content:
          application/x-www-form-urlencoded:
            schema:
              type: object
              properties:
                api_dev_key:
                  type: string
                  description: The developer API key.
                api_user_key:
                  type: string
                  description: The user session key, optional depending on the action.
                api_paste_code:
                  type: string
                  description: The paste content, required for creating a paste.
                api_paste_key:
                  type: string
                  description: The paste key, required for fetching or deleting a specific paste.
                api_option:
                  type: string
                  description: Determines the action to perform.
              required:
                - api_dev_key
                - api_option
      responses:
        "200":
          description: Action performed successfully.
        "400":
          description: Bad request.
        "403":
          description: Forbidden.
  /api_login.php:
    post:
      summary: Create a new API user key
      operationId: createApiKey
      description: Create a new API user key using username and password.
      requestBody:
        required: true
        content:
          application/x-www-form-urlencoded:
            schema:
              type: object
              properties:
                api_dev_key:
                  type: string
                  description: The developer API key.
                api_user_name:
                  type: string
                  description: The username of the user.
                api_user_password:
                  type: string
                  description: The password of the user.
              required:
                - api_dev_key
                - api_user_name
                - api_user_password
      responses:
        "200":
          description: API key created successfully.
        "403":
          description: Forbidden.

