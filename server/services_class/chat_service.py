import services.grpc_generated.chat_pb2 as chat_pb2
import services.grpc_generated.chat_pb2_grpc as chat_pb2_grpc
from ...utils.helper import *


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.messages = []

    def SendMessage(self, request, context):
        """Send a message to a user

        Args:
                                                                        request (Message): The SendMessageRequest message
                                                                        context: The grpc request context

        Returns:
                                                                        Message: The SendMessageResponse message
        """
        # Create a new message
        sending_msg = chat_pb2.Message()
        sending_msg.CopyFrom(request)
        sending_msg.time = GetCurrentTime()

        # Add the message to the list of messages
        self.messages.append(request)

        return sending_msg

    def ReceiveMessage(self, request, context):
        """Receive a message from a user

        Args:
                                                                        request (Empty): The ReceiveMessageRequest message
                                                                        context: The grpc request context

        Returns:
                                                                        Message (stream Message): The message from the user
        """
        for message in self.messages:
            yield message
