# https://github.com/sendgrid/sendgrid-python#installation

import sendgrid
import os
from pprint import pprint

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": "jamesfolk1@gmail.com"
        }
      ],
      "subject": "Sending with SendGrid is Fun"
    }
  ],
  "from": {
    "email": "test@example.com"
  },
  "content": [
    {
      "type": "text/plain",
      "value": "and easy to do anywhere, even with Python"
    }
  ]
}
response = sg.client.mail.send.post(request_body=data)
print(str(response))
# print(response.body)
# print(response.headers)
# print(response)
