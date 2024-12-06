from app.init_db import db
from app import create_app
from app.models import InventoryItem, Customer, Transaction

app = create_app()

with app.app_context():
    Customer1 = Customer(c_Name='Ambar', c_Email='ambargogia@gmail.com', c_Contact='9811896306')
    Customer2 = Customer(c_Name='Admin', c_Email='adminadmin@gmail.com', c_Contact='9101912123')
    Customer1.validate_phone_number()
    Customer2.validate_email()
    db.session.add(Customer1)
    db.session.add(Customer2)
    Transaction1 = Transaction(c_ID=1, t_Date='2024-12-06', t_Amount=500, t_Category='A')
    Transaction1.validate_amount()
    InventoryItem1 = InventoryItem(Item_Name='Rand1', Item_Price=20, Item_Qty=30)
    InventoryItem2 = InventoryItem(Item_Name='Rand2', Item_Price=21, Item_Qty=32)
    InventoryItem1.validate_price()
    InventoryItem2.validate_price()
    
    db.session.add(Transaction1)
    db.session.add(InventoryItem1)
    db.session.add(InventoryItem2)

    db.session.commit()


    
    
    print(f'Total value of inventory is: {InventoryItem.total_val}')
    