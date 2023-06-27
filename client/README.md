<h1 align="center">
  <b>Client Document</b>
</h1>
<br>

## Introduction

**The gRPC service** combines two main functionalities: Chat and User. This service provides communication capabilities through the Chat service and user management functionalities through the User service. It leverages the power of gRPC, a high-performance and language-agnostic remote procedure call (RPC) framework, to facilitate efficient communication between clients and the server.

## Implement the client-side code

To implement client-side code for a gRPC client, you can follow these steps:

-  Import the necessary gRPC libraries and modules
-  Create a **channel** to connect to the gRPC server
-  Create a **stub** for the gRPC service
-  Call the **gRPC service methods** using the **stub**
-  Process the **response** returned by the gRPC server

```py
# client.py

import grpc
from your_generated_proto_file import my_service_pb2, my_service_pb2_grpc

class ChatClient:
   def __init__(self):
      # Create a gRPC channel to connect to the server
      self.channel = grpc.insecure_channel('localhost:50051')

      # Create a stub for the gRPC service
      self.stub = my_service_pb2_grpc.MyServiceStub(self.channel)


   def InputAndSendMessage():
      # Prompt the user to enter a message
      msg = input("Enter msg")

      # Make a request to the server
      request = my_service_pb2.Message(sender='QuanBlue', content=msg)
      response = self.stub.SendMessage(request)

      # Process the response from the server
      print('Response received:', response.content)

   def run(self):
      # Start the client in an infinite loop
      while True:
         self.InputAndSendMessage()

if __name__ == '__main__':
   # Create an instance of the ChatClient and run the client
   client = Client()
   client.run()
```

> **Note:** Remember to handle any potential exceptions that may occur during the gRPC communication, such as `grpc.RpcError` or `grpc.StatusCode exceptions`.
