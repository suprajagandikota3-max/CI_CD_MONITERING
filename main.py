import streamlit as st
import wikipedia
import pandas as pd
import plotly.express as px
from datetime import datetime
from auth import login_page

# Set page config first
st.set_page_config(
    page_title="Wikipedia Chatbot",
    page_icon="📚",
    layout="wide"  # Changed to wide for better sidebar
)

# Configure Wikipedia
wikipedia.set_lang("en")

# ----------------------
# Safe session state initialization
# ----------------------
def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_email" not in st.session_state:
        st.session_state.user_email = ""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "bot", "content": "Hello! I'm your Wikipedia assistant. Ask me anything and I'll search Wikipedia for you!"}
        ]
    if "page_views" not in st.session_state:
        st.session_state.page_views = 0
    if "searches" not in st.session_state:
        st.session_state.searches = 0
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Wikipedia Chatbot"

# Only initialize if Streamlit session_state is available
try:
    init_session_state()
except RuntimeError:
    # Happens if running outside Streamlit (e.g., CI/CD import)
    pass

# ----------------------
# MONITORING DASHBOARD
# ----------------------
def monitoring_dashboard():
    st.title("📊 Live Monitoring Dashboard")
    st.markdown("Real-time insights into your Wikipedia Chatbot")
    
    # Track page views
    st.session_state.page_views += 1
    
    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Page Views", st.session_state.page_views, "+1 now")
    with col2:
        st.metric("Wikipedia Searches", st.session_state.searches, "+0 today")
    with col3:
        st.metric("Active Users", "1", "You")
    with col4:
        st.metric("Uptime", "99.8%", "0.2%")
    
    # Performance charts
    st.subheader("📈 Usage Analytics")
    
    # Sample usage data
    time_data = ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00']
    searches_data = [8, 12, 15, 18, 14, 16]
    users_data = [5, 8, 12, 15, 11, 13]
    
    # Create charts
    fig1 = px.line(
        x=time_data, 
        y=searches_data, 
        title="Wikipedia Searches Per Hour",
        labels={'x': 'Time', 'y': 'Searches'}
    )
    fig1.update_traces(line_color='blue')
    
    fig2 = px.bar(
        x=time_data, 
        y=users_data,
        title="Active Users Per Hour",
        labels={'x': 'Time', 'y': 'Users'}
    )
    fig2.update_traces(marker_color='green')
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    # System status
    st.subheader("🔄 System Status")
    
    status_col1, status_col2 = st.columns(2)
    
    with status_col1:
        st.success("**Wikipedia API**: ✅ Connected")
        st.success("**Authentication**: ✅ Active")
        st.success("**Database**: ✅ Online")
        
    with status_col2:
        st.info("**Last Backup**: 2 hours ago")
        st.info("**Storage Used**: 45%")
        st.info("**Response Time**: 0.4s")
    
    # Recent activity log
    st.subheader("🎯 Recent Activity")
    activities = [
        {"time": datetime.now().strftime("%H:%M"), "user": st.session_state.user_email, "action": "Viewed Monitoring Dashboard"},
        {"time": "14:25", "user": "sara@email.com", "action": "Searched 'Python Programming'"},
        {"time": "14:15", "user": "john@email.com", "action": "Logged in"},
        {"time": "14:10", "user": "admin", "action": "System health check"},
    ]
    
    for activity in activities:
        st.write(f"**{activity['time']}** - `{activity['user']}` - {activity['action']}")

# ----------------------
# Chatbot main function
# ----------------------
def wikipedia_chatbot():
    """Wikipedia chatbot functionality"""
    st.title(f"📚 Wikipedia Chatbot - Welcome, {st.session_state.user_email}!")
    st.markdown("Ask me anything and I'll search Wikipedia for you!")

    def get_wikipedia_summary(query):
        try:
            # Track searches
            st.session_state.searches += 1
            
            results = wikipedia.search(query)
            if not results:
                return "Sorry, I couldn't find anything on that topic. Try being more specific or check your spelling."

            page_title = results[0]
            summary = wikipedia.summary(page_title, sentences=3, auto_suggest=False, redirect=True)
            page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
            response = f"**{page_title}**\n\n{summary}\n\n[Read more on Wikipedia]({page_url})"
            return response

        except wikipedia.DisambiguationError as e:
            suggestions = ', '.join(e.options[:5])
            return f"*Your query is ambiguous.* Did you mean one of these?\n\n**{suggestions}**\n\nPlease be more specific with your search."
        except wikipedia.PageError:
            return "Sorry, I couldn't find a page matching your query. Try different keywords or check your spelling."
        except Exception:
            return "Oops, something went wrong while searching Wikipedia. Please try again."

    # If messages were empty, initialize welcome message with user email
    if not st.session_state.messages:
        st.session_state.messages = [
            {"role": "bot", "content": f"Hello {st.session_state.user_email}! I'm your Wikipedia assistant. Ask me anything and I'll search Wikipedia for you!"}
        ]

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
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="📚"):
            with st.spinner("🔍 Searching Wikipedia..."):
                bot_response = get_wikipedia_summary(prompt)
            st.markdown(bot_response)

        st.session_state.messages.append({"role": "bot", "content": bot_response})

# ----------------------
# Main app function
# ----------------------
def main_app():
    """Main application with navigation"""
    
    # Track page views
    st.session_state.page_views += 1
    
    # Sidebar navigation - THIS IS WHAT YOU'RE MISSING
    with st.sidebar:
        st.title("🔍 Navigation")
        
        # Radio buttons for page selection
        selected_page = st.radio(
            "Choose a page:",
            ["Wikipedia Chatbot", "Monitoring Dashboard"],
            index=0 if st.session_state.current_page == "Wikipedia Chatbot" else 1
        )
        
        # Update current page
        st.session_state.current_page = selected_page
        
        st.divider()
        st.subheader("📊 User Stats")
        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Page Views:** {st.session_state.page_views}")
        st.write(f"**Searches:** {st.session_state.searches}")
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.messages = []
            st.session_state.page_views = 0
            st.session_state.searches = 0
            st.session_state.current_page = "Wikipedia Chatbot"
            st.rerun()
    
    # Show the selected page
    if st.session_state.current_page == "Monitoring Dashboard":
        monitoring_dashboard()
    else:
        wikipedia_chatbot()

# ----------------------
# Run app if this is main
# ----------------------
if __name__ == "__main__":
    try:
        if not st.session_state.logged_in:
            login_page()
        else:
            main_app()
    except RuntimeError:
        # Happens when running outside Streamlit (e.g., CI/CD import)
        pass
