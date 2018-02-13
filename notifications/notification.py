# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
with open('textfile', 'rb') as fp:
    # Create a text/plain message
    msg = MIMEText(fp.read())

me='manojrana.k1@gmail.com'
#you == the recipient's email address
msg['Subject'] = 'The contents of textfile'
msg['From'] = "Mothership@Codeathon.com" 
msg['To'] = me 

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail(me, [me,me], msg.as_string())
s.quit()
