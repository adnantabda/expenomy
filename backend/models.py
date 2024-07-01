from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from config import db



class User(db.Model):
    __tablename__ = "users"

    username = Column(String, primary_key=True, nullable=False, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    profile = Column(String)  # Change To path For the Future

    categories = relationship("Category", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    incomes = relationship("Income", back_populates="user")
    budgets = relationship("Budget", back_populates="user")

    def to_json(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "profile": self.profile,
        }


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    total_amount = Column(Float)
    user_username = Column(String, ForeignKey('users.username'))

    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "total_amount": self.total_amount,
            "username": self.user_username
        }


class Expense(db.Model):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float, nullable=False)
    description = Column(String)
    date = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_username = Column(String, ForeignKey('users.username'))

    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "description": self.description,
            "date": self.date,
            "categoryId": self.category_id,
            "username": self.user_username
        }


class Income(db.Model):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Float, nullable=False)
    date = Column(String)
    description = Column(String)
    user_username = Column(String, ForeignKey('users.username'))

    user = relationship("User", back_populates="incomes")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "date": self.date,
            "description": self.description,
            "username": self.user_username
        }


class Budget(db.Model):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    amount = Column(Integer, nullable=False)
    description = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    username = Column(String, ForeignKey("users.username"))

    user = relationship("User", back_populates="budgets")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "username": self.username,
        }