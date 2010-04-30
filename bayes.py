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
  p_values = {}

  for attr in range(9):
    p_conditionals[attr] = {}
    p_values[attr] = {}
  
    for value in range(1, 11):
      p_conditionals[attr][value] = get_probability(database, [(attr, value)], conditions=[(9, 1)])
      p_values[attr][value] = get_probability(database, [(attr, value)])

  return p_cancer, p_conditionals, p_values

def predict(case, p_cancer, p_conditionals, p_values):
  probability = p_cancer
  
  for attr in range(9):
    probability *= p_conditionals[attr][case[attr]]
  
  p_effect = 1.0
  for attr in range(9):
    p_effect *= (1.0 / 10) if p_values[attr][case[attr]] == 0 else p_values[attr][case[attr]]
  
  return probability / p_effect

def main():
  database = read_database("wdbc.data")
  training_db = database[0: int(0.8 * len(database))]

  p_cancer, p_conditionals, p_values = train(training_db)

  # Evaluate precision of model
  successes = 0
  for case in database:
    probability = predict(case, p_cancer, p_conditionals, p_values)
    
    if probability > 0.5 and case[9] == 1:
      successes += 1
    elif probability < 0.5 and case[9] == 0:
      successes += 1
  
  print "Accuracy = ", float(successes) / len(database)


if __name__ == '__main__':
	main()

