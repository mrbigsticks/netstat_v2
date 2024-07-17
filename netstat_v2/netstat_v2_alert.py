import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send email
def send_email(subject, body):
    sender_email = "shafaamryedu@gmail.com"  # Replace with your email address
    receiver_email = "moshafaamry@gmail.com"  # Replace with recipient's email address
    password = "your_password"  # Replace with your email password

    smtp_server = "smtp.example.com"  # Replace with your SMTP server address
    smtp_port = 465  # Adjust the port number as needed

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def scan_open_ports():
    try:
        # Execute netstat command to get list of listening ports
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, timeout=10)
        
        # Check if the command ran successfully
        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            open_ports = []
            
            # Parse netstat output to find open ports
            for line in output_lines:
                if 'LISTEN' in line:  # Look for lines indicating a listening port
                    parts = line.split()
                    if len(parts) >= 4:  # Ensure there are enough parts to unpack
                        local_address = parts[3]
                        port = local_address.split(':')[-1]
                        protocol = parts[0]
                        open_ports.append((port, protocol))
            
            # Print open ports and raise alert if any are found
            if open_ports:
                alert_subject = "Open Ports Detected"
                alert_body = "The following open ports were found:\n\n"
                for port, protocol in open_ports:
                    alert_body += f"    Port: {port}, Protocol: {protocol}\n"
                
                print(alert_body)
                
                # Send email alert
                send_email(alert_subject, alert_body)
                
                # Print number of open ports found
                print(f"Total open ports found: {len(open_ports)}")
                
            else:
                print("No open ports found")
    
        else:
            print("Failed to execute netstat command")
    
    except subprocess.TimeoutExpired:
        print("Timeout occurred while executing netstat command")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    scan_open_ports()
