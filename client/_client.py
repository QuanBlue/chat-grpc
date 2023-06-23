import grpc
import threading
import os, sys

root_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
grpc_gen_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../services/grpc_generated/')))
utils_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils/')))
sys.path.append(root_dir)
sys.path.append(grpc_gen_dir)
sys.path.append(utils_dir)

from helper import *

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
            
            ClearScreen()
            
            heading_frame_top =  "                       ┏━━━━━━━━━━━━━━━━━━━━━┓"    
            heading_frame     =  "╔══════════════════════╣   CHAT BOX - gRPC   ╠════════════════════╗"
            heading_frame_bot =  "║                      ┗━━━━━━━━━━━━━━━━━━━━━┛                    ║"    
            welcome_msg = f"WELCOME {self.user_name}! - Your ID is {self.user.id}"
            
            frame_len = len(heading_frame)
            padding, remainder = PaddingSpace(frame_len, len(welcome_msg))
            
            print(f" {heading_frame_top}")
            print(f" {heading_frame}")
            print(f" {heading_frame_bot}")
            print(f" ║"," "*(padding - 1),f"{welcome_msg}"," "*(padding + remainder - 1),"║", sep="")
            print(f" ┣","━"*(frame_len - 2),"┫", sep="")
            print(f" ║"," "*(frame_len - 2),"║",sep="")

            # receive all msg from server
            messages = self.chat_stub.ReceiveMessage(chat_pb2.Empty())

            # print all msg
            for message in messages:
                # if not self.IsLikeMessage(message.msg):
                left_padding = 2
                msg = f"[{message.time}][{message.sender.id}] {message.sender.name}: {message.content}"
                print(f" ║"," "*left_padding,f"{msg}"," "*(frame_len -  left_padding - len(msg) - 2),"║",sep="")
            
            print(f" ║"," "*(frame_len - 2),"║", sep="")
            print(f" ╚","═"*(frame_len - 2),"╝", sep="")
            
            print("\n > Enter your Message:")
            
    def InputAndSendMsg(self):
        ClearScreen()
        
        print("(abs(28 - len(self.user_name))):", (abs(28 - len(self.user_name))))
        print(f"  ______________________________________")
        print(f" /                                      \\")
        print(f" |         Welcome to Chat App!      "," "*1,"|")
        print(f" |                                   "," "*1,"|")
        print(f" |      Name: {self.user_name}       "," "*(abs(17 - len(self.user_name))),"|")
        print(f" |      Your ID: {self.user.id}      "," "*13,"|")
        print(f" |                                   "," "*1,"|")
        print(f" |        Let's start chatting!      "," "*1,"|")
        print(f" |                                   "," "*1,"|")
        print(f" \______________________________________/\n")

        while True:
            msg_content = input(" > Enter your Message: ").rstrip('\n')
            
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

#  ╔══════════════════════ ✿CHAT BOX - gRPC ✿══════════════════════╗
#  ║                Welcome, quan! - Your ID is 01                  ║
#  ║ ───────────────────────────────────────────────────────────────║                                                              ║
#  ║ [18:38:33] 01: djd                                             ║
#  ║ [18:38:34] 01: dj                                              ║
#  ║                                                                ║
#  ╚════════════════════════════════════════════════════════════════╝
#
#  Enter your message:


# --------------------------------------------
#  ╔═══════════════════════ CHAT BOX - gRPC ════════════════════════╗
#  ║                                                                ║
#  ║ [18:38:33] 01: djd                                             ║
#  ║ [18:38:34] 01: dj                                              ║
#  ║                                                                ║
#  ╚════════════════════════════════════════════════════════════════╝

#  Welcome, quan! - Your ID is 01
#  Enter your message:


# --------------------------------------------
#   ╔════════════════════════════════════════════════════════╗
#   ║                 ۞ CHAT APPLICATION ۞                  ║
#   ║            WELCOME quan! - your ID is 01               ║
#   ╟────────────────────────────────────────────────────────╢
#   ║                                                        ║
#   ║ [18:38:33] 01: Hello there!                            ║
#   ║ [18:38:34] 01: How are you?                            ║
#   ║                                                        ║
#   ╚════════════════════════════════════════════════════════╝

# --------------------------------------------
#   ─────────────✿ CHAT APPLICATION ✿─────────────
#           WELCOME quan! - your ID is 01
#   ──────────────────────────────────────────────
#    [18:38:33]    01   : Hello there!
#    [18:38:34]    01   : How are you?
#   ──────────────────────────────────────────────