# -*- coding: utf-8 -*-
"""app

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19ETZZ_HcBG2OADA0kFAhv2b4ZUkw0GzM
"""

import numpy as np
import pandas as pd
import flask
from flask import Flask, render_template, request, redirect, url_for
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
#from numba.cpython.hashing import msg


app = flask.Flask(__name__, template_folder='Templates')

#tour_tfidf = CountVectorizer(stop_words='english')
# computing TF-IDF matrix required for calculating cosine similarity
#tour_matrix = tour_tfidf.fit_transform(tour_desc['Keywords'].values.astype('U'))
df = pd.read_csv('travel.csv')            
tour_tfidf = CountVectorizer(stop_words='english')
tour_matrix = tour_tfidf.fit_transform(df['soup'])
df = df.reset_index()
indices = pd.Series(df.index, index=df['Title'])
all_titles = [df['Title'][i] for i in range(len(df['Title']))]

def get_recommendations(title):
  cosine_sim = cosine_similarity(tour_matrix, tour_matrix)
  idx = indices[title]
  sim_scores = list(enumerate(cosine_sim[idx]))
  sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
  sim_scores = sim_scores[1:11]
  tour_indices = [i[0] for i in sim_scores]
  tours = df.iloc[tour_indices][['Title','Days', 'Price','Score','Location']].sort_values('Score', ascending = False)
  return tours



# Set up the main route
@app.route('/', methods=['GET', 'POST'])

def main():
  if flask.request.method == 'GET':
    return(flask.render_template('home.html')) 
  if flask.request.method == 'POST':
    m_name = flask.request.form['tour_name']
    m_name = m_name.title()
    if m_name not in all_titles:
      return(flask.render_template('negative.html', name=m_name))
    else:
      result = get_recommendations(m_name)
      names = []
      Days=[]
      Price = []
      Score= []
      Location = []
      for i in range(len(result)):
        names.append(result.iloc[i][0])
        Days.append(result.iloc[i][1])
        Price.append(result.iloc[i][2])
        Score.append(result.iloc[i][3])
        Location.append(result.iloc[i][4])

      return flask.render_template('positive.html',Tour_names=names,Tour_Days=Days,Tour_Price=Price,Tour_Score=Score,Tour_Location=Location, search_name=m_name)


@app.route("/home" , methods = ["GET" , "POST"])
def home():
  return render_template("home.html")

@app.route("/about" , methods = ["GET" , "POST"])
def about():
  return render_template("about.html")


@app.route("/Signup" , methods = ["GET" , "POST"])
def Signup():
  msg=None
  if(request.method == "POST"):
    if(request.form["username"]!="" and request.form["password"]!=""):
      email=request.form["email"]
      username=request.form["username"]
      password=request.form["password"]
      conn=sqlite3.connect("mytest.db")
      c=conn.cursor()
      #c.execute('CREATE TABLE User (email TEXT, username TEXT, password TEXT)')
      c.execute("INSERT INTO User VALUES('"+email+"' ,'"+username+"' ,'"+password+"') ")
      msg="Your Account is created"
      conn.commit()
      conn.close()
    else:
      msg="Something went wrong"
  return render_template("Signup.html", msg=msg) 

@app.route("/login" , methods = ["GET" , "POST"])
def loginn():
  r=""
  msg=None
  if(request.method =="POST"):
      username=request.form["username"]
      password=request.form["password"]
      conn=sqlite3.connect("mytest.db")
      c=conn.cursor()
      c.execute("SELECt * FROM User WHERE username = '"+username+"' and password = '"+password+"' ")
      r = c.fetchall()
      for i in r:
        if(username == i[0] and password == i[1]):
          session["loginid"] = True
          session["username"] = username
          return redirect(url_for("index"))
          conn.commit()
          conn.close()
        else:
          msg = "Please enter valid username and password"
  return render_template("login.html", msg=msg)
   

@app.route("/index")
def index():
  return render_template("index.html") 

  


  
if __name__ == '__main__':
  app.run(debug=True)
