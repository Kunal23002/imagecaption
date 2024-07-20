import streamlit as st
import requests

st.title("File Upload")

st.write("This is a simple interface to upload a file to the backend.")

# File uploader widget
uploaded_file = st.file_uploader("Choose a file", type = ['jpg','jpeg','png'])

if st.button('Upload'):
    # if uploaded_file is not None:
        try:
            #if button clicked - start the processing with current image
            files = {'file':(uploaded_file.name, uploaded_file , uploaded_file.type)}
            response = requests.post('http://127.0.0.1:8000/uploadfile', files=files)

            if response.status_code == 200:
                st.write("Backend response:")
                response_data = response.json() #parsing the json data sent by the server
                captions = response_data['captions']
                hashtags = response_data['hashtags']
                st.write("Captions:")
                for caption in captions:
                    st.write(caption)  
                st.write("\nHashtags:", hashtags)
                print(response)
            else:
                st.write(f'Failed to upload file. Status code: {response.status_code}')
                st.write(response.text)
        except Exception as e:
            st.write('Error occurred:', e)
    # else:
    #     st.write("Please upload a file.")