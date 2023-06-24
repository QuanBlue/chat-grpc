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


def ClearScreen():
   """Clear the screen
   """
   os.system('cls' if os.name == 'nt' else 'clear')
   
def PaddingSpace(base_len, string_len):
   """_summary_

   Args:
      base_len (int): length of the base string
      string_len (int): length of the string to be padded

   Returns:
      padding: padding for the string
      remainder: remainder of the padding
   """
   padding = int((base_len - string_len) / 2)
   remainder = base_len - int((base_len - string_len) / 2)*2 - string_len
   
   return padding, remainder

def SliceMessage(msg, content_len):
   """Slice the message to fit the frame

   Args:
       msg (string): message to be sliced
       content_len (int): length of the message after sliced

   Returns:
       [string]: sliced message
   """
   sliced_msg = []
   
   start_idx = 0
   end_idx = start_idx
   msg_len = len(msg)
   
   if msg_len < content_len:
      sliced_msg.append(msg)
   else:
      while end_idx < msg_len:
         start_idx = end_idx
         end_idx += content_len
         
         sliced_msg.append(msg[start_idx:end_idx])
         
   return sliced_msg

def GetMaxLength(list_str):
   """Get the max length of the string in the list

   Args:
       list_str ([string]): list of string

   Returns:
       int: max length of the string in the list
   """
   max_len = max(len(s) for s in list_str)
   return max_len