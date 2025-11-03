import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_reminder(email, tasks_today):
    """
    Send email reminder with today's tasks
    Can work with real SMTP (Gmail) or simulate sending
    """
    
    # Email configuration from environment
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')
    
    # If no credentials provided, simulate email sending
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return simulate_email_sending(email, tasks_today)
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg['Subject'] = f"Daily Task Reminder - {date.today().strftime('%B %d, %Y')}"
        
        # Create email body
        body = create_email_body(tasks_today)
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {email}")
        return {"success": True, "message": f"Reminder sent to {email}"}
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return {"success": False, "message": f"Failed to send email: {str(e)}"}

def simulate_email_sending(email, tasks_today):
    """
    Simulate email sending for demo purposes
    """
    print("📧 SIMULATING EMAIL SENDING (No SMTP credentials provided)")
    print("="*60)
    print(f"To: {email}")
    print(f"Subject: Daily Task Reminder - {date.today().strftime('%B %d, %Y')}")
    print("="*60)
    
    if not tasks_today:
        print("🎉 Great! You have no tasks due today!")
    else:
        print(f"📋 You have {len(tasks_today)} task(s) due today:")
        for i, task in enumerate(tasks_today, 1):
            print(f"  {i}. {task['title']}")
    
    print("="*60)
    print("✅ Email simulation completed!")
    
    return {
        "success": True, 
        "message": f"Email simulated successfully to {email} ({len(tasks_today)} tasks)"
    }

def create_email_body(tasks_today):
    """
    Create HTML email body with tasks
    """
    today_str = date.today().strftime('%B %d, %Y')
    
    if not tasks_today:
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2e7d32;">Daily Task Reminder</h2>
            <p style="color: #666;">Date: {today_str}</p>
            
            <div style="background-color: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2e7d32; margin-top: 0;">🎉 Great news!</h3>
                <p style="margin-bottom: 0;">You have no tasks due today. Enjoy your free time!</p>
            </div>
            
            <p style="color: #999; font-size: 12px;">
                Sent from Task Reminder App
            </p>
        </body>
        </html>
        """
    
    tasks_html = ""
    for i, task in enumerate(tasks_today, 1):
        tasks_html += f"""
        <li style="padding: 8px 0; border-bottom: 1px solid #eee;">
            <strong>{task['title']}</strong>
        </li>
        """
    
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #1976d2;">Daily Task Reminder</h2>
        <p style="color: #666;">Date: {today_str}</p>
        
        <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #1976d2; margin-top: 0;">📋 Tasks Due Today ({len(tasks_today)})</h3>
            <ul style="list-style: none; padding: 0; margin: 0;">
                {tasks_html}
            </ul>
        </div>
        
        <p style="color: #666;">
            Don't forget to complete your tasks! 💪
        </p>
        
        <p style="color: #999; font-size: 12px;">
            Sent from Task Reminder App
        </p>
    </body>
    </html>
    """

def test_email_function():
    """
    Test function for email sending
    """
    test_tasks = [
        {"title": "Complete project documentation", "due_date": "2025-11-03"},
        {"title": "Review code with team", "due_date": "2025-11-03"}
    ]
    
    result = send_reminder("test@example.com", test_tasks)
    print(f"Test result: {result}")

if __name__ == "__main__":
    test_email_function()