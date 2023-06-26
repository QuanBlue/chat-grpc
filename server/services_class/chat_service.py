import grpc 

import services.grpc_generated.share_type_pb2 as share_type_pb2

import services.grpc_generated.chat_pb2 as chat_pb2
import services.grpc_generated.chat_pb2_grpc as chat_pb2_grpc

import services.grpc_generated.user_pb2 as user_pb2
import services.grpc_generated.user_pb2_grpc as user_pb2_grpc

from utils.helper import *
from utils.logger import *


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
	def __init__(self):
		self.logger = Logger()
		self.messages = []
  
		self.channel = grpc.insecure_channel('localhost:50051')
		
		# Create a stub for the user service
		self.user_stub = user_pb2_grpc.UserServiceStub(self.channel)

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
			sender = request.sender
			print('---------')
			print("sender.from_user", sender.like.from_user)
			print("sender.is_allow: ", sender.like.is_allow)
			print('---------')

   
			if sender.like.is_allow == False:
				self.logger.error(f'User [{sender.id}]{sender.name} is not allowed to send messages!')
				raise grpc.RpcError('You are not allowed to send messages!')
   
			# Create a new message
			sending_msg = chat_pb2.Message()
			sending_msg.CopyFrom(request)
			sending_msg.time = GetCurrentTime()
   
			# Add the message to the list of messages
			self.messages.append(sending_msg)

			self.logger.info(f'Message sent from user [{sending_msg.sender.id}]{sending_msg.sender.name}: {sending_msg.content}')

			return chat_pb2.SendMessageResponse(success=True)
		except grpc.RpcError as error:
			self.logger.error(f'Error sending message! {error}')
			return chat_pb2.SendMessageResponse(success=False)

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


	def FindUser(self, id):
		users = self.user_stub.GetUsers(share_type_pb2.Empty())
		
		for user in users:
			if user.id == id:
				return user
		
		raise grpc.RpcError(f"User with ID '{id}' not found!")
	

	def HandleLikeMsg(self, request, context):
		print("Handle like")
		
		sender  = request.sender
		receiver = self.FindUser(request.receiver_id)
		
		# check if receiver_id is valid
		if len(receiver.id) != 2 or not receiver.id.isdigit():
			raise grpc.RpcError("Invalid receiver.id, must be \"2 digits\"") 
		elif sender.id == receiver.id:
			raise grpc.RpcError("You can not LIKE yourself!")            
		elif sender.id in receiver.like.from_user:
			raise grpc.RpcError(f"You only LIKED: [{receiver.id}]'s message ONCE!")            
			
		
		receiver.like.from_user.append(sender.id)
					
		if len(receiver.like.from_user) >= 2:
			receiver.like.is_allow = True
			self.user_stub.UpdateUser(receiver)
						
		self.logger.info(f'User[{receiver.id}] is ALLOWED to send message"')
