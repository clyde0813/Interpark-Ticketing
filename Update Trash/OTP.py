totp = pyotp.TOTP('OB4XI2DPNZWW623QN5RWQ33J')
while True:
    input_otp = input('OTP :')
    if input_otp == totp.now():
        print('True')
        break
    else:
        print("false")
        sys.exit()