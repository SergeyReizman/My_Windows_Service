import json
import smtplib
import time
import psutil
import win32serviceutil
import win32service
import win32event
import servicemanager
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Configure logging to write to a log file
logging.basicConfig(filename='service_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Windows Service Definition
class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MyService'
    _svc_display_name_ = 'My Windows Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    # Method to handle service stop
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    # Method to run the service
    def SvcDoRun(self):
        try:
            servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_,))
            self.main()
        except Exception as e:
            logging.error(f"An error occurred in SvcDoRun: {str(e)}")

    # Method to read configuration from 'config.json' file
    def read_config(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                services_config = config.get('services', [])
                monitoring_interval = config.get('monitoring_interval_seconds', 60)
            return services_config, monitoring_interval
        except FileNotFoundError as file_error:
            logging.error(f"Error reading configuration: {str(file_error)}")
            return [], 60
        except Exception as e:
            logging.error(f"Unexpected error reading configuration: {str(e)}")
            return [], 60

    # Method to send email notifications
    def send_notification(self, subject, message, email_sender, email_password, email_receiver):
        try:
            msg = MIMEMultipart()
            msg['From'] = email_sender
            msg['To'] = email_receiver
            msg['Subject'] = subject
            text = MIMEText(message)
            msg.attach(text)
            
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(email_sender, email_password)
                smtp_server.sendmail(email_sender, email_receiver, msg.as_string())
            
            logging.info("Email sent successfully")
        except smtplib.SMTPException as smtp_error:
            logging.error(f"SMTP error: {str(smtp_error)}")
        except Exception as e:
            logging.error(f"Failed to send email notification: {str(e)}")

    # Method to check services with dependencies
    def check_service_with_dependencies(self, service_config, email_sender, email_password, email_receiver):
        service_name = service_config["name"]
        dependencies = service_config.get("dependencies", [])
        
        try:
            for dependency_name in dependencies:
                dependency_service = psutil.win_service_get(dependency_name)
                if dependency_service.status() != "running":
                    logging.warning(f"Dependency {dependency_name} of {service_name} is not running.")
                    self.send_notification(
                        f"Service Alert: Dependency {dependency_name} of {service_name} is not running",
                        f"The {dependency_name} service is not running, required by {service_name}.",
                        email_sender, email_password, email_receiver
                    )
                    return
            
            # Monitor and potentially restart the service
            service = psutil.win_service_get(service_name)
            previous_state = service.status()
            
            if previous_state == "running":
                logging.info(f"{service_name} is running.")
            else:
                logging.warning(f"{service_name} is not running. Attempting to restart...")
                try:
                    service.restart()
                    logging.info(f"Restarted {service_name} successfully.")
                except Exception as restart_error:
                    logging.error(f"Failed to restart {service_name}: {str(restart_error)}")
                    self.send_notification(
                        f"Service Alert: {service_name} restart failed",
                        f"Failed to restart {service_name}: {str(restart_error)}",
                        email_sender, email_password, email_receiver
                    )
            
            current_state = service.status()
            if previous_state != current_state:
                logging.info(f"{service_name} state changed from {previous_state} to {current_state}")
        
        except psutil.NoSuchProcess as no_process_error:
            logging.error(f"No such process: {str(no_process_error)}")
        except Exception as e:
            logging.error(f"Error checking {service_name}: {str(e)}")

    # Main method to run the service
    def main(self):
        while True:
            services_config, monitoring_interval = self.read_config()
            
            for service_config in services_config:
                self.check_service_with_dependencies(service_config, email_sender, email_password, email_receiver)
            
            time.sleep(monitoring_interval)

if __name__ == '__main__':
    # Initialize the service
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(MyService)
    servicemanager.StartServiceCtrlDispatcher()
