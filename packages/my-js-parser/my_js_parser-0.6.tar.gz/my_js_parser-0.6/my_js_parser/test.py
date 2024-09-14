
import pyotp
key = 'CIDIDK3ZX3GD6K7CRIJ4567HP3NSLXEE'
totp = pyotp.TOTP(key)
print(totp.now())