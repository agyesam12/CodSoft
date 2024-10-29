document.addEventListener('DOMContentLoaded', function() {
  const dueDates = document.querySelectorAll('.due-date');
  dueDates.forEach(function(dueDate) {
    const dueDateValue = new Date(dueDate.getAttribute('data-due-date'));
    const today = new Date();
    const timeDiff = dueDateValue - today;
    const totalDays = (dueDateValue - new Date(today.getFullYear(), today.getMonth(), today.getDate() - 16)) / (1000 * 3600 * 24);
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));

    const percentage = Math.max(0, Math.min(100, (daysDiff / totalDays) * 100));

    // Apply the calculated percentage to the progress bar
    const progressBar = dueDate.parentElement.querySelector('.progress-bar');
    progressBar.style.width = `${percentage}%`;
    progressBar.textContent = `${Math.round(percentage)}%`;

    // Set background color based on urgency (green when far from due, red when close)
    if (percentage > 50) {
      progressBar.style.backgroundColor = 'green';
    } else if (percentage > 20) {
      progressBar.style.backgroundColor = 'orange';
    } else {
      progressBar.style.backgroundColor = 'red';
    }
  });
});