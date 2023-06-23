import datetime
import os
from google.protobuf import timestamp_pb2

def GetCurrentTime():
   """Get the current time

   Returns:	
      String: The current time in the format HH:MM:SS
   """
   print("--- GET CURRENT TIME ---")
   
   current_time = datetime.datetime.now()
   formatted_time = current_time.strftime("%H:%M:%S")
   
   print("formatted_time:", formatted_time)
   
   return formatted_time


def ClearScreen(self):
   os.system('cls' if os.name == 'nt' else 'clear')