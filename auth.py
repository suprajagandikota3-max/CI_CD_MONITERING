import streamlit as st
import json
import hashlib

USER_FILE = "users.json"

def load_users():
    try:
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

def make_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    st.title("🔐 Wikipedia Chatbot Login")
    st.write("Please login or sign up to chat with me!")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.header("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            users = load_users()
            if email in users and users[email] == make_password(password):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Wrong email or password!")
    
    with tab2:
        st.header("Create Account")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            users = load_users()
            
            if new_email in users:
                st.error("Email already exists! Please login.")
            elif new_password != confirm_password:
                st.error("Passwords don't match!")
            elif len(new_password) < 4:
                st.error("Password must be at least 4 characters!")
            else:
                users[new_email] = make_password(new_password)
                save_users(users)
                st.success("Account created! Please login.")
