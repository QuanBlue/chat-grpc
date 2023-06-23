import sys
import os

root_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
grpc_gen_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../services/grpc_generated/')))
utils_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils/')))

sys.path.append(root_dir)
sys.path.append(grpc_gen_dir)
sys.path.append(utils_dir)

import grpc
from concurrent import futures

# grpc_gen_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '../services/grpc_generated/')))
# sys.path.append(grpc_gen_dir)

# import user_pb2_grpc
# import chat_pb2_grpc


# service_class_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), './services_class/')))
# sys.path.append(service_class_dir)

# from user_service import UserServiceServicer 
# from chat_service import ChatServiceServicer 

# import services.grpc_generated.user_pb2_grpc as user_pb2_grpc
from services.grpc_generated import user_pb2_grpc
from services.grpc_generated import chat_pb2_grpc

from server.services_class.user_service import UserServiceServicer 
from server.services_class.chat_service import ChatServiceServicer 

"""
Main entry point for the gRPC server.
"""
def Server():
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
	print("Server started")

	# since server.start() will not block,
	server.wait_for_termination()


if __name__ == '__main__':
	Server()
