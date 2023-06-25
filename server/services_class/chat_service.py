import services.grpc_generated.chat_pb2 as chat_pb2
import services.grpc_generated.chat_pb2_grpc as chat_pb2_grpc

from utils.helper import *
from utils.logger import *




class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
	def __init__(self):
		self.logger = Logger()
		self.messages = []

	# complete!
	def SendMessage(self, request, context):
		"""Send a message to a user

		Args:
			request (Message): The SendMessageRequest message
			context: The grpc request context

		Returns:
			Message: The SendMessageResponse message
		"""
		try:
			# Create a new message
			sending_msg = chat_pb2.Message()
			sending_msg.CopyFrom(request)
			sending_msg.time = GetCurrentTime()
     
			# Add the message to the list of messages
			self.messages.append(sending_msg)
	
			self.logger.info(f'Message sent from user [{sending_msg.sender.id}]{sending_msg.sender.name}: {sending_msg.content}')

			return sending_msg
		except:
			self.logger.error(f'Error sending message! - from {sending_msg.sender}')
			return chat_pb2.Message()

	# complete!
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
