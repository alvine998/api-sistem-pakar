from app import mysql, bcrypt
import MySQLdb.cursors
from datetime import datetime
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# class Disease:
    # def __init__(self, id=None, name=None):
    #     self.id = id
    #     self.name = name

    # def to_dick(self):
    #     return {"id": self.id, "name": self.name}

    # @staticmethod
    # def create(name):
        