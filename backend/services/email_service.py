# backend/services/email_service.py
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from ibm_db import result
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER     = os.getenv("GMAIL_USER", "")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")   # Gmail App Password (not account password)
FRONTEND_URL   = os.getenv("FRONTEND_URL", "http://localhost:5173")


def send_reset_email(to_email: str, reset_token: str, user_name: str) -> bool:
    """Send a password-reset link via Gmail SMTP. Returns True on success."""
    if not GMAIL_USER or not GMAIL_PASSWORD:
        print("[email_service] GMAIL_USER / GMAIL_APP_PASSWORD not set — skipping email send")
        return False

    reset_link = f"{FRONTEND_URL}?reset_token={reset_token}"

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <style>
    body {{ font-family: 'DM Sans', Arial, sans-serif; background:#06070c; margin:0; padding:0; }}
    .wrap {{ max-width:520px; margin:40px auto; background:#0d0f18;
             border:1px solid rgba(255,255,255,0.07); border-radius:18px; overflow:hidden; }}
    .header {{ background:linear-gradient(135deg,#2563eb,#3b82f6);
               padding:32px 40px; text-align:center; }}
    .logo {{ font-size:22px; font-weight:700; color:#fff; letter-spacing:-0.5px; }}
    .logo span {{ color:#bfdbfe; }}
    .body {{ padding:36px 40px; color:#e8eaf0; }}
    h2 {{ font-size:18px; font-weight:600; margin:0 0 12px; color:#e8eaf0; }}
    p {{ font-size:14px; color:#8b90a4; line-height:1.7; margin:0 0 18px; }}
    .btn {{ display:inline-block; padding:12px 32px; background:#2563eb;
            color:#fff; text-decoration:none; border-radius:10px;
            font-weight:600; font-size:14px; margin:4px 0 24px;
            box-shadow:0 0 24px rgba(37,99,235,0.35); }}
    .footer {{ background:#06070c; padding:18px 40px; text-align:center; }}
    .footer p {{ font-size:11px; color:#4b5068; margin:0; line-height:1.6; }}
    .link {{ color:#60a5fa; word-break:break-all; font-size:12px; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <div class="logo">📄 DOCU<span>Assist</span></div>
    </div>
    <div class="body">
      <h2>Reset your password</h2>
      <p>Hi {user_name},</p>
      <p>We received a request to reset your DOCUAssist password.
         Click the button below to create a new password.
         This link expires in <strong>15 minutes</strong>.</p>
      <a class="btn" href="{reset_link}">Reset password →</a>
      <p>If the button doesn't work, copy and paste this link into your browser:</p>
      <p class="link">{reset_link}</p>
      <p>If you didn't request this, you can safely ignore this email —
         your password won't change.</p>
    </div>
    <div class="footer">
      <p>DOCUAssist · AI-powered document intelligence<br/>
         This email was sent to {to_email}</p>
    </div>
  </div>
</body>
</html>
"""

    text = (
        f"Hi {user_name},\n\n"
        f"Reset your DOCUAssist password (expires in 15 minutes):\n"
        f"{reset_link}\n\n"
        f"If you didn't request this, ignore this email.\n"
    )
    print("User:", GMAIL_USER)
    print("Password set:", bool(GMAIL_PASSWORD))
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset your DOCUAssist password"
    msg["From"]    = f"DOCUAssist <{GMAIL_USER}>"
    msg["To"]      = to_email
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.set_debuglevel(1)

            server.login(GMAIL_USER, GMAIL_PASSWORD)

            result = server.sendmail(
                GMAIL_USER,
                [to_email],
                msg.as_string()
            )

            print("SMTP Result:", result)

        print(f"[email_service] Reset email sent to {to_email}")
        return True

    except Exception as e:
        print(f"[email_service] Failed to send email: {e}")
        return False







# from fastapi import FastAPI, Depends     
# from sqlalchemy.orm import Session         # To create a db session
# from database import get_db, Base, engine         
# import models
# import auth
# from auth import *
# from datetime import timedelta         # For time difference
# from schemas import *
# from passlib.context import CryptContext       # For hashing password

# #-----smtp-----
# import smtplib
# from email.message import EmailMessage
# from dotenv import load_dotenv
# import os


# load_dotenv()

# app = FastAPI(title="FastAPI Sync Base")

# Base.metadata.create_all(bind = engine)

# @app.get("/")
# def root():
#     return {"message": "FastAPI is running"}

# @app.get("/health")
# def health_check(db: Session = Depends(get_db)):
#     return {"status": "OK"}

# # @app.get("/token_create")
# # def create_token(username: str, id: int):
# #     return create_access_token(username, id, timedelta(minutes=20))

# # @app.get("/token_verify")
# # def verify_token(token: str):
# #     return verify_access_token(token)


# pwd_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

# #Creating a new user 
# #Hashing the password before storing
# @app.post("/register")
# def create_user(data : user_data, db: Session=Depends(get_db)):

#     try: 
#         new_user = user_data(
#             username = data.username,
#             password = pwd_context.hash(data.password)
#         )
#         db.add(models.Users(**new_user.model_dump()))
#         db.commit()
#         return "User Added successfully"
#     except Exception as e:
#         return "Some error"
    
# # Logging user and creating token
# @app.post("/login")
# def user_login(credentials : user_data, db: Session = Depends(get_db)):
#     valid_user = db.query(models.Users).filter(models.Users.username == credentials.username).first()
#     if not valid_user:
#         return "No user exists with this Username"
    
#     hashed_password = valid_user.password
#     check = pwd_context.verify(credentials.password, hashed_password)
#     print(check)
#     if not check:
#         return "Incorrect Password"
    
#     print("User Exists")
#     token = create_access_token(valid_user.username, timedelta(minutes=30))
#     return token

# # Validating User
# @app.post("/verify_token")
# def verify_token(token: str, db:Session = Depends(get_db)):
#     token_data = verify_access_token(token)
#     token_sub = token_data.get('sub')
    
#     db_data = db.query(models.Users).filter(models.Users.username == token_sub).first()
#     if not db_data:
#         return "Invalid Token"
    
#     token_exp = token_data.get('exp')
#     print(type(token_exp))
#     if token_exp < (datetime.now(timezone.utc)).timestamp():
#         return "Token has been expired"
    
#     return "You are a valid user"


# #----------------SMTP------------------
# @app.get("/smtp")
# def stmp():
#     smtp_server = os.getenv("SMTP_SERVER")
#     smtp_port = os.getenv("SMTP_PORT")
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()

#     username = os.getenv("SMTP_USERNAME")
#     password = os.getenv("SMTP_PASSWORD")
#     server.login(username, password)

#     msg = EmailMessage()
#     msg["Subject"] = "Testing"
#     msg["From"] = username
#     msg["To"] = "singhkaranpreet@seasiaconnect.com"
#     msg.set_content("Hey, /n/nIt's a wonderful day!")

#     server.send_message(msg)
#     server.quit
#     return "Message Sent "

