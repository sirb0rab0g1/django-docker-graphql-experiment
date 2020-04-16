#https://myaccount.google.com/lesssecureapps
#https://pypi.org/project/email-to/

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def sendemail(to_email, link):

    # rec_list =  [to_email, 'princessmaygarde@gmail.com', 'kentoyfueconcillo@gmail.com', 'nitishkh01@gmail.com', 'alanbenedictgolpeo@gmail.com', 'jeffxion03@gmail.com', 'mcmeliton1889@gmail.com']
    # rec =  ', '.join(rec_list)
    rec = to_email

    message = MIMEMultipart('alternative')
    message['Subject'] = 'Reset Password'
    message['From'] = 'kentoyfueconcillo@gmail.com'
    message['To'] = rec

    html = """\
    <html>
    <head></head>
    <body>
    <div style='background: #f3ac2c; height: 30px;'></div>
    <center><img src="https://i.imgur.com/ZgkaQXw.png?1" height="500" width="900"><br />
    </center>
    <h2>Reset Password</h2>
    A password change for the account with the e-mail address has been requested. If you are trying to reset your password, please visit the URL below <br />""" + link + """\ <br />

    Kind Regards,<br />
 
    Kent Fueconcillo<br />
    Pasmong Dev<br />
    M: +63 910 777 1037<br />
    W: www.infosoftstudio.com<br />

    <div style='background: #f3ac2c; height: 30px;'></div>
    </body>
    </html>
    """

    message.attach(MIMEText(html, 'html'))

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # two way authentication solves the gmail issue in ssh
    # https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637080027265884993-1110728592&rd=1
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('aeontowertest@gmail.com', 'eicrqxdkmpndicus') # original password is Pasmo.123
    # server.sendmail('kentoyfueconcillo@gmail.com', rec_list, message.as_string()) # multiple sending
    server.sendmail('aeontowertest@gmail.com', rec, message.as_string()) # single sending
    server.quit()

