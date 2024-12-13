from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Coin(Base):
    __tablename__ = "coins"
    
    coin_id = Column(String, index=True)
    trending_date = Column(String, index=True)  # Adjusted for PEP-8 compliance
    coin_name = Column(String, index=True)
    
    # Define composite primary key
    __table_args__ = (
        PrimaryKeyConstraint("coin_id", "trending_date", name="pk_coin"),
    )

    def __repr__(self):
        return f"<Coin(coin_id={self.coin_id}, trending_date='{self.trending_date}', coin_name='{self.coin_name}')>"
