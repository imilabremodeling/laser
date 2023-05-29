import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def email_func(temp1_msg):
    sd,sip,dd,dip,pt,en,day = temp1_msg.split('_')
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "Lightweight Authentication Alarm Message"  #郵件標題
    content["from"] = "avril0930351909@gmail.com"  #寄件者
    content["to"] = "d89012255@gmail.com" #收件者
    if en == "1":#illegal device
        text = "Date : "+day+"\nSorce_device :"+sd+"\nSorce_ip : "+sip+"\n"
        text = text+"Event_device : "+dd+"\nEvent_ip : "+dip+"\nEvent port : "+pt+"\n"
        text = text + "Event describe :\nThe " +dd+" is not a legal device for "+sd+" to communicate.\n"
        text = text + "Please check that device, which may be attacked.\n"
    elif en =="2":#no priority to visit device -> cheat attack
        text = "Date : "+day+"\nSorce_device :"+sd+"\nSorce_ip : "+sip+"\n"
        text = text+"Event_device : "+dd+"\nEvent_ip : "+dip+"\nEvent port : "+pt+"\n"
        text = text + "Event describe :\nThe " +dd+" does not have permission to communicate with  "+sd+".\n"
        text = text + "Please check that device, which may be cheat attacked.\n"
    elif en == "3":#priority not enough to check folder -> physical attack
        text = "Date : "+day+"\nSorce_device :"+sd+"\nSorce_ip : "+sip+"\n"
        text = text+"Event_device : "+dd+"\nEvent_ip : "+dip+"\nEvent port : "+pt+"\n"
        text = text + "Event describe :\nThe " +dd+" does not have permission to check the folder.\n"
        text = text + "Please check that device, which may be physical attacked.\n"
    elif en == "4":#packet traffic analysis (sum of packet bigger than threshold) -> Dos attack
        text = "Date : "+day+"\nSorce_device :"+sd+"\nSorce_ip : "+sip+"\n"
        text = text+"Event_device : "+dd+"\nEvent_ip : "+dip+"\nEvent port : "+pt+"\n"
        text = text + "Event describe :\nThe " +dd+" sends a lot of packet to "+sd+",which is more than threshold.\n"
        text = text + "Please check that device, which may be DoS attacked.\n"

    content.attach(MIMEText(text))  #郵件內容

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("avril0930351909@gmail.com", "giax facu gysj jleq")  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
            print("\033[1;31;47mWe have sent a warning message to the monitoring staff!\033[0m")
        except Exception as e:
            print("Error message: ", e)

