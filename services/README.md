<h1 align="center">
  <b>gRPC Service Document</b>
</h1>

<p align="center">[Provide a brief introduction to the gRPC service. Explain its purpose, functionality, and any relevant background information.]</p>

<p align="center">
  <b>
      <a href="https://github.com/QuanBlue/chat-grpc">Documentation</a> •
      <a href="https://github.com/QuanBlue/chat-grpc/issues/">Report Bug</a> •
      <a href="https://github.com/QuanBlue/chat-grpc/issues/">Request Feature</a>
  </b>
</p>

<br/>

# Introduction

**The gRPC service** combines two main functionalities: Chat and User. This service provides communication capabilities through the Chat service and user management functionalities through the User service. It leverages the power of gRPC, a high-performance and language-agnostic remote procedure call (RPC) framework, to facilitate efficient communication between clients and the server.

# GRPC Overview

**gRPC** is an open-source, high-performance remote procedure call (RPC) framework developed by Google. It enables efficient and scalable communication between distributed systems and is designed to be language-agnostic, allowing developers to build robust and interoperable applications across different programming languages.

## General gRPC code

**1**. **Define your gRPC service** using protocol buffers. This will define the messages and methods used for communication.

1. Define your service in a `.proto` file using protocol buffer syntax.
   Place at `chat-grpc/services/proto/`

   ```go
   // my_service.proto

   syntax = "proto3";

   service MyService {
      rpc SendMessage(Message) returns (Message) {}
      rpc ReceiveMessage(Empty) returns (stream Message) {}
   }

   message Message {
      string sender = 1
      string content = 2
   }

   message Empty {}
   ```

      <details>
        <summary>Explain variable</summary>

   This defines a:

   -  **Message** type with `sender` and `content` fields
   -  **MyService** with two methods:

      -  `SendMessage` takes a `Message` object as input and returns a `Message` object
      -  `ReceiveMessage` takes an empty `Empty` object as input and returns a stream of `Message` objects.

      </details>

2. Generate gRPC code:

-  Open a terminal or command prompt.

-  Navigate to the root directory of project.

-  Run the following command to generate the gRPC code:

   ```shell
   python -m grpc_tools.protoc -I [path/to/protos/dir] --python_out=[path/to/output/python] --grpc_python_out=[path/to/output/grpc/python] [/path/to/protos/file.proto]
   ```

   Example:

   ```shell
   python3 -m grpc_tools.protoc -I services/proto --python_out=./services/grpc_generated --grpc_python_out=./services/grpc_generated ./services/proto/my_service.proto
   ```

      <details>
         <summary>Explain command</summary>

   -  Use the current directory (`services/proto`) as the import search path (`-I` option).
   -  Generate Python code from the `.proto` file using the `--python_out` option.
      Generate gRPC Python code using the `--grpc_python_out` option.
   -  Replace `my_service.proto` with the actual name of your Protobuf file.
   </details>

-  After running the command, you should see two new Python files generated in `services/grpc_generated` directory, allows for a clear distinction between the message definitions and the service definitions in your gRPC application. It helps maintain a clean and organized codebase and makes it easier to work with both the message data and the gRPC service functionality separately. The separation of concerns between these two files:

   -  `my_service_pb2.py` (Syntax: `[proto]_pb2.py`):

      -  This file contains the generated Python code for the message types defined in your `.proto` file (message types).
      -  Provides methods for working with the message data, such as setting and getting field values, serialization, and deserialization.
      -  You can use the message types defined in this file to create, manipulate, and transfer data between the client and the server.

   -  `my_service_pb2_grpc.py` (Syntax: `[proto]_pb2_grpc.py`):
      -  Contains the generated gRPC service stubs and methods that the client and server use to communicate.
      -  Provides classes and methods that allow the client to make gRPC requests to the server and receive responses.
      -  Implements the server-side logic for handling the gRPC requests from the client.
      -  You can use the service stubs and methods defined in this file to interact with the gRPC service, make remote procedure calls (RPCs), and handle the communication between the client and server.

# Service Overview

The `Chat` + `User service` enables clients to engage in real-time chat conversations and perform user-related operations. The Chat service allows clients to send and receive messages, while the User service enables user creation, retrieval, and management.

**The Chat service:** clients can establish a bidirectional stream to send and receive chat messages, facilitating interactive and real-time communication. This service is ideal for building chat applications, collaboration tools, or any system requiring instant messaging capabilities.

**The User service:** provides endpoints to create new users, retrieve user information, and perform user management operations. It allows clients to manage user profiles, authentication, and access control within their applications.

**The share_type service:** provides the message type which is used in `the chat service` and `the user service`.

# Prerequisites

-  **Python:** >= 3.10.7
-  **gRPC tools:** gRPC compiler, Install [here](https://grpc.io/docs/languages/python/quickstart/).
