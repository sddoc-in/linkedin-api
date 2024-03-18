# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi


# uri = "mongodb+srv://admin:BTzG4AjRskOaeFeb@leads.nhrq5wp.mongodb.net/?retryWrites=true&w=majority&ssl=true"

# client = MongoClient(uri, server_api=ServerApi('1'), tls=True,
#                              tlsAllowInvalidCertificates=True)

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)



message  =  "hi {first_name} {last_name} how are you?" 
first_name = "Animesh"
last_name = "Singh"
sendmessage = message.replace("{first_name}", first_name).replace("{last_name}", last_name)
print(sendmessage)  #  hi Animesh Singh how are you?

first_name = "Darakhsha"
last_name = "Rayeen"
sendmessage = message.replace("{first_name}", first_name).replace("{last_name}", last_name)
print(sendmessage) #  hi Darakhsha Rayeen how are you?
