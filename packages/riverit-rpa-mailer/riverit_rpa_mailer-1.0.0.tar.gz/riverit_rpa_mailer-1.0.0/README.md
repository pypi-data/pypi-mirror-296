# robot_notification_mailer

Email notification library for Robocorp robots to use for reporting their process.  
Mailer will send an email to the selected address, with the option of having a list of links to the handled files.

# Setup

To get the **Robot notification mailer** up and running, provide with the following configuration details:

### Robot_Mailer

#### Your Microsoft graph details:

Provide the Robot_mailer with a `dictionary` of account details.

- CLIENT_ID = ["clientid"] :Your Microsoft Graph Client ID
- TENANT_ID = ["tenantid"] :Your Microsoft Graph Tenant ID
- USERNAME = ["username"] :Email address of the sending account
- PASSWORD = ["password"] :Password for the sending account

#### Email sender (optional)

Provide the address to act as the `from:` in the emails.  
You need to have permissions to `send as` or `send on behalf` of that mailbox.  
If not provided, email will be sent from the username address.

### Send_report_mail()

### Recipients

A `list` of adresses to send the report to

### process name

A `string` name for the process being reported on

### status

The status of the process run.  
`0 = failure`  
`1 = attention`  
`2 = success`

### files handled

(Optional) a `list` of files handled by the process run. Items on the list will be emailed as html link elements.

python >= 3.10
msal >= 1.31.0

# Example Usage

```
from robot_notification_mailer import Robot_Mailer

mailer_secrets = {
    'CLIENT_ID': 'your_client_id',
    'TENANT_ID': 'your_tenant_id',
    'USERNAME': 'your_email@example.com',
    'PASSWORD': 'your_password'
}
sender_address = 'another_email@example.com'

# Initialize the mailer
mailer = Robot_Mailer(mailer_config, sender_Address)

# Define recipients and report details
recipients = ['recipient1@example.com', 'recipient2@example.com']
process_name = 'Data Processing'
status = 2  # Success
handled_files = ['file1.csv', 'file2.csv']

# Send the email report
mailer.Send_report_mail(recipients, process_name, status, handled_files)
```
