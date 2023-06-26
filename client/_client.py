import grpc
import threading
import os, sys

root_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
grpc_gen_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../services/grpc_generated/')))
utils_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils/')))
sys.path.append(root_dir)
sys.path.append(grpc_gen_dir)
sys.path.append(utils_dir)

# from helper import *
from utils.helper import *
from utils.logger import *

import services.grpc_generated.share_type_pb2 as share_type_pb2

import services.grpc_generated.chat_pb2 as chat_pb2
import services.grpc_generated.chat_pb2_grpc as chat_pb2_grpc

import services.grpc_generated.user_pb2 as user_pb2
import services.grpc_generated.user_pb2_grpc as user_pb2_grpc


PADDING = 2
CHAT_HISTORY = 9999
FRAME_LENGTH = 80
USER_LENGTH = 10
COMMAND = {
    ':like'     : ":like <user_id> - like for user's message",
    ':name_len' : ":name_len <limit_length> - limit the length of the user name. Default is 10",
    ":frame_len": ":frame_len <limit_length> - limit the length of the frame. Default is 80",
    ":padding"  : ":padding <limit_length> - padding of the content in frame. Default is 2",
    ":history"  : ":history <limit_length> - limit the number of messages in the chat history. Default is 9999",
    ":help"     : ":help - show all commands with description",
}

class ChatClient:
    def __init__(self):
        self.logger = Logger()
        
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
        self.is_show_welcome = False

    def FormatName(self, name):
        """Format the name to be capitalized (Title Case)
        and abbreviate name fit the USER_LENGTH

        Args:
            name (string): The name to be formatted

        Returns:
            string: The formatted name
        """
        words = name.strip().split()
        formatted_words = []

        for word in words:
            formatted_word = word.capitalize()  
            formatted_words.append(formatted_word)

        formatted_name = " ".join(formatted_words)

        return self.AbbreviateName(formatted_name, USER_LENGTH)
    
    def AbbreviateName(self, name, max_length):
        """Abbreviate the name to fit the max_length
        First time : Nguyen Thanh Quan -> Nguyen T. Quan
        Second time: Nguyen Thanh Quan -> N. T. Quan
        Third time : Nguyen Thanh Quan -> NTQ

        Args:
            name (string): The name to be abbreviated
            max_length (int): The max length of the name

        Returns:
            string: The abbreviated name
        """
        words = name.split() 
        abbreviation = []

        # Abbreviate first time 
        # Ex: Nguyen Thanh Quan -> Nguyen T. Quan
        for i, word in enumerate(words):
            if i == 0 or i == len(words) - 1:
                abbreviation.append(word)
            else:
                abbreviation.append(word[0].upper()+".")

        # calculate the length of abbreviation
        abbreviation_length = sum(len(s) for s in abbreviation)
        
        if abbreviation_length <= max_length:
            abbreviation_name = " ".join(abbreviation)
            return abbreviation_name
        else:
            # Abbreviate second time   
            # Ex: Nguyen Thanh Quan -> N. T. Quan
            abbreviation[0] = abbreviation[0][0]+"."    
            
            # calculate the length of abbreviation
            abbreviation_length = sum(len(s) for s in abbreviation)
            
            if abbreviation_length <= max_length:
                abbreviation_name = " ".join(abbreviation)
                return abbreviation_name
            else:
                # Abbreviate third time   
                # Ex: Nguyen Thanh Quan -> NTQ
                abbreviation_name = [abbreviation[i][0] for i in range(len(abbreviation))]    
                abbreviation_name = "".join(abbreviation_name)
                return abbreviation_name
        

    def FormatMessages(self, messages):
        """Add padding to the message name to make it the same length

        Args:
            messages ([string]): list of messages

        Returns:
            [string]: list of formatted messages
        """
        formatted_messages = []
        senders_name = [self.FormatName(message.sender.name) for message in messages]
        
        max_len = GetMaxLength(senders_name)
        
        for i,message in enumerate(messages):
            message.sender.name = senders_name[i].ljust(max_len)
            formatted_messages.append(message)


        return formatted_messages


    def DrawAppUI(self):
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
        messages = self.chat_stub.ReceiveMessage(share_type_pb2.Empty())
        messages = list(messages)[-CHAT_HISTORY:]
        # messages = list(messages)
        messages = self.FormatMessages(messages)

        # print msg
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
                
        print(f" ║"," "*(FRAME_LENGTH - 2),"║", sep="")
        print(f" ╚","═"*(FRAME_LENGTH - 2),"╝", sep="")
        
        print("\n > Enter your Message:")


    def ShowMessage(self):
        messages = self.chat_stub.ReceiveMessage(share_type_pb2.Empty())
        len_msg = len(list(messages))
        
        if self.is_show_welcome == False:
            return 
        else:
            if int(self.number_msg) != int(len_msg):
                self.number_msg = len_msg
                
                # Draw UI                
                self.DrawAppUI()
            
    def BlockSendMessage(self):
        like  = user_pb2.Like()
        like.from_user.extend([])
        like.is_allow = False
        
        self.user.like.CopyFrom(like)
        
        self.user_stub.UpdateUser(self.user)
        
    def InputAndSendMsg(self):
        ClearScreen()
        
        if self.is_show_welcome == False:
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
        else:
            self.DrawAppUI()

        while True:
            msg_content = input(" > Enter your Message: ").rstrip('\n')
            self.is_show_welcome = True

            # run command if msg_content is command            
            command, args = GetCommand(msg_content, COMMAND)
            if command:
                self.ExecuteCommand(command, args)
                return

            try:
                # send msg to server
                # print("------ user ---")
                # # print("from_user:", self.user.like.from_user)
                # print("allow:", self.user.like.is_allow)
                # print("----------")
                if self.user.like.is_allow == True:
                    message = chat_pb2.Message(sender=self.user, content=msg_content)
                    response = self.chat_stub.SendMessage(message)
                    self.BlockSendMessage()
                
                else:
                    self.logger.error(f"User is block send message")
                
                # print("------ updated user ---")
                # # print("from_user:", self.user.like.from_user)
                # print("allow:", self.user.like.is_allow)
                # print("----------")
                
            except grpc.RpcError as error:
                self.logger.error(f"SendMessage error {error}")
                



    def ExecuteCommand(self,command, args):
        # like
        if command == ":like":
            try:
                like_req = chat_pb2.LikeRequest(sender=self.user, receiver_id=args[0])
                response = self.chat_stub.HandleLikeMsg(like_req)
                print(response.response)
            except grpc.RpcError as error:
                self.logger.error(f":like error - {error.details()}")
        
        # name_len
        elif command == ":name_len":
            try:
                global USER_LENGTH
                USER_LENGTH = int(args[0])
                self.DrawAppUI()
            except grpc.RpcError as error:
                self.logger.error(f":user_len err {error.details()}")
                
        # frame_len
        elif command == ":frame_len":
            try:
                global FRAME_LENGTH
                FRAME_LENGTH = int(args[0])
                self.DrawAppUI()
            except grpc.RpcError as error:
                self.logger.error(f":frame_len er {error.details()}")
                
        # padding
        elif command == ":padding":
            try:
                if int(args[0]) < 0 or int(args[0]) > 10:
                    raise Exception("invalid argument [padding must be >= 0 and <= 10]")
                
                global PADDING
                PADDING = int(args[0])
                self.DrawAppUI()
            except grpc.RpcError as error:
                self.logger.error(f":padding error - {error}")
        
        # history                 
        elif command == ":history":
            try:
                global CHAT_HISTORY
                CHAT_HISTORY = int(args[0])
                self.DrawAppUI()
            except grpc.RpcError as error:
                self.logger.error(f":history error - {error.details()}")
                
        # help
        elif command == ":help":
            try:
                print() 
                            
                list_cmd = [value.split(" - ")[0] for key, value in COMMAND.items()]
                max_len_list_cmd = GetMaxLength(list_cmd)
                            
                for key, value in COMMAND.items():
                    cmd = value.split(" - ")[0]
                    desc = value.split(" - ")[1]
                    print(f" {cmd.ljust(max_len_list_cmd)}","  ",f"{desc}", sep="")
                
                input("\n Press Any Key to Continue....\n")
                self.InputAndSendMsg()
                
            except grpc.RpcError as error:
                self.logger.error(f":help error - {error.details()}")
    
    def run(self):
        threading.Thread(target=self.InputAndSendMsg, args=()).start()
        while True:
            self.ShowMessage()


if __name__ == '__main__':
    client = ChatClient()
    client.run()
