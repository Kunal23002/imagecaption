from flask import Flask, request, jsonify
from flask_cors import CORS
from io import BytesIO
from transformers import pipeline, VisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
from PIL import Image
import os
import numpy as np
import nltk
from nltk.corpus import stopwords
import boto3
import re
# nltk.download('stopwords') #download stopwords if not already downloaded

#definining model parameters
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning") #model used to generate captions
feature_extractor = ViTFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning") #preprocesses the images so that they can be fed into the model
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
max_length = 16
num_beams = 7  # how many candidate sequences at each step
num_return_sequences = 4  # number of captions to generate by the decoder
gen_kwargs = {"max_length": max_length, "num_beams": num_beams, "num_return_sequences": num_return_sequences}
hashtags = pipeline("summarization")

#defining amazon bucket parameters
s3 = boto3.resource('s3')
bucket = 'imagecaptionbucket-1'
upload_count = 0 #this variable keeps track of the number of uploads that are being made.




def predict_step(images):
    pixel_values = feature_extractor(images=images, return_tensors="pt").pixel_values  # preprocess image to make it suitable for the model
    output_ids = model.generate(pixel_values, **gen_kwargs)
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    preds = [pred.strip() for pred in preds]
    return ".".join(preds)

def generate_hashtags(captions):
    # little preprocessing before summarizing
    cleaned_text = captions.replace('\n', '. ')
    joined_text = cleaned_text.rstrip('. ') + '.'
    # passing it to the summarizer
    hash = hashtags(joined_text, max_length=10, min_length=2, do_sample=False)
    hash = hash[0]['summary_text']
    hash = ' '.join([word for word in hash.split() if word.lower() not in stopwords.words('english')])
    return hash

def predict_and_generate(input_image):
    captions = predict_step(input_image)
    hashtags = generate_hashtags(captions)
    captions = list(captions.split('.'))
    return (captions, ("#" + hashtags).replace(" ", " #"))

def upload_cloud(image):
    try:
        global upload_count
        upload_count += 1
        image_file_name = f'image_{upload_count}.jpg'

        # Convert PIL image to bytes - as put_object method expects a byte file or a byte array
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        #store the image in the aws s3 storage.
        s3.Bucket(bucket).put_object(Key=image_file_name, Body=img_byte_arr)

    except Exception as e:
        print(e) 


app = Flask(__name__)
CORS(app)  

@app.route('/uploadfile', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'message':'No file was found'}) , 400
       
        file = request.files['file']
        if file.filename == '':
            return jsonify({"message":'No file selected'}),400

        image = Image.open(BytesIO(file.read())).convert("RGB")  # Load the image using PIL
        captions, hashtags = predict_and_generate(image)
        upload_cloud(image) #function to upload image to s3 bucket
        print(captions)
        return jsonify({"captions": captions, "hashtags": hashtags}), 200
        
    except Exception as e: 
        print(f"An error occurred: {e}")
        return jsonify({"message": str(e)}), 500  # Respond with a status code 500 (Internal Server Error)

if __name__ == '__main__':
    app.run(port=8000)  # Run on port 8000