import eel
import sys
import os
from database import add_task, get_tasks, toggle_done, delete_task, get_today_tasks
from email_sender import send_reminder

# Caminho absoluto para a pasta web
WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')
eel.init(WEB_DIR)

print("🚀 Starting Task Reminder App...")
print("📋 Desktop application built with Python + Eel")
print("="*50)

# Expose Python functions to JavaScript
@eel.expose
def py_add_task(title, due_date=None):
    """
    Add a new task
    Called from JavaScript: eel.py_add_task(title, due_date)()
    """
    try:
        print(f"➕ Adding task: {title} (Due: {due_date or 'No date'})")
        result = add_task(title, due_date)
        if result:
            print(f"✅ Task added successfully with ID: {result['id']}")
            return result
        else:
            print("❌ Failed to add task")
            return None
    except Exception as e:
        print(f"❌ Error adding task: {e}")
        return None

@eel.expose
def py_get_tasks():
    """
    Get all tasks
    Called from JavaScript: eel.py_get_tasks()()
    """
    try:
        tasks = get_tasks()
        print(f"📋 Retrieved {len(tasks)} tasks")
        return tasks
    except Exception as e:
        print(f"❌ Error getting tasks: {e}")
        return []

@eel.expose
def py_toggle_task(task_id):
    """
    Toggle task completion status
    Called from JavaScript: eel.py_toggle_task(task_id)()
    """
    try:
        print(f"🔄 Toggling task {task_id}")
        success = toggle_done(task_id)
        if success:
            print(f"✅ Task {task_id} toggled successfully")
        else:
            print(f"❌ Failed to toggle task {task_id}")
        return success
    except Exception as e:
        print(f"❌ Error toggling task: {e}")
        return False

@eel.expose
def py_delete_task(task_id):
    """
    Delete a task
    Called from JavaScript: eel.py_delete_task(task_id)()
    """
    try:
        print(f"🗑️ Deleting task {task_id}")
        success = delete_task(task_id)
        if success:
            print(f"✅ Task {task_id} deleted successfully")
        else:
            print(f"❌ Failed to delete task {task_id}")
        return success
    except Exception as e:
        print(f"❌ Error deleting task: {e}")
        return False

@eel.expose
def py_send_reminder(email):
    """
    Send daily reminder email
    Called from JavaScript: eel.py_send_reminder(email)()
    """
    try:
        print(f"📧 Sending reminder to: {email}")
        
        # Get today's tasks
        today_tasks = get_today_tasks()
        print(f"📋 Found {len(today_tasks)} tasks due today")
        
        # Send the reminder
        result = send_reminder(email, today_tasks)
        
        if result['success']:
            print(f"✅ Reminder sent successfully to {email}")
        else:
            print(f"❌ Failed to send reminder: {result['message']}")
            
        return result
        
    except Exception as e:
        print(f"❌ Error sending reminder: {e}")
        return {"success": False, "message": f"Error: {str(e)}"}

@eel.expose
def py_get_app_info():
    """
    Get application information
    Called from JavaScript: eel.py_get_app_info()()
    """
    return {
        "name": "Task Reminder App",
        "version": "1.0.0",
        "description": "Desktop task management with email reminders",
        "tech_stack": ["Python", "Eel", "SQLite", "HTML/CSS/JS"]
    }

# Optional: Expose a function to gracefully close the app
@eel.expose
def py_close_app():
    """
    Close the application
    Called from JavaScript: eel.py_close_app()()
    """
    print("👋 Closing Task Reminder App...")
    sys.exit()

# JavaScript functions that can be called from Python (if needed)
# These are exposed in the JavaScript side using eel.expose()

def show_js_message(message, message_type="info"):
    """
    Show a message in the JavaScript UI
    """
    try:
        eel.js_show_message(message, message_type)
    except:
        pass  # Fail silently if JS function doesn't exist

# App startup function
def start_app():
    """
    Start the Eel application
    """
    try:
        print("🌐 Initializing web interface...")
        print("📱 Opening application window...")
        
        # Start the app with custom window size and options
        eel.start(
            'index.html',  # Main HTML file
            size=(900, 700),  # Window size (width, height)
            position=(100, 50),  # Window position (x, y)
            disable_cache=True,  # Disable cache for development
            mode='chrome',  # Use Chrome browser engine
            host='localhost',  # Host
            port=0,  # Auto-select port
            close_callback=on_close,  # Callback when window is closed
            cmdline_args=[
                '--disable-web-security',
                '--disable-features=TranslateUI'
            ]
        )
        
    except EnvironmentError:
        # If Chrome is not available, try with default browser
        print("⚠️ Chrome not found, trying with default browser...")
        try:
            eel.start(
                'index.html',
                size=(900, 700),
                mode='default',
                host='localhost',
                port=0,
                close_callback=on_close
            )
        except Exception as e:
            print(f"❌ Failed to start application: {e}")
            print("💡 Make sure you have Chrome or another modern browser installed")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

def on_close(page, sockets):
    """
    Callback function when the window is closed
    """
    print("👋 Window closed, shutting down...")
    sys.exit()

# Development helper functions
def setup_development_environment():
    """
    Setup development environment
    """
    # Add some sample tasks for development
    sample_tasks = [
        ("Complete project documentation", "2025-11-03"),
        ("Review code with team", "2025-11-04"),
        ("Deploy to production", "2025-11-05")
    ]
    
    existing_tasks = get_tasks()
    if len(existing_tasks) == 0:
        print("🛠️ Setting up development data...")
        for title, due_date in sample_tasks:
            add_task(title, due_date)
        print(f"✅ Added {len(sample_tasks)} sample tasks")

# Main execution
if __name__ == "__main__":
    print("Task Reminder App - Starting...")
    
    # Check if running in development mode
    if "--dev" in sys.argv:
        print("🛠️ Running in development mode")
        setup_development_environment()
    
    # Start the application
    start_app()