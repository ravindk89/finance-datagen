import random

class Client:
   
   def __init__(self, client_company, clearing):
       self.client = []
       self.client_company = client_company
       self.clearing = clearing

   def add_client(self, client):
       self.client.append(client)

   def return_details(self):
       ret = {
           "client" : random.choice(self.client),
           "Company" : self.client_company
           }
           
       return ret

   def return_clearing(self):
       return random.choice(self.clearing)