# DUMPIFY
A local web app to make your process of organizing and storing media files an easy one.

Description:
--
You dump all your media files in a dump or source media folder, this web-app helps you to organize your media in a folder in which it will move your files to folder of which that file is created or modified (date). It moves all the media files ie, image and videos to your desired folder location.
For example:
Your file name : sample.mp4 (date : 12-11-2024)
Your target folder path : /home/user/backup

Since this file's creation or modified date is 12-11-2024, now this web-app will move this file based on the year and month of the file.
New organized file path : /home/user/backup/2024/Nov/sample.mp4

---
## **Features**

-   Moves files from a source folder (dump folder) to a target folder.
-   Organizes media files by **year** and **month**.
-   Supports media file types like photos and videos.
-   Helps declutter your storage and arrange media files systematically.

## **Technologies Used**

-   **Backend**: Python 3.9.13, Flask 3.1.3
-   **Frontend**: HTML5, JavaScript, Bulma CSS framework
-   **Environment Variables**: Configurable source and target folder paths.

## **Installation Instructions**

### **Prerequisites**

-   Python 3.9.13 (or later)
-   Pip (Python package manager)

### **Setup**

1.  Clone the repository:
    
        git clone https://github.com/soumenpasari/dumpify.git
    cd media-file-organizer

   
2.  Create a virtual environment:
    
`python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate` 
    
3.  Install required Python packages:
    
    `pip install -r requirements.txt` 
    
4.  Install Flask 3.1.3:
    
    `pip install flask==3.1.3` 
    

----------

## **Environment Variables**

Set the following environment variables in a `.env` file or export them directly in your environment:

| Variable name |Description  | Example
|--|--|--
| `MEDIA_FOLDER` | Path to the source file folder | `/path/to/source/folder`
| `TARGET_FOLDER` | Path to the target folder| `/path/to/target/folder`
| `HARDDRIVE_FOLDER` | Path to the hard disk | `H:\`
| `BACKDATAFILE` | name of the file which stores meta data of process | meta_data.json


### **Example `.env` File**

    SOURCE_FOLDER=/path/to/source/folder
    TARGET_FOLDER=/path/to/target/folder
    HARDDRIVE_FOLDER=H:\
    BACKDATAFILE=meta_data.json

----------

## **Usage**

1.  Run the Flask application:
    `python run.py` 
    
2.  Access the web interface in your browser:
    `http://127.0.0.1:5000` 
    
3.  Use the interface to trigger the file organization process i.e. choose the media type and click on the button to trigger the process.
    

----------

## **Frontend**

-   **CSS Framework**: [Bulma](https://bulma.io/) (Lightweight, responsive CSS framework).
-   **Technologies**: HTML5, JavaScript.
----------
## Timeline
This project is a work in progress for now. Though it's main function is complete i.e. move files in a organized manner to another folder which is mostly considered your hard disk.
Time allotted to this project for now : ***14 hrs 50 mins.***
It includes all the process from scratch in designing, creating basic API functionality, handling basic JavaScript functionalities, testing basic functionalities.
Few things are there which is not completed yet, like error handling and showing it to user which are necessary.

## **Contributing**

Contributions are welcome! Feel free to fork the repository and submit a pull request.

----------

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.

----------

### **Contact**

For any issues or suggestions, please contact:

-   **Name**: Soumen Pasari
-   **Email**: soumenpasari849@gmail.com
