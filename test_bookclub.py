#!/usr/bin/env python
# coding: utf-8

import pytest

# python files to test
import bookclub_manager as bcm

# testdata
import testing_data as td

@pytest.fixture
def incomming():
    yield bcm.Collection("incomming")

@pytest.fixture
def potential():
    yield bcm.Collection("potential")

@pytest.fixture
def buffer():
    yield bcm.Collection("buffer")

@pytest.fixture
def books_this_month():
    yield td.generate_books(10, 1)

@pytest.fixture
def books_two_months():
    yield td.generate_books(20, 2)

#@pytest.fixture # this still needs to be created
#def books_next_month():
#    yield td.generate_books(10, 1)

@pytest.fixture
def manager():
    return bcm.Manager()

@pytest.fixture
def generate_votes_potential(potential):
    for title in potential.find_all({}, find_titles, sort_books):
        potential.add_votes(title["title"], td.generate_title_votes(1))

@pytest.fixture
def generate_votes_incomming(incomming):
    for title in incomming.find_all({}, find_titles, sort_books):
        incomming.add_votes(title["title"], td.generate_title_votes(1))
