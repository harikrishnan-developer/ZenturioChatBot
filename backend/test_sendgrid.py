import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

# Load environment variables
load_dotenv()  # Use the main .env file

def test_sendgrid_email():
    # Get API key from environment
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    if not sendgrid_api_key:
        print("Error: SENDGRID_API_KEY environment variable is not set")
        return False
    
    # Get sender email from environment
    sender_email = os.getenv("SENDER_EMAIL")
    if not sender_email:
        print("Error: SENDER_EMAIL environment variable is not set")
        return False
    
    # Test recipient email (replace with your email for testing)
    recipient_email = "haribro00123@gmail.com"  # Using the same email for testing
    
    # Create test email
    subject = "SendGrid Test Email"
    body = "This is a test email sent using SendGrid API. If you received this, the integration is working correctly!"
    
    try:
        # Create SendGrid message
        from_email = Email(sender_email)
        to_email = To(recipient_email)
        content = Content("text/plain", body)
        mail = Mail(from_email, to_email, subject, content)
        
        # Send email via SendGrid
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(mail)
        
        print(f"Email sent successfully with status code: {response.status_code}")
        print(f"Response body: {response.body}")
        print(f"Response headers: {response.headers}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    print("Testing SendGrid email integration...")
    success = test_sendgrid_email()
    if success:
        print("✅ SendGrid integration test passed!")
    else:
        print("❌ SendGrid integration test failed. Check the error messages above.")