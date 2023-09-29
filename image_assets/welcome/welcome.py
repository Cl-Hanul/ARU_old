from PIL import Image, ImageOps, ImageDraw, ImageFont

def getwelcome(profileImage:Image,serverName:str,nick:str) -> Image:
    size = (224,224)
    mask = Image.new('L', size, 255)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=0)

    im = profileImage
    bg = Image.open('image_assets/welcome.png')

    profile = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    profile.paste(0, mask=mask)
    profile.convert('P', palette=Image.ADAPTIVE)

    text = f"`{serverName}`에 오신 것을"
    text2 = "환영합니다-!"
    font = ImageFont.truetype("font/학교안심 가을소풍B.ttf",64)

    bg.paste(profile,(239,35),profile)
    draw = ImageDraw.Draw(bg)
    draw.text((350,340),text,(255,255,255),font,anchor='ms')

    font = ImageFont.truetype("font/학교안심 가을소풍B.ttf",120)
    draw.text((110,370),text2,(255,255,255),font)

    draw.rounded_rectangle((224,220,474,270),fill="#ffd8ee")

    font = ImageFont.truetype("font/학교안심 가을소풍B.ttf",30)

    draw.text((330,230),nick,(0,0,0),font,align="center")

    return bg