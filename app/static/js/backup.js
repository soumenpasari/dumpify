/**
 * Code for backing up file or the process
 */
const backupBtn = document.getElementById("backUpBtn");
const mediaType = document.getElementById("mediaType");
const backupNotificaton = document.getElementById('backupNotificaton');
const bckNotificationClose = document.getElementById('backupNotificatonDelete')
const dataContentDiv = document.getElementById("dataContentDiv");
const backUpLogTitle = document.getElementById('backUpLogTitle');
const fileLogTable = document.getElementById("fileLogTable");
const fileLogTableBody = document.getElementById("fileLogTableBody");
const notMsg = document.getElementById('notMsg');

async function backUpMedia() {
    const mediaTypeValue = mediaType.value;
    
    if(mediaTypeValue !== '0') {
        // adding button loading animation
        backupBtn.classList.add('is-loading');
        // calling api
        const backUpEndpoint = api_endpoint + '/backup_file/' + mediaTypeValue;

        try {
            const response = await fetch(backUpEndpoint);
            if (!response) {
                throw new Error(`HTTP ERROR! Status : ${response.status}`);
            }
            const data = await response.json();
            backupBtn.classList.remove('is-loading');
            // updating the last back-up date text
            getLastBackupDate();
            // updating the file count which are ready to backup
            getFileToBackUpData();
            backupNotificaton.classList.add('is-hidden');
            // show content on table
            if (data.length !== 0) {
                showDataOnTable(data);
            } else {
                backupNotificaton.classList.remove('is-hidden');
                notMsg.textContent = 'There is no file to back-up!';
            }
        } catch(error) {
            console.log('Error : ',error);
        }
    } else {
        backupNotificaton.classList.remove('is-hidden');
        notMsg.textContent='Please select media type!';
    }
}

/**
 * handles the process of data content div
 */
function showDataOnTable(backupData) {

    dataContentDiv.classList.remove('is-hidden');
    backUpLogTitle.classList.add('animate__animated','animate__fadeInDown');
    fileLogTable.classList.add('animate__animated','animate__fadeInDown');
    thKeys = Object.keys(backupData[0]);
    backupData.forEach(dataItem => {
        const tableRow = document.createElement('tr');
        tableRow.classList.add('animate__animated','animate__flipInX');

        const tds = ['file_name','file_extension','file_size','modified_time'].map(key => {
            const td = document.createElement('td');
            td.textContent = dataItem[key];
            return td;
        });

        tableRow.append(...tds);
        fileLogTableBody.appendChild(tableRow);
    });
}

backupBtn.addEventListener("click",()=>{
    backUpMedia();
});

bckNotificationClose.addEventListener("click", () => {
    backupNotificaton.classList.add('is-hidden');
});