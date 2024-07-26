import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to_email):
    from_email = "your email here"
    password = "your password here"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.set_debuglevel(1)  # Enable debug output
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(from_email, password)  # Login to the email server
            server.sendmail(from_email, to_email, msg.as_string())  # Send the email
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

def show():
    st.title("Contact Us")

    st.markdown("""
    If you have any questions or feedback, please use the form below to reach out to us. We'll get back to you as soon as possible.
    """)

    # Create the contact form
    with st.form(key='contact_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        submit_button = st.form_submit_button("Send")

        if submit_button:
            email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            if send_email(subject, email_body, "guyet.julien@outlook.com"):
                st.success("Your message has been sent successfully!")
            else:
                st.error("There was a problem sending your message. Please try again later.")

if __name__ == "__main__":
    show()
