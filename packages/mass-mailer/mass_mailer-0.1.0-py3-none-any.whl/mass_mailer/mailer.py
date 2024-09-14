import smtplib as s
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


ob = s.SMTP('smtp.gmail.com', 587)
ob.ehlo()
ob.starttls()


ob.login('anuprabhsinghcp@gmail.com', 'epvt minl tbwy newk')


recipients = [
    ('gs22ecb0b22@student.nitw.ac.in', 'Vignesh'),
    ('as22ecb0b06@student.nitw.ac.in', 'Anuprabh')
]

subject = "Freshers Alert!"

for email, name in recipients:

    message = MIMEMultipart()
    message['From'] = 'anuprabhsinghcp@gmail.com'
    message['To'] = email
    message['Subject'] = subject

    
    body = f"Hello {name},\n\n Get ready for freshers!"
    message.attach(MIMEText(body, 'plain'))


    ob.sendmail('anuprabhsinghcp@gmail.com', email, message.as_string())

    print(f"Mail sent to {name}")


ob.quit()
