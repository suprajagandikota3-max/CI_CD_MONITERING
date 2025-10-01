import streamlit as st
import wikipedia

# Configure Wikipedia
wikipedia.set_lang("en")

st.set_page_config(
    page_title="Wikipedia Chatbot",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Wikipedia Chatbot")
st.markdown("Ask me anything and I'll search Wikipedia for you!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Hello! I'm your Wikipedia assistant. Ask me anything and I'll search Wikipedia for you!"}
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
