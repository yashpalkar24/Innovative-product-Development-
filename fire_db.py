# import firebase_admin
# from firebase_admin import credentials, initialize_app, db

# def init_firebase():
#     # Path to your Firebase service account key file
#     key_path = 'D:\\mirage-main\\ipd0-6e264-firebase-adminsdk-pruwz-5d051dd728.json'
    
#     # Initialize the app with a service account, granting admin privileges
#     cred = credentials.Certificate(key_path)
#     firebase_app = initialize_app(cred, {
#         'databaseURL': 'https://ipd0-6e264-default-rtdb.firebaseio.com/'
#     })
    
#     return firebase_app

# # Export the initialized app
# firebase_asset = init_firebase()

# # Example usage of the Firebase Realtime Database
# def get_database_reference():
#     # Reference to the database
#     ref = db.reference('/')
#     return ref

# # # Get the database reference
# database_ref = get_database_reference()

# # # Example to write data
# # database_ref.set({
# #     'users': {
# #         'user001': {
# #             'name': 'John Doe',
# #             'email': 'john@example.com'
# #         }
# #     }
# # })

# # # Example to read data
# # users_data = database_ref.child('users').get()
# # print(users_data)

# print(firebase_asset)
# print(database_ref)