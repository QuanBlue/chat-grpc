<h1 align="center">
  <b>Server Document</b>
</h1>

<p align="center">Server-side</p>

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

# Implement the server-side code

This will handle incoming requests and provide responses. You can create a new process for each instance of your gRPC server.

-  This defines a `MyServiceServicer` class that implements the `MyService` defined in `my_service.proto`. The `SendMessage` function appends the received message to a list of messages and returns the same message. The `ReceiveMessage` function yields all the messages in the list.
-  The `serve` function creates a gRPC server and adds the `ChatServiceServicer` to it. It starts the server on port `50051`.
