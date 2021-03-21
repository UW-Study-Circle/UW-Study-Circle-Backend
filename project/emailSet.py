


def send_email(user):
    token = user.get_reset_token()
    msg = Message()
    msg.subject = "UW-Study-Circle Password Reset"
    msg.sender = app.config('MAIL_USERNAME')
    msg.recipients = [user.email]
    msg.html = render_template('reset_password_email.html', user=user, token=token)
    # msg.body = render_template('email/reset_password.txt', user=user, token=token)
