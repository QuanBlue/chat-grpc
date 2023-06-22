import service.grpc_generated.user_pb2 as user_pb2
import service.grpc_generated.user_pb2_grpc as user_pb2_grpc

class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
	def __init__(self):
		pass

	def CreateUser(self, request, context):
		pass