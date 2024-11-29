const api_endpoint = 'http://127.0.0.1:5000'

async function getLastBackupDate() {
    try {
            const endPointUrl = api_endpoint + '/get_last_backup_date';
            // fetching data from endpoint
            const response = await fetch(endPointUrl);

            if (!response.ok) {
                throw new Error(`HTTP error! Status! -> ${response.status}`);
            }

            const data = await response.json();

            const lastBackupDate = data.backup_time || 'Unknown date';
            // updating the DOM element with data
            document.getElementById('last_backup_date').textContent = lastBackupDate;
        } catch(error) {
            console.error('Error in fetching data: ', error);
            document.getElementById('last_backup_date').textContent = 'Error in fetching date';
        }
}

// getting file count info which are ready to backup
async function getFileToBackUpData() {
    try {
        const endPointUrl = api_endpoint + '/get_file_count';

        const response = await fetch(endPointUrl);
        if(!response) {
            throw new Error(`HTTP Error! Status : ${response.status}`);
        }
        const data = await response.json();

        // updating DOM
        document.getElementById('totalFileCount').textContent = data.total;
        document.getElementById('imageFileCount').textContent = data.images;
        document.getElementById('videoFileCount').textContent = data.videos;
        
    } catch(error) {
        console.error("Error fetching backup file data :", error);
        document.getElementById('totalFileCount').textContent = 'n/a';
        document.getElementById('imageFileCount').textContent = 'n/a';
        document.getElementById('videoFileCount').textContent = 'n/a';
    }
}

// HDD Connection check through api call
async function checkHddConnection() {
  try {
    const endpointUrl = api_endpoint + '/get_hdd_connection_status';
    const response = await fetch(endpointUrl);
    if(!response) {
        throw new Error(`HTTP Error! Status : ${response.status}`);
    }
    const data = await response.json();
    if(data.status == false) {
        const hddConnCheck = document.getElementById("hddStatusCheck");
        if(hddConnCheck && hddConnCheck.classList.contains('is-hidden')) {
            hddConnCheck.classList.remove('is-hidden');
        }
    }
  } catch (error) {
    console.error("Error in checking hdd connection :", error);
  }
}

function initializePage() {
    getLastBackupDate();
    getFileToBackUpData();
    checkHddConnection();
}

// calling the function when page loads
document.addEventListener('DOMContentLoaded', initializePage);