import qrcode

qr = qrcode.QRCode(version = 2,
                   error_correction = qrcode.constants.ERROR_CORRECT_H,
                   box_size = 20,
                   border = 2)

qr.add_data("https://brandon-cho.mystrikingly.com/") #'{LINK}'
qr.make(fit = True)

img = qr.make_image(fill_color = 'black', back_color = 'pink')
img.save('portfolio.png') #'name'.png
