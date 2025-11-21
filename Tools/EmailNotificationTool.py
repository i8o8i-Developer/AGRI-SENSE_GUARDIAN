# AgriSenseGuardian Email Notification Tool - SMTP-Based Email Delivery For Agricultural Communications
# Supports Gmail, Outlook, SendGrid, And Custom SMTP Servers For Global Farmer Notifications
# Provides HTML-Formatted Emails With Professional Branding And Delivery Tracking

import os
from Config.Settings import get_settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any, Dict
from google.adk.tools.tool_context import ToolContext

settings = get_settings()

async def EmailNotificationTool(
    RecipientEmail: str,
    Subject: str,
    MessageContent: str,
    ToolContextInstance: ToolContext
) -> Dict[str, Any]:
    """
    Send HTML-Formatted Email Notification To Farmer With Agricultural Action Plan.
    
    Delivers Professional Email Communications Containing Risk Assessments, Action Plans,
    And Farming Recommendations Using Configured SMTP Providers. Supports Multiple
    Free And Commercial SMTP Services With Automatic HTML Formatting And Delivery Tracking.
    
    The Tool Creates Multipart Emails With Both Plain Text And HTML Versions, Includes
    Professional Branding, And Tracks Delivery Status For Observability. Used As the
    Primary Communication Channel For Farmer Notifications.
    
    Args:
        RecipientEmail: Recipient's Email Address (e.g., "farmer@example.com").
                       Must Be Valid Email Format For Successful Delivery.
        Subject: Email Subject Line String. Should Be Descriptive But Concise.
        MessageContent: The Main Message Content (Action Plan, Recommendations, Etc.).
                       Will Be Formatted With HTML Styling And AgriSenseGuardian Branding.
        ToolContextInstance: ADK Tool Context For Session State Management And
                           Delivery Tracking Integration.
        
    Returns:
        Dict: Structured Email Delivery Response With The Following Keys:
            - Status: Delivery Status ('Success' Or 'Error')
            - MessageId: Unique Message Identifier For Tracking
            - Recipient: Email Address Used For Delivery
            - Subject: Email Subject Line Used
            - MessageLength: Character Count Of Original Message Content
            - DeliveryStatus: Current Delivery Status ('Sent' On Success)
            - DeliveryTimestamp: ISO Format Timestamp Of Send Attempt
            - Provider: SMTP Provider Used (Capitalized)
            - Cost: Delivery Cost (0.00 For Free Tiers)
            - Currency: Cost Currency ('USD')
            - DataSource: 'SMTP' Identifier
            
        On Error Returns:
            - Status: 'Error'
            - Message: Error Description String
            - Recipient: Email Address That Failed Delivery
    """
    
    # Real SMTP Email Sending Only
    MessageLength = len(MessageContent)
    
    try:
        import uuid
        from datetime import datetime
        
        MessageId = f'EMAIL-{uuid.uuid4().hex[:8].upper()}'
        
        # Get SMTP Configuration From Application Settings (Fallback to Env)
        settings = get_settings()
        SmtpProvider = settings.smtp_provider or os.getenv('SMTP_PROVIDER', 'gmail') 
        SmtpHost = settings.smtp_host or os.getenv('SMTP_HOST', 'smtp.gmail.com')
        SmtpPort = int(settings.smtp_port or os.getenv('SMTP_PORT', '587'))
        SmtpUser = settings.smtp_user or os.getenv('SMTP_USER', '')
        SmtpPassword = settings.smtp_password or os.getenv('SMTP_PASSWORD', '')
        SenderEmail = settings.sender_email or os.getenv('SENDER_EMAIL', SmtpUser)
        SenderName = settings.sender_name or os.getenv('SENDER_NAME', 'AgriSenseGuardian')
        
        # Validate Configuration
        if not SmtpUser or not SmtpPassword:
            return {
                'Status': 'Error',
                'Message': 'SMTP credentials Not Configured. Set SMTP_USER and SMTP_PASSWORD Environment Variables.',
                'Recipient': RecipientEmail
            }
        
        # Create Email Message
        Message = MIMEMultipart('alternative')
        Message['From'] = f'{SenderName} <{SenderEmail}>'
        Message['To'] = RecipientEmail
        Message['Subject'] = Subject
        Message['Message-ID'] = f'<{MessageId}@agrisenseguardian.com>'
        
        # Plain Text Version
        TextPart = MIMEText(MessageContent, 'plain', 'utf-8')
        
        # HTML Version (Enhanced Formatting)
        HtmlContent = f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); padding: 20px; color: white;">
                    <h1 style="margin: 0;">🌾 AgriSenseGuardian</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Agricultural Decision Support System</p>
                </div>
                <div style="padding: 20px; background: #f5f5f5;">
                    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <pre style="white-space: pre-wrap; font-family: 'Courier New', monospace; line-height: 1.6;">{MessageContent}</pre>
                    </div>
                    <p style="text-align: center; color: #666; font-size: 12px; margin-top: 20px;">
                        Powered By Google ADK & A2A Protocol | Message ID: {MessageId}
                        Build With 💚 For Farmers Worldwide | From : Anubhav Chaurasia
                    </p>
                </div>
            </body>
        </html>
        """
        HtmlPart = MIMEText(HtmlContent, 'html', 'utf-8')
        
        Message.attach(TextPart)
        Message.attach(HtmlPart)
        
        # Send Email Via SMTP
        with smtplib.SMTP(SmtpHost, SmtpPort, timeout=10) as Server:
            Server.starttls()
            Server.login(SmtpUser, SmtpPassword)
            Server.send_message(Message)
        
        # Log To Tool Context State For Observability (If Available)
        if ToolContextInstance is not None:
            if 'SentEmails' not in ToolContextInstance.state:
                ToolContextInstance.state['SentEmails'] = []
            
            ToolContextInstance.state['SentEmails'].append({
                'MessageId': MessageId,
                'Recipient': RecipientEmail,
                'Timestamp': datetime.utcnow().isoformat() + 'Z'
            })
        
        return {
            'Status': 'Success',
            'MessageId': MessageId,
            'Recipient': RecipientEmail,
            'Subject': Subject,
            'MessageLength': MessageLength,
            'DeliveryStatus': 'Sent',
            'DeliveryTimestamp': datetime.utcnow().isoformat() + 'Z',
            'Provider': SmtpProvider.title(),
            'Cost': 0.00,  # Free Tier
            'Currency': 'USD',
            'DataSource': 'SMTP'
        }
        
    except smtplib.SMTPAuthenticationError:
        return {
            'Status': 'Error',
            'Message': 'SMTP Authentication Failed. Check SMTP_USER And SMTP_PASSWORD.',
            'Recipient': RecipientEmail
        }
    except smtplib.SMTPException as SmtpError:
        return {
            'Status': 'Error',
            'Message': f'SMTP Error: {str(SmtpError)}',
            'Recipient': RecipientEmail
        }
    except Exception as Error:
        return {
            'Status': 'Error',
            'Message': f'Failed To Send Email: {str(Error)}',
            'Recipient': RecipientEmail
        }