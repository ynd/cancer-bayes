#!/usr/bin/env python
# encoding: utf-8
"""
bayes.py

Created by  on 2010-04-30.
Copyright (c) 2010 Lambda Tree Media. All rights reserved.
"""

import sys
import os
import re


def read_database(filename):
  f = open(filename)
  d = re.findall(r"\d+ (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)", f.read())
  
  return map(lambda x: [int(a) for a in x], d)

def get_probability(database, event, conditions=[]):
  universe = filter(lambda x: False not in [x[a] == v for a, v in conditions], database)
  
  set = filter(lambda x: False not in [x[a] == v for a, v in event], universe)
  
  return float(len(set)) / len(universe)

def train(database):
  p_cancer = get_probability(database, [(9, 1)])
  p_conditionals = {}

  for attr in range(9):
    p_conditionals[attr] = {}
  
    for value in range(1, 11):
      p_positive = get_probability(database, [(attr, value)], conditions=[(9, 1)])
      p_negative = get_probability(database, [(attr, value)], conditions=[(9, 0)])
      p_conditionals[attr][value] = (p_positive, p_negative)

  return p_cancer, p_conditionals

def predict(case, p_cancer, p_conditionals):
  positive = p_cancer
  
  for attr in range(9):
    positive *= p_conditionals[attr][case[attr]][0]
  
  negative = (1.0 - p_cancer)
  for attr in range(9):
    negative *= p_conditionals[attr][case[attr]][1]
  
  return positive / (positive + negative)

def main():
  database = read_database("wdbc.data")
  training_db = database[0: int(0.8 * len(database))]

  p_cancer, p_conditionals = train(training_db)

  # Evaluate precision of model
  successes = 0
  for case in database:
    probability = predict(case, p_cancer, p_conditionals)
    
    if probability > 0.5 and case[9] == 1:
      successes += 1
    elif probability < 0.5 and case[9] == 0:
      successes += 1
  
  print "Accuracy = ", float(successes) / len(database)


if __name__ == '__main__':
	main()

