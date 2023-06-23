import grpc
import threading
import os, sys

root_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
grpc_gen_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../services/grpc_generated/')))
sys.path.append(root_dir)
sys.path.append(grpc_gen_dir)

import services.grpc_generated.chat_pb2 as chat_pb2
import services.grpc_generated.chat_pb2_grpc as chat_pb2_grpc

import services.grpc_generated.user_pb2 as user_pb2
import services.grpc_generated.user_pb2_grpc as user_pb2_grpc


class ChatClient:
    def __init__(self):
        # Create a gRPC channel
        self.channel = grpc.insecure_channel('localhost:50051')

        # Create a stub for the service
        self.chat_stub = chat_pb2_grpc.ChatServiceStub(self.channel)
        self.user_stub = user_pb2_grpc.UserServiceStub(self.channel)

        # Do not specify the user ID, it will be assigned by the server
        self.user_name = input("Enter your name: ")
        self.user = user_pb2.User(name=self.user_name)
        self.user = self.user_stub.CreateUser(self.user)
        
        self.number_msg = 0

    def ShowMessage(self):
        messages = self.chat_stub.ReceiveMessage(chat_pb2.Empty())
        len_msg = len(list(messages))
        # print("LOG: number_msg:", self.number_msg,"- len_msg:", len_msg)
        
        if int(self.number_msg) != int(len_msg):
            self.number_msg = len_msg

            print(f"WELCOME {self.user_name}! - your ID is {self.user.id}\n\n")
            print("-------------- CHAT BOX - gRPC --------------")

            # receive all msg from server
            messages = self.chat_stub.ReceiveMessage(chat_pb2.Empty())

            # print all msg
            for message in messages:
                # if not self.IsLikeMessage(message.msg):
                print(f"[{message.time}][{message.sender.id}] {message.sender.name}: {message.content}")

            print("----------------------------------------------")
            print("Enter your Message:")
            
    def InputAndSendMsg(self):
        print("self.user:", self.user)
        while True:
            msg_content = input("Enter your Message: ").rstrip('\n')
            print("log: msg_content:", msg_content)
            
            # send msg to server
            message = chat_pb2.Message(sender=self.user, content=msg_content)
            response = self.chat_stub.SendMessage(message)

    def run(self):
        threading.Thread(target=self.InputAndSendMsg, args=()).start()
        while True:
            self.ShowMessage()


if __name__ == '__main__':
    client = ChatClient()
    client.run()

