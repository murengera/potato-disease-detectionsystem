from fastapi import  File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import firebase_admin
from firebase_admin import credentials,auth
import pyrebase
from models import  LoginSchema,SignUpSchema
from fastapi.responses import JSONResponse
from fastapi import HTTPException



app = FastAPI(
    description="Student Perfomance",
    title="Student Perfomance",
    docs_url="/"
)




if not firebase_admin._apps:

     cred = credentials.Certificate("serviceaccount.json")
     firebase_admin.initialize_app(cred)


firebaseConfig = {
  "apiKey": "AIzaSyCR3Y3-onw-sYfhYejRexl5ucH4S8RJrq0",
  "authDomain": "fir-auth-c3a80.firebaseapp.com",
  "projectId": "fir-auth-c3a80",
  "storageBucket": "fir-auth-c3a80.appspot.com",
  "messagingSenderId": "108748216311",
  "appId": "1:108748216311:web:bfee68e2a27a9d14ce00f2",
  "measurementId": "G-LJHRP3L195",
   "databaseURL":""
}

firebase=pyrebase.initialize_app(firebaseConfig)
@app.post('/signup')
async def create_an_account(user_data:SignUpSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = auth.create_user(
            email = email,
            password = password
        )

        return JSONResponse(content={"message" : f"User account created successfuly for user {user.uid}"},
                            status_code= 201
               )
    except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail= f"Account already created for the email {email}"
        )



@app.post('/login')
async def create_access_token(user_data:LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=email,
            password = password
        )

        token = user['idToken']

        return JSONResponse(
            content={
                "token":token
            },status_code=200
        )

    except:
        raise HTTPException(
            status_code=400,detail="Invalid Credentials"
        )


origins = [
    "http://localhost",
    "http://localhost:8100",
    "http://192.168.1.77:8100",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL =tf.keras.models.load_model("../saved_models/1")

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
