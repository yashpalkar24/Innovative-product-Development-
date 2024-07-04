import utils, scraper, report, json
from flask import Flask,render_template, request
from flask import jsonify
#from firebase import firebase
from firebase_admin import credentials, initialize_app, db ,_apps

import json
#firebase = firebase.FirebaseApplication("https://ipd0-6e264-default-rtdb.firebaseio.com/", authentication=None)
# Initialize Firebase Admin SDK with service account credentials

import firebase_admin
print(firebase_admin.get_app())




# def initialize_firebase():
#     if not _apps:
#         # Path to your Firebase credentials JSON file
#         SERVICE_ACCOUNT_KEY_PATH = "D:\\mirage-main\\ipd0-6e264-firebase-adminsdk-pruwz-5d051dd728.json"
#         cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
#         initialize_app(cred, {
#             'databaseURL': 'https://ipd0-6e264-default-rtdb.firebaseio.com/'
#         })

# # Initialize Firebase outside of any Flask route
# initialize_firebase()






# # Path to the service account key file
# SERVICE_ACCOUNT_KEY_PATH = "D:\mirage-main\ipd0-6e264-firebase-adminsdk-pruwz-5d051dd728.json"
# cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)


# firebase_client = firebase.FirebaseApplication("https://ipd0-6e264-default-rtdb.firebaseio.com/", authentication=None)
app = Flask(__name__)

@app.route("/", methods=['GET'])
def genReport():
    id = request.args.get('id')
    url = request.args.get('url')

    try:
        web_html = utils.getHTML(url)
        qna = utils.divideIntoQnA(web_html)
        output = report.generate_report(qna)
        db.reference('/privacy/' + id).update({'data': json.dumps(output), 'status': 'DONE'})
    except Exception as e:
        db.reference('/privacy/' + id).update({'status': 'ERROR'})
        return jsonify({'error': str(e)})

    return jsonify({'message': 'Process complete'})


@app.route("/api2/", methods=['GET'])
def scaperApi():
    #?url=
    url = request.args.get('url')
    #?id=
    id = request.args.get('id')
    try:
        output2 = scraper.scrap(url)
        # db.reference('/gdpr/' + id).update({'data': json.dumps(output2), 'status': 'DONE'})
        db.reference('/gdpr/' + id).update({'data': json.dumps(output2), 'status': 'DONE'})
        
        # Fetch data from Firebase based on the provided ID
        firebase_data = db.reference('/gdpr/' + id).get()

        if firebase_data:
            print(jsonify(firebase_data))
            return jsonify(firebase_data)
        else:
            return jsonify({'error': 'Data not found for the provided ID'})
    except:
        db.reference('/gdpr/' + id).update({'status': 'ERROR'})

    return "True"

if __name__ == '__main__':
    app.run(debug=True)
    
