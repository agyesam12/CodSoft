document.addEventListener('DOMContentLoaded', function() {
  const dueDates = document.querySelectorAll('.due-date');
  dueDates.forEach(function(dueDate) {
    const dueDateValue = new Date(dueDate.getAttribute('data-due-date'));
    const today = new Date();
    const timeDiff = dueDateValue - today;
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));

    // Calculate the total days from today to the due date
    const totalDays = Math.ceil((dueDateValue - today) / (1000 * 3600 * 24));
    const percentage = Math.max(0, Math.min(100, (daysDiff / totalDays) * 100));

    // Set the background color based on the percentage
    dueDate.style.background = `linear-gradient(to right, red ${percentage}%, green ${percentage}%)`;
  });
});
