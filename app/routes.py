from flask import Blueprint, render_template
# importing inner modules
from app.controller.file_controller import FileController

#creating blueprint
main = Blueprint('main', __name__)

fc_obj = FileController()

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/get_file_count')
def get_file_count():
    '''
        Get information about the count of files ready to backup or move
        from source media folder to target media folder
    '''
    return fc_obj.get_file_count()

@main.route('/get_hdd_connection_status')
def get_hdd_connection_status():
    '''
        Get connection status of the hard disk or the target folder
        status to which files will be moved
    '''
    return fc_obj.check_hdd_conn()

@main.route('/get_last_backup_date')
def get_last_backup_date():
    '''
        Get the date of last moving files from source folder to target folder
    '''
    return fc_obj.get_last_backup_date()

@main.route('/backup_file/<file_type>', methods=['GET'])
def backup_media(file_type):
    '''
        Backup the media files from soruce to target folder
    '''
    return fc_obj.back_up_files(file_type)