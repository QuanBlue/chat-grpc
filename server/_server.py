import os, sys

root_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
grpc_gen_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../services/grpc_generated/')))
utils_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils/')))
sys.path.append(root_dir)
sys.path.append(grpc_gen_dir)
sys.path.append(utils_dir)

import grpc
from concurrent import futures

from services.grpc_generated import user_pb2_grpc
from services.grpc_generated import chat_pb2_grpc

from server.services_class.user_service import UserServiceServicer 
from server.services_class.chat_service import ChatServiceServicer 


from utils.logger import *

"""
Main entry point for the gRPC server.
"""
def Server():
   logger = Logger()
   
   # create a gRPC server
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	
	# add servicers to the server
   chat_pb2_grpc.add_ChatServiceServicer_to_server(
		ChatServiceServicer(), server)
   user_pb2_grpc.add_UserServiceServicer_to_server(
		UserServiceServicer(), server)
	
	# listen on port 50051
   server.add_insecure_port('[::]:50051')

   # start gRPC server
   server.start()
   logger.info('Server started on port 50051...')

	# since server.start() will not block,
   server.wait_for_termination()


if __name__ == '__main__':
	Server()
