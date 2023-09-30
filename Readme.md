Overview:

Windows Service for Monitoring and Managing Services

Overview:

This Python script defines a Windows service named "MyService" that monitors and manages other Windows services based on a configuration file. It periodically checks the status of specified services, restarts them if necessary, and sends email notifications about service status changes.

Features:

Monitors and manages Windows services.

Supports configuration through a JSON file.

Sends email notifications using Gmail.

Handles service dependencies.

Provides logging for monitoring and error tracking.

Getting Started:

Follow these steps to set up and use the Windows service:

Prerequisites:

Python: Ensure you have Python installed on your system.

Python Packages: Install required packages using pip install psutil pywin32.

Customization:

You can customize the service name and display name by changing _svc_name_ and _svc_display_name_ in the script.

Troubleshooting:

Check the service_log.txt file for logs and error messages.
Ensure that the required dependencies are installed and configured correctly.

My Service Watchdog is a Windows service that monitors other Windows services and sends email notifications when issues are detected. It helps ensure the reliability and availability of critical services.

Python code for the "My Service Watchdog" Windows service defines a Windows service that monitors other Windows services, sends email notifications when issues are detected, and logs its activity.

Here's a breakdown of the key components and functionalities in the code:

Service Definition:

The service is defined as a class named MyService, which inherits from win32serviceutil.ServiceFramework.
_svc_name_ and _svc_display_name_ specify the service name and display name, respectively.

Logging Configuration: 

It configures logging to write log messages to a file named "service_log.txt" with a specified format.

Initialization:

The __init__ method sets up the service and creates an event for stopping the service.
Service Control:

SvcStop and SvcDoRun methods are part of the Windows service control flow. SvcStop handles service stop requests, and SvcDoRun is the main entry point when the service starts.
Reading Configuration:

The read_config method reads the configuration from a config.json file. It returns the list of services to monitor and the monitoring interval in seconds.
Sending Email Notifications:

The send_notification method sends email notifications using the provided SMTP server (Gmail in this case). It logs success or failure.
Monitoring Services with Dependencies:

The check_service_with_dependencies method checks a service and its dependencies. If a dependency is not running, it sends an email notification.
It also monitors the main service's status, potentially restarting it if necessary.
Main Loop:

The main method is the service's main loop. It continuously reads the configuration, checks services, and sleeps for the specified monitoring interval.
Service Initialization:

In the __main__ block, the service is initialized and started using the win32serviceutil and servicemanager modules.

Logging is configured to write to a log file (service_log.txt).

Specific exceptions are caught and logged with meaningful error messages.

Error handling is enhanced to provide better diagnostic information.

The SvcDoRun method is wrapped in a try-except block to handle any unexpected errors that may occur during service execution.

Table of Contents:

Installation

Usage

Configuration

Installation:

To install My Service Watchdog, follow these steps:

Download the latest release.

Extract the contents to a directory of your choice.

Open a command prompt as administrator.

Navigate to the directory where you extracted the files.

Run the following command to install the service:

sc create MyService binPath= "C:\path\to\MyService.exe"

Start the service:

sc start MyService

Usage:

Once the service is installed and running, it will monitor the services specified in the config.json file. You can view the service logs in the Windows Event Viewer under "Windows Logs" > "Application." Look for entries related to "My Windows Service."

Configuration

The configuration for My Service Watchdog is stored in the config.json file. You can customize the configuration as follows:

services: List of services to monitor, along with their dependencies.
monitoring_interval_seconds: The interval at which the service checks the status of monitored services.

{
   "services": [
      {
         "name": "ServiceName1",
         "dependencies": ["DependencyService1", "DependencyService2"]
      },
      {
         "name": "ServiceName2"
      }
   ],
   "monitoring_interval_seconds": 60
}

This configuration states that your "MyService" Windows service should monitor two services: 
"ServiceName1" and "ServiceName2." 

"ServiceName1" has two dependencies, "DependencyService1" and "DependencyService2," which will be checked before monitoring "ServiceName1" itself. 

The monitoring interval is set to 60 seconds.

Assuming this configuration accurately reflects your monitoring requirements, it should be fine. 

However, make sure that the service names and dependencies listed in the configuration match the actual service names on your system.

If these service names and dependencies are correct, you can proceed to use this configuration with your "MyService" Windows service for monitoring and managing services as intended.

Additionally, configure the email settings in the MyService class in the code to enable email notifications.

To implement this service code follow these steps:

Install Required Dependencies:

Ensure you have the necessary dependencies installed. You will need Python, pywin32, and the psutil library. You can install them using pip:

pip install pywin32 psutil

Configure Email Credentials:

In MyService class, there are references to email_sender, email_password, and email_receiver. 
You'll need to replace these with your actual email credentials and recipient email address for sending notifications.

Install the Service:

Install pyinstaller Globally: If you plan to use pyinstaller for other projects in the future, you can install it globally using pip. Open a command prompt or terminal and run:

pip install pyinstaller

Once installed globally, you should be able to run pyinstaller from any directory.

Use pyinstaller from a Virtual Environment: If you prefer to keep dependencies isolated for your project, you can create a virtual environment, activate it, and then install pyinstaller within that environment. Here's how:

# Create a virtual environment (if you haven't already)
python -m venv venv_name

# Activate the virtual environment
# On Windows:
venv_name\Scripts\activate
# On macOS and Linux:
source venv_name/bin/activate

# Install pyinstaller within the virtual environment
pip install pyinstaller

With the virtual environment activated, you can run the pyinstaller command without any issues.

Open a command prompt as administrator and navigate to the directory containing your Python script. Then, install the service using the pywin32 pyinstaller command. Replace <PathToYourScript> with the actual path to your script:

pyinstaller --name MyService --hidden-import=win32timezone <PathToYourScript>

Specifically:

pyinstaller --name MyService --hidden-import=win32timezone C:<Insert the exact path to the location of the project folder here>\Watchdog_service\app.py

This command will create a dist folder with an executable file named MyService.exe.

Once you've successfully run the pyinstaller command, you can proceed with the remaining steps to install and manage your Windows service.

Install the Service:

Install the service using the following command (you need to specify the full path to the MyService.exe file):

sc create MyService binPath= "<FullPathToMyService.exe>"

Specifically:

C:<Insert the exact path to the location of the project folder here>\Watchdog_service\dist\MyService.exe

Start the Service:

Start the service you just created:

sc start MyService

View Service Logs:

The service logs are created using the logging module. You can view the logs in the Windows Event Viewer under "Windows Logs" > "Application." Look for entries related to "My Windows Service."

Manage the Service:

You can manage the service like any other Windows service. To stop or restart it, you can use the sc command:

sc stop MyService

To uninstall the service:

sc delete MyService

That's it! Your service is now running and will monitor the specified services based on the configuration in config.json. It will send email notifications when issues are detected. Make sure to monitor the logs for any errors or issues related to the service.

Use the pip command to install the requirements specified in a requirements.txt file. Here's the basic command to do that:

pip install -r requirements.txt

Make sure you navigate to the directory where the requirements.txt file is located before running this command, or provide the full path to the requirements.txt file if it's in a different directory. This command will install all the packages listed in the requirements.txt file, ensuring that your project has the necessary dependencies.

requirements.txt:

altgraph==0.17.4
aniso8601==9.0.1
blinker==1.6.2
click==8.1.7
colorama==0.4.6
distlib==0.3.7
filelock==3.12.2
Flask==2.3.3
Flask-RESTful==0.3.10
Flask-WTF==1.1.1
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
packaging==23.1
pefile==2023.2.7
platformdirs==3.10.0
psutil==5.9.5
pygame==2.5.1
pyinstaller==6.0.0
pyinstaller-hooks-contrib==2023.9
pytz==2023.3.post1
pywin32==306
pywin32-ctypes==0.2.2
secure-smtplib==0.1.1
six==1.16.0
virtualenv==20.24.3
Werkzeug==2.3.7
WTForms==3.0.1





