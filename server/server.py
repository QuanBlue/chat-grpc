import grpc
from concurrent import futures

import service.grpc_generated.chat_pb2_grpc as chat_pb2_grpc
import service.grpc_generated.user_pb2_grpc as user_pb2_grpc

from services.user_service import UserServiceServicer 
from services.chat_service import ChatServiceServicer 

"""
Main entry point for the gRPC server.
"""
def serve():
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
	serve()
