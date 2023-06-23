import threading
import grpc

import services.grpc_generated.chat_pb2 as chat_pb2
import services.grpc_generated.chat_pb2_grpc as chat_pb2_grpc

import services.grpc_generated.user_pb2 as user_pb2
import services.grpc_generated.user_pb2_grpc as user_pb2_grpc


class ChatClient:
	def __init__(self):
		# Create a gRPC channel
		self.channel = grpc.insecure_channel('localhost:50051')

		# Create a stub for the service
		self.chat_stub = chat_pb2_grpc.ChatServiceStub(self.channel)
		self.user_stub = user_pb2_grpc.UserServiceStub(self.channel)

		# Do not specify the user ID, it will be assigned by the server
		self.user_name = input("Enter your name: ")
		self.user = chat_pb2.User(name=self.user_name)
		self.user = self.user_stub.CreateUser(self.user)

	def InputAndSendMsg(self):
		while True:
			msg_content = input("Enter your Message: ").rstrip('\n')

			# send msg to server
			message = chat_pb2.Message(sender=self.user, content=msg_content)
			response = self.stub.SendMessage(message)


	def run(self):
		threading.Thread(target=self.InputAndSendMsg, args=()).start()
		while True:
			self.ShowMessage()


if __name__ == '__main__':
	client = ChatClient()
	client.run()
