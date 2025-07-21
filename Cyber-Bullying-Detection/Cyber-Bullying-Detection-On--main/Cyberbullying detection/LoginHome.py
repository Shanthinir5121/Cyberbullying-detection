
import streamlit as st

from PIL import Image
# import pandas as pd
import numpy as np
import re
import string
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import RegexpTokenizer
from nltk import PorterStemmer, WordNetLemmatizer

import pickle
from functions import *


import base64

from datetime import datetime
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3 
conn = sqlite3.connect('comments.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data

# conn = sqlite3.connect('comments.db')
# c = conn.cursor()

# Create a table to store comments if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS comments
             (name text, comment text, date text)''')

# Define a function to add a comment to the database
def add_comment(name, comment):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO comments VALUES (?, ?, ?)", (name, comment, date))
#     c.execute("DELETE FROM comments")
    conn.commit()

# Define a function to get all the comments from the database
def get_comments():
    c.execute("SELECT * FROM comments order by date desc")
    rows = c.fetchall()
    return rows


def check_comment(comment):
    prediction = custom_input_prediction(comment)
    if prediction == "not bully":
        return False
    else:
        return True
    return False

# def detect():
#     st.subheader("Cyberbullying Detection")
#     # name = st.text_input("Name")
#     comment = st.text_area("Comment")
#     if st.button("Detect"):
#         if check_comment(comment):
#             st.error("This comment is bullying and cannot be posted.")
#         else:
#             st.success("This comment is not bullying")
#     return st.error("Enter comment")
def prevent(username):
#     global username
    user_email = st.session_state.get('user_email')
    if user_email:
        st.title("Cyberbullying Prevention")

#         name = st.text_input("Name")
        st.text_input("User email", value=username, disabled=True)
        comment = st.text_area("Comment")

        if st.button("Post Comment"):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if check_comment(comment):
                st.error("This comment is bullying and cannot be posted.")
            else:
                add_comment(username, comment)

            # Get all the comments from the database and display them
        comments = get_comments()
        for row in comments:
    #         st.write(f"Posted on {row[2]} by {row[0]} :")
#     style={"color": "white"})
            st.write(f"@{row[0]} on {row[2]}")
            st.write(f"{row[1]}")
    else:
        st.warning('You need to login first.')
            
            
            
def detect():
    user_email = st.session_state.get('user_email')
    if user_email:
        st.write(f'Welcome, {user_email}!')
        st.title("Cyberbullying Detection")
        # name = st.text_input("Name")
        comment = st.text_area("Comment")

        if st.button("Detect"):
        #     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if check_comment(comment):
                st.error("This comment is bullying.")
            else:
                st.success("This comment is not bullying.")
    else:
        st.warning('You need to login first.')
        



def main():

    st.set_page_config(page_title="Detection and Prevention Of Cyber Bullyin", page_icon=":rocket:", layout="wide", initial_sidebar_state="expanded")
    
#     data_testid="stAppViewContainer"
    pg_bg="""
    <style>
    [data-testid="stAppViewContainer"]{
    background: linear-gradient(45deg, gray, transparent)
    },
    [data-testid="stSidebar"]{
    background: #e6e6fa
    }
    
    </style>
    """
    st.markdown(pg_bg,unsafe_allow_html=True)
#     main_bg = "bg.jpg"
#     main_bg_ext = "jpg"

#     side_bg = "bg.jpg"
#     side_bg_ext = "jpg"

#     st.markdown(
#     """
#     <style>
#     .reportview-container {
#         background: url("images/bg.jpg")
#     }
#    .sidebar .sidebar-content {
#         background: url("images/bg.jpg")
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

#     st.markdown(
#         f"""
#         <style>
#         .reportview-container {{
#             background: url(data:images/{main_bg_ext};base64,{base64.b64encode(open('images/bg.jpg', "rb").read()).decode()})
#         }}
  
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
    
    
#     """Simple Login App"""


    st.title("Detection and Prevention Of Cyberbullying")

    menu = ["Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)

    
    if choice == "Login":
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("Let's Stop Cyberbullying")
        st.markdown("<hr>", unsafe_allow_html=True)
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')

        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                task = st.selectbox("Task",["Cyberbullying Detection","Cyberbullying Prevention"])
                st.session_state['user_email'] = username
    
                if task == "Cyberbullying Detection":
                    detect()


                elif task == "Cyberbullying Prevention":
                    prevent(username)
#                     st.subheader("Cyberbullying Prevention")
#                     user_result = view_all_users()
#                     clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
#                     st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")



    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")



if __name__ == '__main__':
    main()





# conn = sqlite3.connect('comments.db')
# c = conn.cursor()

# # Create a table to store comments if it doesn't exist
# c.execute('''CREATE TABLE IF NOT EXISTS user
#              (name text, comment text, date text)''')
# st.title("Cyberbullying")

# Authentication

# choice = st.sidebar.selectbox('Login/Signup',['Login','Sign up'])


# choice = st.selectbox('Login/Signup',['Login','Sign up'])


# email = st.text_input('Please enter your email address')
# password = st.text_input('Please enter your password',type = 'password')

# if choice == 'Sign up':
#     handle =st.sidebar.text_input('Please input your app handle name',value = 'Default')
#     submit = st.sidebar.button('Create my account')
    
#     if submit:
#         user = auth.create_user_with_email_and_password(email,password)
#         st.success('Your account is created successfully!')
#         st.balloons()
        
#         # Sign in
#         user = auth.sign_in_with_email_and_password(email,password)
#         db.child(user['localId']).child("Handle").set(handle)
#         db.child(user['localId']).child("ID").set(localId)
#         st.title('Welcome' + handle)
#         st.info('Login via login drop down')
# if choice == 'Login':
#     login = st.sidebar.checkbox('Login')
#     if login:
#         user = auth.sign_in_with_email_and_password(email,password)
#         st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
#         bio = st.radio('Jump to',['Home','Workplace Feeds', 'Settings'])