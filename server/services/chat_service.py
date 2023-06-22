import service.grpc_generated.chat_pb2 as chat_pb2
import service.grpc_generated.chat_pb2_grpc as chat_pb2_grpc


class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
	def __init__(self):
		pass

	def SendMessage(self, request, context):
		pass

	def ReceiveMessage(self, request, context):
		pass
	