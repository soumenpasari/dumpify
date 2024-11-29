'''
    Controller class for file related operations
'''
import os, imghdr, mimetypes, shutil, json
from pathlib import Path
from datetime import datetime
from flask import jsonify


class FileController:

    def __init__(self):
        self.HDD_LOCATION = os.getenv("HARDDRIVE_FOLDER")
        self.MEDIA_FILE_LOC = os.getenv("MEDIA_FOLDER")
        self.BACKUPDATA_FILE = os.getenv("BACKDATAFILE")
        # image and video type extension dict
        self.video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv")
        self.image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp")
    
    def check_hdd_conn(self):
        '''
            Check if the hard drive is plugged in or not

        '''
        final_result = {
            'status' : False
        }
        folder = Path(self.HDD_LOCATION)
        if folder.is_dir():
            final_result['status'] = True
        return jsonify(final_result)
        

    def get_file_count(self)->dict:
        '''
            Return the number of files based on the file type
            
            Returns:
                dict of total number of files with key of image and video
        '''
        final_result = {
            'images' : 0,
            'videos' : 0,
            'total' : 0
        }

        if not os.path.isdir(self.MEDIA_FILE_LOC):
            print('Media folder not available!')
            return final_result
        
        for file_name in os.listdir(self.MEDIA_FILE_LOC):
            file_path = os.path.join(self.MEDIA_FILE_LOC,file_name)
            if os.path.isfile(file_path):
                if imghdr.what(file_path) or file_name.lower().endswith(self.image_extensions):
                    final_result['images'] += 1
                elif file_name.lower().endswith(self.video_extensions) or (mimetype := mimetypes.guess_type(file_path)[0]) and mimetype.startswith("video"):
                    final_result['videos'] += 1
        
        final_result['total'] = final_result['images'] + final_result['videos']
        
        return jsonify(final_result)
    
    def back_up_files(self,file_type=None)->list:
        '''
            backup the file from source media location to hdd location
            according to the media type
            
            Returns:
                returns a list of total files moved
        '''
        # checking the file_type has any other value or not
        if file_type not in [None,'image','video']:
            file_type = None
        if not os.path.isdir(self.MEDIA_FILE_LOC):
            return "Media folder don't exist! Check env variable."
        files_moved = []
        for file_name in os.listdir(self.MEDIA_FILE_LOC):
            file_path = os.path.join(self.MEDIA_FILE_LOC,file_name)
            if os.path.isfile(file_path):
                #process of image backup
                if file_name.lower().endswith(self.image_extensions) and (file_type == 'image' or file_type == None):
                    moved_file = self.move_files(file_path,os.getenv("TARGET_FOLDER"),'Image')
                    if len(moved_file) != 0:
                        files_moved.append(moved_file)
                elif (file_name.lower().endswith(self.video_extensions) or(mimetype := mimetypes.guess_type(file_path)[0]) and mimetype.startswith("video")) and (file_type == 'video' or file_type == None):
                    moved_file = self.move_files(file_path,os.getenv("TARGET_FOLDER"),'Video')        
                    if len(moved_file) != 0:
                        files_moved.append(moved_file)
        # writing the backup_data file
        if len(files_moved) != 0:
            self.create_backup_data_file(file_type)
        return jsonify(files_moved)
    
    def get_file_stats(self,file_path:str)->dict:
        '''
            Returns a dict with information related to file
            like file created_date, modified_date, file name, file_size

            Args:
                file_path(str): full file path of the file to get stats about

            Returns:
                Dict with info about that file
        '''
        file_stats = os.stat(file_path)
        file_name = os.path.basename(file_path)
        _,file_extension = os.path.splitext(file_name)
        return {
            'file_name' : file_name,
            'file_size': file_stats.st_size, # in bytes
            'created_date': file_stats.st_ctime, # it changes if you copy and paste the file
            'modified_time': file_stats.st_mtime, # it depicts the date of creation mostly
            'file_extension': file_extension
        }

    def create_folder_for_file(self,target_folder:str,file_timestamp,file_type:str)->str:
        '''
            Creates folder of year and month for the file to be backed up based on the file's modified timestamp

            Args:
                target_folder(str): target folder inside which year and month folders will be created
                file_stamp(str): timestamp or mostly it will be modified date of the file
            
            Returns:
                returns the folder name that is created
        
        '''
        
        file_timestamp = float(file_timestamp)
        file_year = datetime.fromtimestamp(file_timestamp).year
        file_month = datetime.fromtimestamp(file_timestamp).strftime("%B")
        folder_to_create = os.path.join(target_folder,str(file_year),file_month,file_type)
        try:
            os.makedirs(folder_to_create, exist_ok=True)
            return folder_to_create
        except Exception as e:
            print(f'Error in creating folder: {e}')
            return ""
    
    def move_files(self,source_file:str,target_folder:str,file_type)->dict:
        '''
            Moves a file from source folder to target folder

            Args:
                file_name(str): name of the file to move
                source_folder(str): folder path which is the source folder of the file
                target_folder(str): folder path to which the file will be moved or copied

            Returns:
                returns the file information such as file_name, size, type and modified date
        '''

        try:
            # check if the file exists or not
            if not os.path.isfile(source_file):
                print("File doesn't exist")
                return {}
            # get file info before creating folder related to this file
            source_file_info = self.get_file_stats(source_file)
            # create folder to move file to that folder
            created_target_folder = self.create_folder_for_file(target_folder,source_file_info['modified_time'],file_type)
            #TODO:: Check created_target_folder is a real path or not then move the file
            # else return proper error
            shutil.move(source_file, created_target_folder)
            source_file_info['modified_time'] = datetime.fromtimestamp(source_file_info['modified_time']).strftime("%d-%m-%Y")
            source_file_info['file_size'] = round(source_file_info['file_size'] / (1024 * 1024),2)
            return source_file_info
        except Exception as e:
            print(f"Error in moving file : {e}")
            return {}
    
    def create_backup_data_file(self,backup_type):
        '''
            Creates one text file in the destination folder
            which have json about last backed-up date and file type
            that got backed-up
        '''
        back_up_info = {
            'backup_time' : datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'back_up_type': backup_type
        }
        file_name = os.path.join(self.MEDIA_FILE_LOC,self.BACKUPDATA_FILE)
        # writing the info to file as json
        try:
            with open(file_name, "w") as backup_data_file:
                json.dump(back_up_info,backup_data_file, indent=4)
            return True
        except Exception as e:
            print(f"Exception occured -> {e}")
            return False
    
    def get_last_backup_date(self):
        '''
            Returns the date of last backup process done to move the files
            from source folder to target folder
            
        '''
        file_path = os.path.join(self.MEDIA_FILE_LOC,self.BACKUPDATA_FILE)
        try:
            with open(file_path,'r') as backup_date_file:
                file_data = json.load(backup_date_file)
                return jsonify(file_data)
        except FileNotFoundError:
            print("Backup data file not found")
            return {}
        except json.JSONDecodeError:
            print("Error in json decoding")
            return {}
        except Exception as e:
            print(f"Error ->{e}")
