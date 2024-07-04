import streamlit as st
import json
from firebase_admin import credentials, initialize_app, db

# import firebase_admin
# print(firebase_admin.get_app())

# Initialize Firebase Admin SDK
# cred = credentials.Certificate("D:\mirage-main\ipd0-6e264-firebase-adminsdk-pruwz-5d051dd728.json")
# initialize_app(cred, {'databaseURL': 'https://ipd0-6e264-default-rtdb.firebaseio.com/'})

def fetch_data(ref_path):
    ref = db.reference(ref_path)
    return ref.get()

st.title('SAFE SURF')

st.title('Privacy Policy Checker')

id = st.text_input('Enter ID to fetch data:', '')

if st.button('Fetch Data'):
    data = fetch_data(f'/gdpr/{id}')
    if data and 'data' in data:
        processed_data = json.loads(data['data'])
        # Assuming processed_data contains a numeric value or percentage
        st.progress(processed_data / 100.0)
    else:
        st.error('No data found for this ID.')

st.sidebar.info('Enter the ID and press "Fetch Data" to see the visualization.')
