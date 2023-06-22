# Service

**1**. **Define your gRPC service** using protocol buffers. This will define the messages and methods used for communication.

1. Define your service in a .proto file using protocol buffer syntax. (`chat.proto` in `/service`)

   ```go
   syntax = "proto3";

   service ChatService {
     rpc SendMessage(Message) returns (Message) {}
     rpc ReceiveMessage(Empty) returns (stream Message) {}
   }

   message Message {
     string user_name = 1;
     string text = 2;
   }

   message Empty {}
   ```

   <details>
     <summary>Explain variable</summary>

   This defines a:

   -  **Message** type with `text` and `sender` fields
   -  **ChatService** with two methods:
      -  `SendMessage` takes a `Message` object as input and returns a `Message` object
      -  `ReceiveMessage` takes an empty `Empty` object as input and returns a stream of `Message` objects.

   </details>

2. Use the generated code to implement gRPC service.

   ```shell
   python -m grpc_tools.protoc -I [path/to/protos/dir] --python_out=[path/to/output/python] --grpc_python_out=[path/to/output/grpc/python] [/path/to/protos/file.proto]
   ```

   Example:

   ```shell
    python3 -m grpc_tools.protoc -I service --python_out=./service --grpc_python_out=./service ./service/user.proto

   python3 -m grpc_tools.protoc -I service/proto --python_out=./service --grpc_python_out=./service ./service/proto/chat.proto
   ```

---

the generated user_pb2.py file typically contains the message definitions and methods for interacting with the message data, while the user_pb2_grpc.py file contains the generated gRPC service stubs and methods for interacting with the gRPC service.

Here's a breakdown of the roles of each file:

-  user_pb2.py:

   -  Defines the message types using Protocol Buffers syntax. These message types represent the data structures that will be exchanged between the client and the server.
   -  Provides methods for working with the message data, such as setting and getting field values, serialization, and deserialization.
   -  You can use the message types defined in this file to create, manipulate, and transfer data between the client and the server.

-  user_pb2_grpc.py:
   -  Contains the generated gRPC service stubs and methods that the client and server use to communicate.
   -  Provides classes and methods that allow the client to make gRPC requests to the server and receive responses.
   -  Implements the server-side logic for handling the gRPC requests from the client.
   -  You can use the service stubs and methods defined in this file to interact with the gRPC service, make remote procedure calls (RPCs), and handle the communication between the client and server.

The separation of concerns between these two files allows for a clear distinction between the message definitions and the service definitions in your gRPC application. It helps maintain a clean and organized codebase and makes it easier to work with both the message data and the gRPC service functionality separately.

It's important to note that these files are generated by the Protocol Buffers compiler (protoc) based on the .proto file that you provide, and their exact names and contents may vary depending on your specific proto file and the options used during compilation.

---

-  \*\_pb2.py:

   -  This file contains the generated Python code for the message types defined in your .proto file.
   -  It includes the classes representing your message types, as well as methods for working with the message data, such as serialization, deserialization, setting and getting field values, and more.
   -  This file allows you to create, manipulate, and transfer data using the message types defined in your .proto file.

-  \*\_pb2_grpc.py:
   -  This file contains the generated gRPC service stubs and methods for interacting with the gRPC service defined in your .proto file.
   -  It includes classes and methods that allow the client to make gRPC requests to the server, receive responses, and handle the communication between the client and server.
   -  This file also implements the server-side logic for handling the gRPC requests from the client.
   -  It provides the necessary functionality to make remote procedure calls (RPCs) and work with the gRPC service defined in your .proto file.