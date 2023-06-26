import os, sys
import grpc

# from google.protobuf import timestamp_pb2
# from google.protobuf import timestamp_pb2
from datetime import datetime

import services.grpc_generated.user_pb2 as user_pb2
import services.grpc_generated.user_pb2_grpc as user_pb2_grpc

from utils.helper import *
from utils.logger import *


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.logger = Logger()
        
        self.users = []
        self.max_user_id = 0

    # complete this function
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

    # complete this function
    def CreateUser(self, request, context): 
        """Create a new user and add it to the list of allowed users

        Args:
                request (User): The CreateUserRequest message
                context: The grpc request context

        Returns:	
                string: The CreateUserResponse message
        """
        try:
            user = request

            # Create a new user
            new_user = user_pb2.User()
            
            new_user.CopyFrom(user)
            new_user.id = self.GenerateUserId()
            new_user.created_time = GetCurrentTime()
            new_user.like.from_user.extend([])
            new_user.like.is_allow = True
                
            # Add the new_user to the list
            self.users.append(new_user)
            
            self.logger.info(f"User '{new_user.name}' with ID '{new_user.id}' created successfully!")            
            return new_user
        except:
            # Prepare the response
            new_user = user_pb2.CreateUserResponse()
            self.logger.error(f"User '{new_user.name}' with ID '{new_user.id}' created Fail!")            


    def UpdateUser(self, request, context):
        updated_user = request
        
        for user in self.users:
            if user.id == updated_user.id:
                user.CopyFrom(updated_user)
                self.logger.info(f"User '{user.name}' with ID '{user.id}' updated successfully!")
                # print("user.from_user: ", user.like.from_user)
                # print("user.like.is_allow: ", user.like.is_allow)
        return updated_user

 
    def GetUser(self, request, context):
        id = request.id
        for user in self.users:
            if user.id == id:
                return user
		
        raise grpc.RpcError(f"User with ID '{id}' not found!")


    def GetUsers(self, request, context):
        """Get all users

        Args:
                request (Empty): The GetUsersRequest message
                context: The grpc request context

        Returns:	
                User (stream User): The user list
        """
        try:
            for user in self.users:
                yield user
        except:
            self.logger.error(f"Error getting users!")
            return user_pb2.User()