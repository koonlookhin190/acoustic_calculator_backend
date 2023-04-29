import bcrypt
from sqlalchemy import event
from .materialUse import Material
from .database import db


@event.listens_for(Material.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(Material("Cylence Zandera", 0.24, 0.68, 0.89, 0.83, 0.77))
    db.session.add(Material("พื้นไม้ลามิเนต", 0.3, 0.2, 0.2, 0.15, 0.1))
    db.session.add(Material("พื้นไม้ปาเก้", 0.03, 0.06, 0.09, 0.1, 0.2))
    db.session.add(Material("อิฐ", 0.03, 0.03, 0.04, 0.05, 0.07))
    db.session.add(Material("ยิปซั่ม สมาร์ทบอร์ด", 0.1, 0.05, 0.04, 0.07, 0.1))
    db.session.add(Material("พรม", 0.06, 0.15, 0.4, 0.6, 0.6))
    db.session.add(Material("ผ้าม่าน", 0.3, 0.5, 0.7, 0.7, 0.6))
    db.session.add(Material("เหล็ก", 0.1, 0.1, 0.1, 0.7, 0.2))
    db.session.add(Material("กระเบื้องบนพื้นปูน", 0.03, 0.03, 0.03, 0.03, 0.02))
    db.session.add(Material("กระจก", 0.2, 0.2, 0.1, 0.7, 0.4))
    db.session.add(Material("แผ่นยิปซั่มเจาะรู Echo Block", 0.96, 0.81, 0.66, 0.53, 0.49))
    db.session.add(Material("แผ่นแขวน", 0.7, 0.73, 1.17, 1.28, 1.39))
    db.session.add(Material("Mboard 15 mm วางบน Tbar", 0.39, 0.7, 0.93, 0.89, 0.65))
    db.session.add(Material("Mboard 12 mm ติดใต้ฉาบเรียบ", 0.21, 0.51, 0.58, 0.65, 0.54))
    db.session.add(Material("Mboard 9 mm ติดใต้ฉาบเรียบ", 0.3, 0.37, 0.4, 0.4, 0.4))
    db.session.add(Material("โพลี 12 mm", 0.08, 0.21, 0.46, 0.69, 0.79))
    db.session.add(Material("ใยแก้ว / ฟองน้ำ 50 mm", 0.68, 0.87, 1.0, 1.0, 0.95))
    db.session.add(Material("โพลี 10 mm", 0.12, 0.27, 0.6, 0.81, 0.93))
    db.session.add(Material("พื้นปูน", 0.03, 0.03, 0.03, 0.03, 0.02))
    db.session.add(Material("ใยแก้ว / ฟองน้ำ 25 mm", 0.34, 0.66, 0.9, 0.86, 0.74))
    db.session.commit()
