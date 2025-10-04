import streamlit as st
import wikipedia
from auth import login_page

# Configure Wikipedia
wikipedia.set_lang("en")

# Check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

def main_chatbot():
    """This is your chatbot that shows after login"""
    
    st.set_page_config(
        page_title="Wikipedia Chatbot",
        page_icon="📚",
        layout="centered"
    )

    st.title(f"📚 Wikipedia Chatbot - Welcome, {st.session_state.user_email}!")
    st.markdown("Ask me anything and I'll search Wikipedia for you!")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "bot", "content": f"Hello {st.session_state.user_email}! I'm your Wikipedia assistant. Ask me anything and I'll search Wikipedia for you!"}
        ]

    def get_wikipedia_summary(query):
        try:
            # Search for pages matching the query
            results = wikipedia.search(query)
            if not results:
                return "Sorry, I couldn't find anything on that topic. Try being more specific or check your spelling."

            # Get summary of the top result
            page_title = results[0]
            summary = wikipedia.summary(page_title, sentences=3, auto_suggest=False, redirect=True)
            
            # Add page title and link
            page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
            response = f"{page_title}\n\n{summary}\n\n[Read more on Wikipedia]({page_url})"
            return response
            
        except wikipedia.DisambiguationError as e:
            suggestions = ', '.join(e.options[:5])
            return f"*Your query is ambiguous.* Did you mean one of these?\n\n{suggestions}\n\nPlease be more specific with your search."
        except wikipedia.PageError:
            return "Sorry, I couldn't find a page matching your query. Try different keywords or check your spelling."
        except Exception as e:
            return "Oops, something went wrong while searching Wikipedia. Please try again."

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar="📚"):
                st.markdown(message["content"])

    # User input at bottom
    if prompt := st.chat_input("Ask me anything..."):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get Wikipedia response
        with st.chat_message("assistant", avatar="📚"):
            with st.spinner("🔍 Searching Wikipedia..."):
                bot_response = get_wikipedia_summary(prompt)
            st.markdown(bot_response)
        
        st.session_state.messages.append({"role": "bot", "content": bot_response})
    
    # Logout button in sidebar
    with st.sidebar:
        st.write(f"Logged in as: *{st.session_state.user_email}*")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.messages = []  # Clear chat history
            st.rerun()

# Show login page or main chatbot
if not st.session_state.logged_in:
    login_page()
else:
    main_chatbot()
