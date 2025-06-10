# AI Image Captioning System

An intelligent image captioning system that generates descriptive captions and relevant hashtags for uploaded images using state-of-the-art AI models. The system combines computer vision and natural language processing to create Instagram-style captions.

## Features

- **Image Captioning**: Generates multiple descriptive captions for uploaded images
- **Hashtag Generation**: Automatically creates relevant hashtags from captions
- **Cloud Storage**: Stores images in AWS S3 bucket
- **Database Integration**: Maintains a record of all processed images and their captions
- **User-friendly Interface**: Simple web interface built with Streamlit
- **RESTful API**: Backend service built with Flask

## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Flask
- **AI Models**: 
  - Vision Encoder-Decoder (ViT-GPT2) for image captioning
  - Transformers pipeline for hashtag generation
- **Database**: MySQL
- **Cloud Storage**: AWS S3
- **Additional Libraries**: 
  - NLTK for text processing
  - PIL for image handling
  - Boto3 for AWS integration

## Prerequisites

- Python 3.x
- MySQL Server
- AWS Account with S3 bucket
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd image-caption
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
```sql
CREATE DATABASE `image-caption`;
USE `image-caption`;

CREATE TABLE `image_data` (
  `image_id` varchar(255) NOT NULL,
  `captions` text NOT NULL,
  `hashtags` text NOT NULL,
  PRIMARY KEY (`image_id`)
);
```

4. Configure AWS credentials:
   - Create an AWS account if you don't have one
   - Create an S3 bucket named 'imagecaptionbucket-1'
   - Configure AWS credentials in your environment

## Running the Application

1. Start the backend server:
```bash
cd server
python app.py
```

2. Start the frontend client:
```bash
cd client
streamlit run index.py
```

3. Access the application at `http://localhost:8501`

## Usage

1. Open the web interface in your browser
2. Click "Choose a file" to select an image
3. Click "Upload" to process the image
4. View the generated captions and hashtags

## Project Structure

```
image-caption/
├── client/
│   └── index.py          # Streamlit frontend
├── server/
│   └── app.py           # Flask backend
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## API Endpoints

### POST /uploadfile
- **Purpose**: Upload and process an image
- **Input**: Image file
- **Output**: JSON containing captions and hashtags
- **Response Format**:
  ```json
  {
    "captions": ["caption1", "caption2", ...],
    "hashtags": "#tag1 #tag2 ..."
  }
  ```

## Model Details

- **Image Captioning Model**: ViT-GPT2
  - Vision Transformer (ViT) for image encoding
  - GPT-2 for text generation
  - Generates multiple captions per image
  - Maximum caption length: 16 tokens
  - Beam search with 7 beams

- **Hashtag Generation**:
  - Uses text summarization pipeline
  - Removes stopwords
  - Formats output as Instagram-style hashtags

## Contributing

Feel free to submit issues and enhancement requests!
