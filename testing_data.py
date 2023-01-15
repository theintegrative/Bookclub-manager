from pprint import pprint
from datetime import datetime
import numpy as np
import pandas as pd

def first_day():
    now = pd.Timestamp.now()
    now = now - pd.offsets.MonthBegin(1)
    return now.strftime('%Y-%m-%d')

def days_of_this_month(months):
    last_day = pd.date_range(first_day(), periods=months, freq="M")
    return pd.date_range(start=first_day(), end=last_day[months-1])

def weeks_of_this_month():
    _first_day = first_day()
    last_days = pd.date_range(_first_day, periods=5, freq="W")
    for last_day in last_days:
        yield pd.date_range(start=_first_day, end=last_day)
        _first_day = last_day

def book_dict(title, author, pages, user, votes, date):
    return {"title": title, "author": author, "pages": pages, "user": user, "votes": votes, "date": date}

def generate_str(total, name):
    for num in range(total):
        string = f"{name}-{num}"
        yield string

def generate_num(total):
    pages_low = 100
    pages_high = 500
    for num in np.random.randint(pages_low, pages_high, total):
        yield int(num)

def generate_votes(low, high, total):
    for num in np.random.randint(low, high, total):
        yield np.random.choice([str for str in generate_str(total, "user")], size=num).tolist()

def generate_dates(total, months):
    for date in np.random.choice(days_of_this_month(months), size=total):
        moment = pd.Timestamp(date)
        yield moment.strftime('%Y-%m-%d')
        
def generate_books(total, months):
    votes_low = 0 
    votes_high = 6
    title = generate_str(total, "title")
    author = generate_str(total, "author") 
    pages = generate_num(total) 
    user = generate_str(total, "user") 
    votes = generate_votes(votes_low, votes_high, total) 
    date = generate_dates(total, months)
    for _ in range(total):
        book = book_dict(next(title), next(author), next(pages), next(user), next(votes), next(date))
        yield book
        
def generate_title_votes(total):
    votes_low = 0 
    votes_high = 6
    return generate_votes(votes_low, votes_high, total) 
  
#books = generate_books(10, 1)
#book_list = [book for book in books]
#pprint(book_list)
