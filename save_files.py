import os

def save_uploaded_files(uploaded_files, directory):
    for uploaded_file in uploaded_files:
        with open(os.path.join(directory, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getvalue())