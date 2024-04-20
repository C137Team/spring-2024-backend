import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import APIRouter, FastAPI, HTTPException, BackgroundTasks, status
from pydantic import BaseModel
from typing import Dict
from random import randint
import smtplib
from email.message import EmailMessage

email_address = "maoirtx77@gmail.com"
email_password = "zqia tkvq ppcj sead"

router = APIRouter()

confirmation_codes: Dict[str, str] = {}

class Email(BaseModel):
    email: str

class ConfirmationCode(BaseModel):
    code: str


def generate_confirmation_code() -> str:
    return str(randint(1000, 9999))


def send_message(receiver_email: str, content: str):
    msg = EmailMessage()
    msg['Subject'] = "Email subject"
    msg['From'] = email_address
    msg['To'] = receiver_email
    msg.set_content(content)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)


def send_confirmation_code(email: str, code: str):
    receiver_email = email
    
    send_message(receiver_email, f"Your confirmation code is: {code}")
    print(f"Confirmation code sent to {receiver_email}")


    return "email successfully sent"


@router.post("/auth/request-code")
async def request_confirmation_code(email: Email, background_tasks: BackgroundTasks):
    user_domain = email.email.split('@')[-1]
    #проверка на почту компании: (изменить)
    if user_domain != "gmail.com": 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    code = generate_confirmation_code()
    confirmation_codes[email.email] = code
    background_tasks.add_task(send_confirmation_code, email.email, code)

    return {"message": "Confirmation code has been sent to your email."}


@router.post("/auth/confirm-code/")
async def confirm_code(email: Email, code_data: ConfirmationCode):
    if email.email in confirmation_codes and code_data.code == confirmation_codes[email.email]:
        send_message(email.email, "Вы успешно зарегистрировались! Мы рады вас видеть RandomCoffee!")
        return {"message": "Authentication successful for email: " + email.email}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid confirmation code")


@router.get("/auth")
async def index():
    return {"message": "Server is running. Use /auth/request-code and /auth/confirm-code endpoints for authentication."}
