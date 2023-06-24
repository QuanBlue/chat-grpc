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


PADDING = 2
CHAT_HISTORY = 9999
FRAME_LENGTH = 79

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

    def FormatMessages(self, messages):
        """Add padding to the message name to make it the same length

        Args:
            messages ([string]): list of messages

        Returns:
            [string]: list of formatted messages
        """
        formatted_messages = []

        senders_name = [message.sender.name for message in messages]
        max_len = GetMaxLength(senders_name)
        
        for message in messages:
            message.sender.name = message.sender.name.ljust(max_len)
            formatted_messages.append(message)

        return formatted_messages
        
    def ShowMessage(self):
        """Draw Chat box frame + Show the message in the chat box
                                ┏━━━━━━━━━━━━━━━━━━━┓"    
            ╔═══════════════════╣  CHAT BOX - gRPC  ╠═══════════════════╗
            ║                   ┗━━━━━━━━━━━━━━━━━━━┛                   ║
            ║               WELCOME hi! - Your ID is 14                 ║
            ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
            ║                                                           ║
            ║  [19:54:51][01] Ngoc Lien : hi                            ║
            ║  [20:05:00][02] Thanh Quan: hello there                   ║
            ║  [20:05:02][02] Thanh Quan: what's up                     ║
            ║  [20:05:07][03] Thanh Dat : alo                           ║
            ║                                                           ║
            ╚═══════════════════════════════════════════════════════════╝
    
        """
        messages = self.chat_stub.ReceiveMessage(chat_pb2.Empty())
        len_msg = len(list(messages))
        
        if int(self.number_msg) != int(len_msg):
            self.number_msg = len_msg
            
            ClearScreen()
            
            title_padding, remainder = PaddingSpace(FRAME_LENGTH, 21)
            print(f"  "," "*title_padding,"┏━━━━━━━━━━━━━━━━━━━┓", sep="")
            print(f" ╔","═"*title_padding,"╣  CHAT BOX - gRPC  ╠","═"*(title_padding + remainder - 2),"╗", sep="")
            print(f" ║"," "*title_padding,"┗━━━━━━━━━━━━━━━━━━━┛"," "*(title_padding + remainder - 2),"║", sep="")
            
            welcome_msg = f"WELCOME {self.user_name}! - Your ID is {self.user.id}"
            title_padding, remainder = PaddingSpace(FRAME_LENGTH, len(welcome_msg))
            print(f" ║"," "*(title_padding - 1),f"{welcome_msg}"," "*(title_padding + remainder - 1),"║", sep="")
            print(f" ┣","━"*(FRAME_LENGTH - 2),"┫", sep="")
            print(f" ║"," "*(FRAME_LENGTH - 2),"║",sep="")

            # receive CHAT_HISTORY msg from server and format it
            messages = self.chat_stub.ReceiveMessage(chat_pb2.Empty())
            messages = list(messages)[-CHAT_HISTORY:]
            # messages = list(messages)
            messages = self.FormatMessages(messages)

            # print all msg
            for message in messages:
                # if not self.IsLikeMessage(message.msg):
                msg_info = f"[{message.time}][{message.sender.id}] {message.sender.name}"
                msg = f"{msg_info}: {message.content}"
                    
                content_len = FRAME_LENGTH -  PADDING*2 - len(msg_info) - 4
                
                msg = SliceMessage(message.content, content_len)
                
                if len(msg) == 1:
                    left_padding = PADDING
                    right_padding = content_len - len(msg[0]) + PADDING
                    print(f" ║"," "*left_padding,f"{msg_info}: {msg[0]}"," "*right_padding,"║",sep="")
                else:
                    # print first line
                    print(f" ║"," "*PADDING,f"{msg_info}: {msg[0]}"," "*PADDING,"║",sep="")
                    
                    # print middle lines
                    for i in range(1, len(msg) - 1):
                        print(f" ║"," "*(PADDING + len(msg_info) + 2),f"{msg[i]}"," "*PADDING,"║",sep="")
                    
                    # print last line
                    left_padding = PADDING + len(msg_info) + 2
                    right_padding = FRAME_LENGTH - left_padding - len(msg[-1]) - 2
                    print(f" ║"," "*left_padding,f"{msg[-1]}"," "*right_padding,"║",sep="")
                    
             #9   
                
            
            print(f" ║"," "*(FRAME_LENGTH - 2),"║", sep="")
            print(f" ╚","═"*(FRAME_LENGTH - 2),"╝", sep="")
            
            print("\n > Enter your Message:")
            
    def InputAndSendMsg(self):
        ClearScreen()
        
        print(f"  ____________________________________")
        print(f" /                                    \\")
        print(f" |       Welcome to Chat App!    "," "*3,"|")
        print(f" |                               "," "*3,"|")
        print(f" |    Name: {self.user_name}      "," "*(abs(18 - len(self.user_name))),"|")
        print(f" |    Your ID: {self.user.id}    "," "*15,"|")
        print(f" |                               "," "*3,"|")
        print(f" |      Let's start chatting!    "," "*3,"|")
        print(f" |                               "," "*3,"|")
        print(f" \____________________________________/\n")

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