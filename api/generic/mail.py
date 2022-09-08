from flask_mail import Message
from api.extensions import mail


def send_password_to_voter(voter_email: str, voter_name: str, password: str):
    msg = Message(
        "KNUST Voting Details",
        sender="thesupernovaegroups@gmail.com",
        recipients=[voter_email],
    )
    msg.body = f"""
    Hello {voter_name},
    Find below your password for the voting process
    Password: {password}
    """
    mail.send(msg)
    return "Message sent"


def send_password_to_admin(admin_email: str, admin_name: str, password: str):
    msg = Message(
        "KNUST Voting Details",
        sender="thesupernovaegroups@gmail.com",
        recipients=[admin_email],
    )
    msg.body = f"""
    Hello {admin_name},
    You have been granted administrator privileges
    Find below your password for the KNUST Voting Platform
    Password: {password}
    """
    mail.send(msg)
    return "Message sent"
