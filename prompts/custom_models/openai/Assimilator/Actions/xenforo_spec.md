openapi: 3.0.0
info:
  title: XenForo Admin API
  description: API for managing XenForo forum software through admin functions.
  version: 1.0.0
servers:
  - url: https://1e1ba522e9f490e6.demo-xenforo.com/2215/admin.php
    description: XenForo Admin API server
paths:
  /api-keys/:
    get:
      operationId: getApiKey
      summary: Retrieve or confirm creation of a new API key.
      parameters:
        - name: new_key_id
          in: query
          required: true
          schema:
            type: integer
            description: ID for the new API key to retrieve or confirm.
      responses:
        '200':
          description: API key details retrieved successfully.
          content:
            application/json:
              schema: 
                type: object
                properties:
                  keyId:
                    type: integer
                  keySecret:
                    type: string
                required:
                  - keyId
                  - keySecret
        '400':
          description: Bad request, possibly due to invalid parameters.
        '404':
          description: API key not found.

