# Get current user

GET https://api.fanvue.com/users/me

Get details of the currently authenticated user.

    <Info>Scope required: `read:self`</Info>

Reference: https://api.fanvue.com/docs/api-reference/reference/users/get-current-user

## OpenAPI Specification

```yaml
openapi: 3.1.1
info:
  title: Get current user
  version: endpoint_.getCurrentUser
paths:
  /users/me:
    get:
      operationId: get-current-user
      summary: Get current user
      description: |-
        Get details of the currently authenticated user.

            <Info>Scope required: `read:self`</Info>
      tags:
        - []
      parameters:
        - name: Authorization
          in: header
          description: >-
            Bearer authentication of the form `Bearer <token>`, where token is
            your auth token.
          required: true
          schema:
            type: string
        - name: X-Fanvue-API-Version
          in: header
          description: API version to use for the request
          required: true
          schema:
            type: string
            default: '2025-06-26'
      responses:
        '200':
          description: Current user details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/getCurrentUser_Response_200'
        '400':
          description: API version not supported
          content: {}
        '401':
          description: Unauthorized Response
          content: {}
        '403':
          description: Unauthorized Response
          content: {}
        '410':
          description: API version no longer supported (sunset)
          content: {}
components:
  schemas:
    UsersMeGetResponsesContentApplicationJsonSchemaFanCounts:
      type: object
      properties:
        followersCount:
          type: number
          format: double
        subscribersCount:
          type: number
          format: double
      required:
        - followersCount
        - subscribersCount
    UsersMeGetResponsesContentApplicationJsonSchemaContentCounts:
      type: object
      properties:
        imageCount:
          type: number
          format: double
        videoCount:
          type: number
          format: double
        audioCount:
          type: number
          format: double
        postCount:
          type: number
          format: double
        payToViewPostCount:
          type: number
          format: double
      required:
        - imageCount
        - videoCount
        - audioCount
        - postCount
        - payToViewPostCount
    getCurrentUser_Response_200:
      type: object
      properties:
        uuid:
          type: string
          format: uuid
        email:
          type: string
          format: email
        handle:
          type: string
        bio:
          type: string
        displayName:
          type: string
        isCreator:
          type: boolean
        createdAt:
          type: string
          format: date
        updatedAt:
          type: string
          format: date
        avatarUrl:
          type: string
          format: uri
        bannerUrl:
          type: string
          format: uri
        likesCount:
          type: number
          format: double
        fanCounts:
          $ref: >-
            #/components/schemas/UsersMeGetResponsesContentApplicationJsonSchemaFanCounts
        contentCounts:
          $ref: >-
            #/components/schemas/UsersMeGetResponsesContentApplicationJsonSchemaContentCounts
      required:
        - uuid
        - email
        - handle
        - bio
        - displayName
        - isCreator
        - createdAt
        - updatedAt

```

## SDK Code Examples

```python
import requests

url = "https://api.fanvue.com/users/me"

headers = {
    "X-Fanvue-API-Version": "2025-06-26",
    "Authorization": "Bearer <token>"
}

response = requests.get(url, headers=headers)

print(response.json())
```

```javascript
const url = 'https://api.fanvue.com/users/me';
const options = {
  method: 'GET',
  headers: {'X-Fanvue-API-Version': '2025-06-26', Authorization: 'Bearer <token>'}
};

try {
  const response = await fetch(url, options);
  const data = await response.json();
  console.log(data);
} catch (error) {
  console.error(error);
}
```

```go
package main

import (
	"fmt"
	"net/http"
	"io"
)

func main() {

	url := "https://api.fanvue.com/users/me"

	req, _ := http.NewRequest("GET", url, nil)

	req.Header.Add("X-Fanvue-API-Version", "2025-06-26")
	req.Header.Add("Authorization", "Bearer <token>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```ruby
require 'uri'
require 'net/http'

url = URI("https://api.fanvue.com/users/me")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Get.new(url)
request["X-Fanvue-API-Version"] = '2025-06-26'
request["Authorization"] = 'Bearer <token>'

response = http.request(request)
puts response.read_body
```

```java
HttpResponse<String> response = Unirest.get("https://api.fanvue.com/users/me")
  .header("X-Fanvue-API-Version", "2025-06-26")
  .header("Authorization", "Bearer <token>")
  .asString();
```

```php
<?php

$client = new \GuzzleHttp\Client();

$response = $client->request('GET', 'https://api.fanvue.com/users/me', [
  'headers' => [
    'Authorization' => 'Bearer <token>',
    'X-Fanvue-API-Version' => '2025-06-26',
  ],
]);

echo $response->getBody();
```

```csharp
var client = new RestClient("https://api.fanvue.com/users/me");
var request = new RestRequest(Method.GET);
request.AddHeader("X-Fanvue-API-Version", "2025-06-26");
request.AddHeader("Authorization", "Bearer <token>");
IRestResponse response = client.Execute(request);
```

```swift
import Foundation

let headers = [
  "X-Fanvue-API-Version": "2025-06-26",
  "Authorization": "Bearer <token>"
]

let request = NSMutableURLRequest(url: NSURL(string: "https://api.fanvue.com/users/me")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "GET"
request.allHTTPHeaderFields = headers

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error as Any)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```
