# J POS - GOLDEN EDITION - FINAL CODE
# Power By: J POS Company
import json, os, hashlib, platform
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import textwrap

# ===== 1. SECURITY SYSTEM (TOP PE) =====
def get_mid():
    raw = platform.node() + platform.processor()
    return hashlib.md5(raw.encode()).hexdigest()[:8].upper()

MID = get_mid()
LIC_FILE = "jpos.lic"
SETTINGS_FILE = "shop_settings.json"

print(f"--- J POS GOLDEN EDITION ---")
print(f"Machine ID: {MID}")

def check_license():
    if os.path.exists(LIC_FILE):
        d = json.load(open(LIC_FILE))
        if d['mid'] != MID:
            print("❌ COPY BLOCKED!")
            return False
        exp = datetime.strptime(d['exp'], "%Y-%m-%d")
        if datetime.now() > exp:
            print("❌ License Expire!")
            os.remove(LIC_FILE)
            return False
        return True
    else:
        key = input("License Key (DEMO likho 7 din ke liye): ").strip().upper()
        if key == "DEMO":
            exp = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            json.dump({"mid":MID, "exp":exp}, open(LIC_FILE,"w"))
            print(f"✅ 7 Din Demo Active!")
            return True
        if MID not in key:
            print("❌ Invalid Key!")
            return False
        exp_str = key.split("-")[-1]
        exp_date = datetime.strptime(exp_str, "%Y%m%d").strftime("%Y-%m-%d")
        json.dump({"mid":MID, "exp":exp_date, "key":key}, open(LIC_FILE,"w"))
        print(f"✅ Activated till {exp_date}")
        return True

if not check_license():
    exit()

# ===== 2. SHOP SETTINGS (Customer Editable) =====
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        return json.load(open(SETTINGS_FILE))
    else:
        # Default settings - Customer yahan se change karega
        default = {
            "shop_name": "Rajpoot Electric",
            "shop_address": "Gujar Khan",
            "support_number": "03XX-XXXXXXX"
        }
        json.dump(default, open(SETTINGS_FILE,"w"), indent=4)
        return default

settings = load_settings()
print(f"Shop: {settings['shop_name']} | {settings['shop_address']}")

# ===== 3. BILL GENERATOR (80mm Thermal Look) =====
def generate_bill(bill_no, items, total, paid):
    # 80mm = 576px width
    W = 576
    H = 900
    img = Image.new('RGB', (W, H), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        # Font - agar na ho to default
        font_bold = ImageFont.truetype("arialbd.ttf", 32)
        font_bold_small = ImageFont.truetype("arialbd.ttf", 24)
        font_normal = ImageFont.truetype("arial.ttf", 22)
        font_small = ImageFont.truetype("arial.ttf", 20)
    except:
        font_bold = ImageFont.load_default()
        font_bold_small = ImageFont.load_default()
        font_normal = ImageFont.load_default()
        font_small = ImageFont.load_default()

    y = 20
    # --- TOP J POS LOGO (FIXED) ---
    draw.text((W//2, y), "♛", font=font_bold, fill='black', anchor='mt')
    y += 35
    draw.text((W//2, y), "J POS", font=font_bold, fill='black', anchor='mt')
    y += 45
    draw.text((W//2, y), "J POS - COMPANY LOGO", font=font_small, fill='black', anchor='mt')
    y += 30
    draw.text((W//2, y), "-"*38, font=font_small, fill='black', anchor='mt')
    y += 25

    # --- MIDDLE SHOP NAME (EDITABLE) ---
    draw.text((W//2, y), settings['shop_name'], font=font_bold_small, fill='black', anchor='mt')
    y += 35
    draw.text((W//2, y), f"Address: {settings['shop_address']}", font=font_normal, fill='black', anchor='mt')
    y += 30
    draw.text((W//2, y), "-"*38, font=font_small, fill='black', anchor='mt')
    y += 25

    # Bill Info
    draw.text((20, y), f"Bill No: {bill_no}  Date: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}", font=font_normal, fill='black')
    y += 30
    draw.text((20, y), f"Cashier: Owner", font=font_normal, fill='black')
    y += 30
    draw.text((W//2, y), "-"*38, font=font_small, fill='black', anchor='mt')
    y += 25

    # Items Header
    draw.text((20, y), f"ITEM", font=font_bold_small, fill='black')
    draw.text((W-20, y), f"AMT", font=font_bold_small, fill='black', anchor='rt')
    y += 35
    draw.line((20, y, W-20, y), fill='black', width=2)
    y += 10

    for name, qty, price, amt in items:
        line = f"{name}  {qty} x {price}"
        draw.text((20, y), line, font=font_normal, fill='black')
        draw.text((W-20, y), str(amt), font=font_normal, fill='black', anchor='rt')
        y += 30

    y += 10
    draw.text((W//2, y), "-"*38, font=font_small, fill='black', anchor='mt')
    y += 25

    # Totals
    draw.text((20, y), f"TOTAL", font=font_bold_small, fill='black')
    draw.text((W-20, y), str(total), font=font_bold_small, fill='black', anchor='rt')
    y += 35
    draw.text((20, y), f"PAID", font=font_bold_small, fill='black')
    draw.text((W-20, y), str(paid), font=font_bold_small, fill='black', anchor='rt')
    y += 35
    draw.text((20, y), f"RETURN", font=font_bold_small, fill='black')
    draw.text((W-20, y), str(paid-total), font=font_bold_small, fill='black', anchor='rt')
    y += 40
    draw.text((W//2, y), "-"*38, font=font_small, fill='black', anchor='mt')
    y += 30

    # --- BOTTOM J POS (FIXED) ---
    draw.text((W//2, y), "♛", font=font_bold, fill='black', anchor='mt')
    y += 35
    draw.text((W//2, y), "J POS", font=font_bold, fill='black', anchor='mt')
    y += 45
    draw.text((W//2, y), "Powered by J POS - Golden Edition", font=font_normal, fill='black', anchor='mt')
    y += 25
    draw.text((W//2, y), f"Support: {settings['support_number']}", font=font_normal, fill='black', anchor='mt')
    y += 25
    draw.text((W//2, y), "Thank You • Visit Again", font=font_normal, fill='black', anchor='mt')

    # Crop
    img_cropped = img.crop((0, 0, W, y+40))
    filename = f"Bill_{bill_no}_{datetime.now().strftime('%d%m%Y_%H%M')}.png"
    img_cropped.save(filename)
    print(f"✅ Bill Generated: {filename}")
    img_cropped.show()

# ===== 4. DEMO RUN =====
if __name__ == "__main__":
    demo_items = [
        ("china board 8+2", 2, 750, 1500),
        ("Ghee Dalda 1KG", 1, 500, 500),
        ("Sugar 1KG", 2, 150, 300)
    ]
    generate_bill(bill_no=1025, items=demo_items, total=2300, paid=2500)
    
    # Shop name change option
    ch = input("\nKya shop name change karna hai? (y/n): ")
    if ch.lower() == 'y':
        new_name = input("Naya Shop Name: ")
        new_addr = input("Naya Address: ")
        settings['shop_name'] = new_name
        settings['shop_address'] = new_addr
        json.dump(settings, open(SETTINGS_FILE,"w"), indent=4)
        print("✅ Shop Settings Update Ho Gaye!")