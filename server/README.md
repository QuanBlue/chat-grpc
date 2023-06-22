# Server

## :mechanical_arm: How to use gRPC

3. **Implement the server-side code** for your gRPC service. This will handle incoming requests and provide responses. You can create a new process for each instance of your gRPC server.
     <details>
       <summary>Explain server</summary>

   -  This defines a `ChatServiceServicer` class that implements the `ChatService` defined in `chat.proto`. The `SendMessage` function appends the received message to a list of messages and returns the same message. The `ReceiveMessage` function yields all the messages in the list.
   -  The `serve` function creates a gRPC server and adds the `ChatServiceServicer` to it. It starts the server on port `50051`.

      </details>

4. **Implement the client-side code** for your gRPC service. This will send requests to the server and receive responses. You can create one or more client processes as needed.

5. **Start** the `server process` and `client process(es)`.

6. Use gRPC's built-in functionality to handle the communication between the server and client processes.
