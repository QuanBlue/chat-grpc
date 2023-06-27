<h1 align="center">
  <b>Server Document</b>
</h1>

<br/>

# Introduction

**The gRPC service** combines two main functionalities: Chat and User. This service provides communication capabilities through the Chat service and user management functionalities through the User service. It leverages the power of gRPC, a high-performance and language-agnostic remote procedure call (RPC) framework, to facilitate efficient communication between clients and the server.

# Implement the server-side code

**1. Write gRPC service** by subclassing the generated service interface. Override the methods defined in the interface and provide the desired functionality for each method.

1. Define your service servicer. Place at `chat-grpc/server/services_class/`

   ```py
   # my_service.py

   from your_generated_proto_file import my_service_pb2, my_service_pb2_grpc

   # Create a class that inherits from the generated gRPC server class
   class MyServiceServicer(my_service_pb2_grpc.MyServiceServicer):
      def __init__(self):
         # Initialize any required resources or dependencies
         pass

      def SendMessage(self, request, context):
         # Implement the logic for handling the SendMessage RPC
         # This method is called when a client sends a message

         # Retrieve the message content from the request
         message = request

         # Process the message, e.g., store it in a database, send it to other clients, etc.
         # ...

         # Create a response message
         response = my_service_pb2.Message()
         response.content = "Message sent successfully"

         return response

      def ReceiveMessage(self, request, context):
         # Implement the logic for handling the ReceiveMessage RPC
         # This method is called when a client requests to receive messages
         ...
         pass
   ```

**2. Configure server**

1. Create a gRPC server object and configure its settings such as port number, maximum concurrent requests, and SSL/TLS options.
2. Register the service: Add your service implementation to the gRPC server by calling the appropriate registration method (`add_XXXServicer_to_server`) and passing an instance of your service implementation.
3. Start the server: Start the gRPC server to listen for incoming client requests and handle them using your service implementation.

   ```py
   # server.py

   import grpc
   from concurrent import futures
   from your_generated_proto_file import my_service_pb2, my_service_pb2_grpc
   import MyServiceServicer


   # create a gRPC server
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

   # add servicers to the server
   my_service_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)

   # start the gRPC server
   server.add_insecure_port('[::]:50051') # Specify the server port
   server.start()

   # Keep the server running
   server.wait_for_termination()
   ```

</br>

This will handle incoming requests and provide responses. You can create a new process for each instance of your gRPC server.

-  This defines a `MyServiceServicer` class that implements the `MyService` defined in `my_service.proto`.
-  The `serve` function creates a gRPC server and adds the `MyServiceServicer` to it. It starts the server on port `50051`.
