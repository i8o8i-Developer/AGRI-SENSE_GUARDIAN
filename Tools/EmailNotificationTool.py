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
        
        # HTML Version (Enhanced Formatting With Modern Design)
        HtmlContent = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta name="color-scheme" content="light">
            <meta name="supported-color-schemes" content="light">
            <title>{Subject}</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f0f4f8; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f0f4f8; padding: 20px 0;">
                <tr>
                    <td align="center">
                        <!-- Main Container -->
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                            
                            <!-- Header Section -->
                            <tr>
                                <td style="background: linear-gradient(135deg, #4CAF50 0%, #388E3C 50%, #2E7D32 100%); padding: 40px 30px; text-align: center;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 32px; font-weight: 700; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                                        🌾 AgriSenseGuardian
                                    </h1>
                                    <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.95); font-size: 15px; font-weight: 400; letter-spacing: 0.3px;">
                                        AI-Powered Agricultural Intelligence Platform
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Subject Banner -->
                            <tr>
                                <td style="background: linear-gradient(90deg, #e8f5e9 0%, #c8e6c9 100%); padding: 15px 30px; border-bottom: 3px solid #4CAF50;">
                                    <p style="margin: 0; color: #2E7D32; font-size: 16px; font-weight: 600; text-align: center;">
                                        📬 {Subject}
                                    </p>
                                </td>
                            </tr>
                            
                            <!-- Message Content -->
                            <tr>
                                <td style="padding: 30px;">
                                    <div style="background: #fafafa; border-left: 4px solid #4CAF50; border-radius: 8px; padding: 25px; margin-bottom: 20px;">
                                        <pre style="white-space: pre-wrap; word-wrap: break-word; font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Courier New', monospace; font-size: 14px; line-height: 1.7; color: #333333; margin: 0; overflow-x: auto;">{MessageContent}</pre>
                                    </div>
                                </td>
                            </tr>
                            
                            <!-- Action Footer -->
                            <tr>
                                <td style="background: linear-gradient(90deg, #f5f5f5 0%, #e8e8e8 100%); padding: 25px 30px; border-top: 1px solid #e0e0e0;">
                                    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                                        <tr>
                                            <td style="text-align: center; padding-bottom: 15px;">
                                                <p style="margin: 0; color: #555555; font-size: 13px; font-weight: 500;">
                                                    🤖 Powered By <strong style="color: #4CAF50;">Google ADK</strong> & <strong style="color: #2196F3;">A2A Protocol</strong>
                                                </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="text-align: center; padding-bottom: 10px;">
                                                <p style="margin: 0; color: #777777; font-size: 12px;">
                                                    Message ID: <code style="background: #e0e0e0; padding: 2px 6px; border-radius: 3px; font-family: monospace; color: #333333;">{MessageId}</code>
                                                </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="text-align: center; border-top: 1px solid #d0d0d0; padding-top: 15px;">
                                                <p style="margin: 0; color: #888888; font-size: 11px; line-height: 1.5;">
                                                    Built With 💚 For Farmers Worldwide<br>
                                                    <strong style="color: #4CAF50;">Anubhav Chaurasia</strong> | Open-Source Agricultural AI
                                                </p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="text-align: center; padding-top: 10px;">
                                                <p style="margin: 0; color: #999999; font-size: 10px;">
                                                    © 2025 AgriSenseGuardian | Apache 2.0 License
                                                </p>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            
                        </table>
                        
                        <!-- Email Client Compatibility Footer -->
                        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="max-width: 600px; margin-top: 15px;">
                            <tr>
                                <td style="text-align: center; padding: 10px;">
                                    <p style="margin: 0; color: #999999; font-size: 11px; line-height: 1.5;">
                                        🌍 Supporting Sustainable Agriculture Through AI Technology<br>
                                        <a href="https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN" style="color: #4CAF50; text-decoration: none; font-weight: 500;">View On GitHub</a> | 
                                        <a href="https://github.com/i8o8i-Developer/AGRI-SENSE_GUARDIAN/tree/main/Docs" style="color: #2196F3; text-decoration: none; font-weight: 500;">Documentation</a>
                                    </p>
                                </td>
                            </tr>
                        </table>
                        
                    </td>
                </tr>
            </table>
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