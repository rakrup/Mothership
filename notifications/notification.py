# Import smtplib for the actual sending function
import smtplib
import datetime
# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
#with open('textfile', 'rb') as fp:
        # Create a text/plain message
def notfications(cv, build):
    now = datetime.datetime.now()
    #print now.strftime("%Y-%m-%d")
    tt=now.strftime("%Y-%m-%d-%T")
    msg1="Vulnerability detected on {0} for AMI:{1}".format(tt, build)
    #print msg1

    msg = MIMEText("This is sample message "+str(cv))

    me='manojrana.k1@gmail.com'
    you=['manojrana.k1@gmail.com','vjagachittes@gmail.com'] 
    #msg['Subject'] = 'Project motherhsip CVE details for'
    msg['Subject'] = msg1
    msg['From'] = "Mothership@Codeathon.com" 
    #msg['To'] = ['manojrana.k1@gmail.com','vjagachittes@gmail.com']  
    msg['To'] = "manojrana.k1@gmail.com" 

            # Send the message via our own SMTP server, but don't include the
            # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail(me, you, msg.as_string())
    s.quit()

notfications(14, "test")
