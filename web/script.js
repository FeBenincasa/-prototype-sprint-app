// Task Reminder App - JavaScript
// Handles communication between frontend and Python backend via Eel

// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize the application
function initializeApp() {
    loadTasks();
    setupEventListeners();
    console.log('Task Reminder App initialized!');
}

// Setup event listeners
function setupEventListeners() {
    // Add task form
    const taskForm = document.getElementById('taskForm');
    taskForm.addEventListener('submit', handleAddTask);
    
    // Refresh tasks button
    const refreshBtn = document.getElementById('refreshTasks');
    refreshBtn.addEventListener('click', loadTasks);
    
    // Send reminder button
    const sendReminderBtn = document.getElementById('sendReminder');
    sendReminderBtn.addEventListener('click', handleSendReminder);
}

// Handle add task form submission
async function handleAddTask(event) {
    event.preventDefault();
    
    const titleInput = document.getElementById('taskTitle');
    const dateInput = document.getElementById('taskDate');
    
    const title = titleInput.value.trim();
    const dueDate = dateInput.value || null;
    
    if (!title) {
        showMessage('Please enter a task title', 'error');
        return;
    }
    
    try {
        // Call Python function to add task
        const result = await eel.py_add_task(title, dueDate)();
        
        if (result) {
            showMessage('Task added successfully!', 'success');
            titleInput.value = '';
            dateInput.value = '';
            loadTasks(); // Refresh the task list
        } else {
            showMessage('Failed to add task', 'error');
        }
    } catch (error) {
        console.error('Error adding task:', error);
        showMessage('Error adding task', 'error');
    }
}

// Load and display all tasks
async function loadTasks() {
    const container = document.getElementById('tasksContainer');
    container.innerHTML = '<div class="loading">Loading tasks...</div>';
    
    try {
        // Call Python function to get tasks
        const tasks = await eel.py_get_tasks()();
        
        if (tasks.length === 0) {
            container.innerHTML = '<div class="no-tasks">No tasks yet. Add your first task above! 🎯</div>';
            return;
        }
        
        // Render tasks
        container.innerHTML = '';
        tasks.forEach(task => renderTask(task));
        
    } catch (error) {
        console.error('Error loading tasks:', error);
        container.innerHTML = '<div class="error">Failed to load tasks</div>';
    }
}

// Render a single task
function renderTask(task) {
    const container = document.getElementById('tasksContainer');
    const template = document.getElementById('taskTemplate');
    const taskElement = template.content.cloneNode(true);
    
    // Set task data
    const taskItem = taskElement.querySelector('.task-item');
    taskItem.setAttribute('data-task-id', task.id);
    
    // Set checkbox
    const checkbox = taskElement.querySelector('.task-checkbox');
    checkbox.checked = task.done;
    checkbox.addEventListener('change', () => handleToggleTask(task.id));
    
    // Set task title
    const titleElement = taskElement.querySelector('.task-title');
    titleElement.textContent = task.title;
    if (task.done) {
        titleElement.classList.add('completed');
    }
    
    // Set task date
    const dateElement = taskElement.querySelector('.task-date');
    if (task.due_date) {
        const date = new Date(task.due_date);
        dateElement.textContent = `Due: ${date.toLocaleDateString()}`;
        
        // Highlight overdue tasks
        if (date < new Date() && !task.done) {
            taskItem.classList.add('overdue');
        }
    } else {
        dateElement.textContent = 'No due date';
    }
    
    // Set delete button
    const deleteBtn = taskElement.querySelector('.delete-btn');
    deleteBtn.addEventListener('click', () => handleDeleteTask(task.id));
    
    container.appendChild(taskElement);
}

// Handle task toggle (complete/incomplete)
async function handleToggleTask(taskId) {
    try {
        await eel.py_toggle_task(taskId)();
        loadTasks(); // Refresh the list
        showMessage('Task updated!', 'success');
    } catch (error) {
        console.error('Error toggling task:', error);
        showMessage('Failed to update task', 'error');
        loadTasks(); // Reload to revert UI changes
    }
}

// Handle task deletion
async function handleDeleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    
    try {
        const success = await eel.py_delete_task(taskId)();
        
        if (success) {
            showMessage('Task deleted!', 'success');
            loadTasks(); // Refresh the list
        } else {
            showMessage('Failed to delete task', 'error');
        }
    } catch (error) {
        console.error('Error deleting task:', error);
        showMessage('Failed to delete task', 'error');
    }
}

// Handle send reminder
async function handleSendReminder() {
    const emailInput = document.getElementById('emailInput');
    const statusDiv = document.getElementById('emailStatus');
    const sendBtn = document.getElementById('sendReminder');
    
    const email = emailInput.value.trim();
    
    if (!email) {
        showEmailStatus('Please enter an email address', 'error');
        return;
    }
    
    if (!isValidEmail(email)) {
        showEmailStatus('Please enter a valid email address', 'error');
        return;
    }
    
    // Show loading state
    sendBtn.disabled = true;
    sendBtn.textContent = '📧 Sending...';
    showEmailStatus('Sending reminder...', 'info');
    
    try {
        // Call Python function to send reminder
        const result = await eel.py_send_reminder(email)();
        
        if (result.success) {
            showEmailStatus(result.message, 'success');
        } else {
            showEmailStatus(result.message, 'error');
        }
    } catch (error) {
        console.error('Error sending reminder:', error);
        showEmailStatus('Failed to send reminder', 'error');
    } finally {
        // Reset button
        sendBtn.disabled = false;
        sendBtn.textContent = '📧 Send Daily Reminder';
    }
}

// Show general messages
function showMessage(message, type = 'info') {
    // Create message element
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${type}`;
    messageEl.textContent = message;
    
    // Add to page
    document.body.appendChild(messageEl);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        messageEl.remove();
    }, 3000);
}

// Show email status messages
function showEmailStatus(message, type = 'info') {
    const statusDiv = document.getElementById('emailStatus');
    statusDiv.textContent = message;
    statusDiv.className = `status-message status-${type}`;
    
    // Clear after 5 seconds for success/info messages
    if (type === 'success' || type === 'info') {
        setTimeout(() => {
            statusDiv.textContent = '';
            statusDiv.className = 'status-message';
        }, 5000);
    }
}

// Validate email format
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Auto-refresh tasks every 30 seconds
setInterval(loadTasks, 30000);

// Expose functions for Python to call (if needed)
eel.expose(function js_show_message(message, type) {
    showMessage(message, type);
});

console.log('Task Reminder App JavaScript loaded!');