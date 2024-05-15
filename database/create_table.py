from sqlalchemy import  Column, Integer, ForeignKey, String, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Category(Base): 
    __tablename__ = "dim_category"
    category_id = Column(Integer, primary_key=True)
    category = Column(String(40))
    
class Product(Base): 
    __tablename__ = "dim_product"
    product_id = Column( Integer, primary_key=True)
    product_name = Column(String(40))
    shipping_priority = Column(String(40))
    unit_price = Column(Integer)
    shipping_priority = Column(String(40))
    category_id = Column(Integer, ForeignKey("dim_category.category_id"), nullable=False)
    category = relationship("Category")


    
class Delivery(Base): 
    __tablename__ = "dim_delivery_date"
    delivery_date_id = Column(Integer, primary_key=True)
    delivery_date = Column(DATE)
    delivery_month = Column(Integer)
    delivery_quarter = Column(Integer)
    delivery_year = Column(Integer)
    delivery_day = Column(Integer)
    delivery_week_day = Column(String(15))

class Shipment(Base): 
    __tablename__ = "dim_shipment_date"
    shipment_date_id = Column(Integer, primary_key=True)
    shipment_date = Column(DATE)
    shipment_month = Column(Integer)
    shipment_quarter = Column(Integer)
    shipment_year = Column(Integer)
    shipment_day = Column(Integer)
    shipment_week_day = Column(String(15))

class Time(Base): 
    __tablename__ = "dim_date"
    date_id = Column(Integer, primary_key=True)
    delivery_date_id = Column(Integer, ForeignKey("dim_delivery_date.delivery_date_id"), nullable=False)
    delivery = relationship("Delivery")
    shipment_date_id = Column(Integer, ForeignKey("dim_shipment_date.shipment_date_id"), nullable=False)
    shipment = relationship("Shipment")


class Destination(Base): 
    __tablename__ = "dim_courier_destination"
    destination_id = Column(Integer, primary_key=True)
    destination_city = Column(String(50))
    destination_state = Column(String(50))
    destination_country = Column(String(50))
    
class Origin(Base): 
    __tablename__ = "dim_courier_origin"
    origin_id = Column(Integer, primary_key=True)
    origin_city = Column(String(50))
    origin_state = Column(String(50))
    origin_country = Column(String(50))
    
        
class Courier(Base): 
    __tablename__ = "dim_courier"
    courier_id = Column(Integer, primary_key=True)
    carrier_name = Column(String(40))
    carrier_rating = Column(Integer)
    mode_of_transport = Column(String(40))
    destination_id = Column(Integer, ForeignKey("dim_courier_destination.destination_id"), nullable=False)
    destination = relationship("Destination")
    origin_id = Column(Integer, ForeignKey("dim_courier_origin.origin_id"), nullable=False)
    origin = relationship("Origin")

class City(Base): 
    __tablename__ = 'dim_customer_city'
    city_id = Column(Integer, primary_key=True)
    customer_city = Column(String(40))    
    customer_state = Column(String(40))
    customer_country = Column(String(40))

class Payment(Base): 
    __tablename__ = 'dim_customer_payment'
    payment_id = Column(Integer, primary_key=True)
    payment_method = Column(String(40))   

class Customer(Base): 
    __tablename__ = 'dim_customer'
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String(40))    
    customer_segment = Column(String(40))
    city_id = Column(Integer, ForeignKey("dim_customer_city.city_id"), nullable=False)
    city = relationship("City")
    payment_id = Column(Integer, ForeignKey("dim_customer_payment.payment_id"), nullable=False)
    payment = relationship("Payment")
       
    
class Fact(Base): 
    __tablename__ = "fact_table"
    shipment_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    total_cost = Column(Integer)
    courier_id = Column(Integer, ForeignKey("dim_courier.courier_id"), nullable=False)
    courier = relationship("Courier")
    date_id = Column(Integer, ForeignKey("dim_date.date_id"), nullable=False)
    time = relationship('Time')
    product_id = Column( Integer, ForeignKey("dim_product.product_id"), nullable=False)
    product = relationship('Product')
    customer_id = Column(Integer, ForeignKey("dim_customer.customer_id"), nullable=False)
    customer = relationship('Customer')

def create_db_table(engine): 
    """
    Creates database tables based on SQLAlchemy metadata.

    This function drops existing tables (if any) and creates new tables based on the SQLAlchemy metadata defined in Base.

    Args:
        engine (Engine): SQLAlchemy engine object for the database.

    Raises:
        Exception: If an error occurs during the table creation process.
    """
    try: 
        # Drop existing tables
        Base.metadata.drop_all(engine, 
                               tables=[Base.metadata.tables["dim_category"], 
                                       Base.metadata.tables["dim_product"],
                                       Base.metadata.tables["dim_delivery_date"], 
                                       Base.metadata.tables["dim_shipment_date"],
                                       Base.metadata.tables["dim_date"],
                                       Base.metadata.tables["dim_courier_destination"], 
                                       Base.metadata.tables["dim_courier_origin"], 
                                       Base.metadata.tables["dim_courier"],
                                       Base.metadata.tables["dim_customer_city"], 
                                       Base.metadata.tables["dim_customer_payment"], 
                                       Base.metadata.tables["dim_customer"],
                                       Base.metadata.tables["fact_table"]]) 
        # Create new tables
        Base.metadata.create_all(engine)
        print("all table successfully created")
        
    except Exception as e: 
        raise Exception(f"Error creating tables: {e}")