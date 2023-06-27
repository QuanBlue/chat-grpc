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
   
			if sender.like.is_allow == False:
				self.logger.error(f'User[{sender.id}] is BLOCKED to send message')
				return chat_pb2.SendMessageResponse(success=False)
   
			# Create a new message
			sending_msg = chat_pb2.Message()
			sending_msg.CopyFrom(request)
			sending_msg.time = GetCurrentTime()
   
			# Add the message to the list of messages
			self.messages.append(sending_msg)

			self.logger.info(f'User[{sending_msg.sender.id}] send message: {sending_msg.content}')

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
   

	def HandleLikeMsg(self, request, context):
		sender  = request.sender
		response = ""

		try:
			receiver = self.user_stub.GetUser(user_pb2.GetUserRequest(id=request.receiver_id))
		except grpc.RpcError as error:
			error = error.details().strip("Exception calling application: ")
			self.logger.error(f'Getting user! {error}')
			return chat_pb2.LikeResponse(response=f"{error}")   


		# check if receiver_id is valid
		if len(receiver.id) != 2 or not receiver.id.isdigit():
			response = f"Invalid receiver.id, must be \"2 digits\""
		elif sender.id == receiver.id:
			response = f"User[{sender.id}] can not LIKE yourself!"
		elif sender.id in [user.id for user in receiver.like.from_user]:
			response = f"User[{sender.id}] only LIKED: [{receiver.id}]'s message ONCE!"
		else:
			receiver.like.from_user.append(sender)
			self.user_stub.UpdateUser(receiver)
			
			response = f'User[{sender.id}] like for user[{receiver.id}]'

			if len(receiver.like.from_user) >= 2:
				receiver.like.is_allow = True
				self.user_stub.UpdateUser(receiver)
							
				response = f'User[{receiver.id}] is ALLOWED to send message'
			
			self.logger.info(f"{response}")
			return chat_pb2.LikeResponse(response=f"{response}")

		self.logger.error(f"{response}")
		return chat_pb2.LikeResponse(response=f"{response}")