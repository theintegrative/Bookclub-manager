import pandas as pd
import numpy as np
import pymongo
from pprint import pprint
import bookclub_test_data as td

def first_day():
    now = pd.Timestamp.now() - pd.offsets.MonthBegin(1)
    return now.strftime('%Y-%m-%d')

def last_day():
    now = pd.Timestamp(first_day()) + pd.offsets.MonthBegin(1)
    return now.strftime('%Y-%m-%d')

between_dates_query = {"date":{"$gte": first_day(), "$lt": last_day()}}
vote_count_pipline = [{ "$addFields": {"vote_count": { "$size": "$votes" } } }]
reset_vote = [{"$set": {"votes": [], "vote_count": 0}}]
# vote = [{"$push": {"votes": }}]
find = {"_id": 0}
find_titles = {"title": 1}
find_books = { "_id": 0, "date": 0, "votes": 0}
find_nice = { "_id": 0, "votes": 0}
sort_books = [("vote_count", -1), ("date", 1)] # first highest vote count then lowest date

class Collection:
    def __init__(self, collection):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.client["bookclub"]
        self.collection = self.mydb[collection]

    def add(self, book):
        self.collection.insert_one(book)
    
    def add_many(self, books):
        self.collection.insert_many(books)
    
    def add_vote(self, title, username):
        self.collection.update_one({"title": title}, [{"$push": {"votes": usermame}}])
        
    def add_votes(self, title, usernames):
        self.collection.update_one({"title": title}, [{"$push": {"votes": {"$each": usermames}}}])

    def delete(self, book):
        self.collection.delete_one(book)

    def count_votes(self):
        self.collection.update_many({}, vote_count_pipline)
        
    def reset_votes(self):
        self.collection.update_many({}, reset_vote)

    def drop(self):
        self.collection.drop()

    def find_all(self, query, fields, sort):
        for book in self.collection.find(query,fields).sort(sort):
            yield book
            
    def find(self, query, fields, sort, total):
        for book in self.collection.find(query,fields).sort(sort).limit(total):
            yield book

class Manager:
    def __init__(self):
        self.incomming = Collection("incomming")
        self.potential = Collection("potential")
        self.buffer = Collection("buffer")
        self.total = 3
        self.book_of_month = ""
    
    def incomming_books(self, books):
        self.incomming.add_many(books)
        self.incomming.count_votes()
        return [book for book in self.incomming.find(between_dates_query, find_nice, sort_books, self.total)]
    
    def potential_books(self, books):
        self.potential.add_many(books)
        self.potential.reset_votes()
        random_book = np.random.choice([book for book in self.incomming.find_all({},{},[("date", -1)])])
        self.book_of_month = random_book
        self.potential.delete(random_book)
        return self.book_of_month
       
    def potential_remove(self):
        # this is also for generating tests > wil be moved to a dedicated testfile
        for title in self.potential.find_all({}, find_titles, sort_books):
            self.potential.add_votes(title["title"], td.generate_title_votes(1))
        self.potential.count_votes()
        for book in self.find(between_dates_query, find_nice, sort_books, self.total):
            self.buffer.add(book)
            self.potential.delete(book)
            
    def drop_all(self):
        bookclub.incomming.drop()
        bookclub.potential.drop()
        bookclub.buffer.drop()
