# College Smart Alumni - Email + Phone OTP Verification

Registration now requires verification of both the email address and phone number.

## 1. Create `.env`

Copy `.env.example` to `.env` in the same folder as `manage.py`.

### Gmail
Use a Gmail **App Password** for `EMAIL_HOST_PASSWORD`; do not put your normal Gmail password in the project.

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Twilio SMS
Create a Twilio account, obtain an Account SID, Auth Token, and a Twilio-enabled sending number, then set:

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM_NUMBER=+1xxxxxxxxxx
```

Phone numbers entered during registration must use international format, for example:

```text
+919876543210
```

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. Apply migrations

```powershell
python manage.py migrate
```

## 4. Run

```powershell
python manage.py runserver
```

## Registration flow

1. User fills the registration form.
2. Account is created inactive.
3. A 6-digit OTP is emailed to the email address.
4. A separate 6-digit OTP is sent by SMS to the phone number.
5. User enters both OTPs on `/accounts/verify-otp/`.
6. Only after both are correct does the account become active and the user is logged in.
7. OTPs expire after 10 minutes and are limited to 5 failed attempts.


## SSS College administrator

The project includes a management command for the requested administrator account:

```powershell
python manage.py migrate
python manage.py ensure_college_admin
```

Administrator login:
- Username: `SSSCOLLEGE`
- Password: `SSS@555`

The command creates the account if it does not exist, or updates the existing `SSSCOLLEGE` account.

## Dark / Light mode

A Dark Mode / Light Mode toggle is available from the navigation bar and login page. The selected theme is saved in the browser, so it remains selected when moving between pages.
