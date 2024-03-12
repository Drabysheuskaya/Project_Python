// static/scripts.js
function openPopup() {
document.getElementById("popup").style.display = "block";
}


function closePopup() {
  const popup = document.getElementById("popup");
  popup.style.display = "none";
}





function deleteActivity(scheduleId) {
  fetch(`/timetable/${scheduleId}`, {
    method: 'DELETE',
  })
  .then(response => {
    if (response.ok) {
      location.reload();
    } else {
      console.error('Failed to delete schedule:', response.statusText);
    }
  })
  .catch(error => {
    console.error('An error occurred while deleting the schedule:', error);
  });
}





