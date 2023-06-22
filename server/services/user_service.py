from google.protobuf import timestamp_pb2
from datetime import datetime

import service.grpc_generated.user_pb2 as user_pb2
import service.grpc_generated.user_pb2_grpc as user_pb2_grpc

from utils.helper import *

class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
	def __init__(self):
		self.users = []

	# def GetCurrentTime(self):
	# 	"""Get the current time
  
	# 	Returns:	
	# 		google.protobuf.Timestamp: The current time.
	# 	"""
	# 	# Get the current time
	# 	current_time = datetime.utcnow()
		
	# 	# Create a Timestamp object and set the current time
	# 	timestamp = timestamp_pb2.Timestamp()
	# 	timestamp.FromDatetime(current_time)

	# 	return timestamp

	def GenerateUserId(self):
		"""Generate a new user ID
  
		Returns: 
			string: The new user ID.
		"""
		new_id = str(self.max_user_id + 1)

		# Add a leading zero to the user ID if it is less than 10
		if len(new_id) < 2:
			new_id = '0' + new_id

		self.max_user_id += 1

		return new_id

	
	def CreateUser(self, request, context):				
		"""Create a new user and add it to the list of allowed users

		Args:
			request (User): The CreateUserRequest message
			context: The grpc request context

		Returns:	
			string: The CreateUserResponse message
		"""
		try:
			user = request.user
			
			# Create a new user
			new_user = user_pb2.User()
			new_user.id = self.GenerateUserId()
			new_user.create_time = GetCurrentTime()
			new_user.CopyFrom(user)

			# Add the new_user to the list
			self.users.append(new_user)

			# Prepare the response
			response = user_pb2.CreateUserResponse()
			response.message = f"User '{new_user.name}' with ID '{new_user.id}' created Successfully!"

			return response
		except:
			# Prepare the response
			response = user_pb2.CreateUserResponse()
			response.message = f"User '{new_user.name}' with ID '{new_user.id}' created Fail!"

			return response

