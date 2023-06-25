import os, sys

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
            
            # Add the new_user to the list
            self.users.append(new_user)
            
            self.logger.info(f"User '{new_user.name}' with ID '{new_user.id}' created successfully!")            
            return new_user
        except:
            # Prepare the response
            new_user = user_pb2.CreateUserResponse()
            self.logger.error(f"User '{new_user.name}' with ID '{new_user.id}' created Fail!")            

