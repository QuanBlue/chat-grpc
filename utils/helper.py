import datetime
from google.protobuf import timestamp_pb2

def GetCurrentTime(self):
   """Get the current time

   Returns:	
      google.protobuf.Timestamp: The current time.
   """
   # Get the current time
   current_time = datetime.utcnow()
   
   # Create a Timestamp object and set the current time
   timestamp = timestamp_pb2.Timestamp()
   timestamp.FromDatetime(current_time)

   return timestamp