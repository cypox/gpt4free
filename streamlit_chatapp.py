import streamlit as st
import g4f


providers = [
    #"Aichat",
    "ChatBase",
    #"GeekGpt",
    #"You",
    "Yqcloud",
    "Liaobots",
    "Phind",
    #"Raycast",
    #"Aivvm",
    #"GptChatly",
    #"Lockchat",
    #"Myshell",
    "Bard",
    "Bing",
    "GptGo",
]

models = [
    "gpt-3.5-turbo",
    "palm",
    "gpt-4",
]


title_placeholder = st.empty()
title_placeholder.title("")

if "title_generated" not in st.session_state:
    st.session_state["title_generated"] = False

if "openai_model" not in st.session_state:
    st.session_state["model"] = "gpt-3.5-turbo"

if "provider" not in st.session_state:
    st.session_state["provider"] = None

if "stream" not in st.session_state:
    st.session_state["stream"] = True

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def double_reset():
    reset_session()
    reset_session()
    first = True

def reset_session():
    st.session_state.messages.clear()

with st.sidebar:
    provider_placeholder = st.empty()
    selected_provider = provider_placeholder.selectbox("Select a provider", providers, index=len(providers)-1)
    st.session_state.provider = getattr(g4f.Provider, selected_provider)

    stream_placeholder = st.empty()
    selected_model = stream_placeholder.selectbox("Select a model", models, index=len(models)-1)
    st.session_state.model = selected_model

    if not st.session_state.title_generated:
        title_placeholder.title("Using " + selected_model + " with " + st.session_state.provider.__name__)

    model_placeholder = st.empty()
    use_streaming = model_placeholder.radio("Use streaming for answers?", ["Yes", "No"])
    st.session_state.stream = use_streaming == "Yes"

    st.button("Reset", on_click=double_reset)

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        max_len = 4096
        history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        trimmed_history = []
        for entry in reversed(history):
            max_len -= len(entry["content"])
            if max_len > 0:
                trimmed_history.insert(0, entry)
        history = trimmed_history
        for response in g4f.ChatCompletion.create(
            model=st.session_state.model,
            messages=history,
            provider=st.session_state.provider,
            stream=st.session_state.stream,
        ):
            full_response += response
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    if not st.session_state.title_generated:
        content = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        content.append({"role": "user", "content": "Can you generate a four or five word title for this conversation?"})
        title = g4f.ChatCompletion.create(
            model=st.session_state.model,
            messages=content,
            provider=st.session_state.provider,
            stream=False,
        )
        if "**" in title:
            title = title[title.find("**")+2:title.rfind("**")]
        if "\"" in title:
            title = title.strip("\"")
        title_placeholder.title(title.strip())
        st.session_state.title_generated = True
