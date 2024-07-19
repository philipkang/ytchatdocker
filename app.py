import streamlit as st
from utilities import get_video_id_from_url, get_transcript, generate_prompt_from_transcript
from bedrock import bedrock_chain

# Initialize the Bedrock chain and conversation state outside the main function
if 'conversation' not in st.session_state:
    st.session_state.conversation = bedrock_chain()

# Initialize the state variables
if 'video_processed' not in st.session_state:
    st.session_state.video_processed = False

if 'awaiting_response' not in st.session_state:
    st.session_state.awaiting_response = False

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

def main():
    st.title("YouTube Digest")

    # Input YouTube video URL
    youtube_url = st.text_input("Enter YouTube Video URL")

    if youtube_url and not st.session_state.video_processed:
        try:
            # Get video ID from URL
            video_id = get_video_id_from_url(youtube_url)

            # Get transcript for the video
            transcript = get_transcript(video_id)

            # Generate prompt from the transcript
            prompt = generate_prompt_from_transcript(transcript)

            # Summarize the transcript
            summary = st.session_state.conversation({"input": prompt})

            # Extract the summary text from the response
            summarized_text = summary.get("response", "Summary not available.")

            # Store the summary and mark the video as processed
            st.session_state.summarized_text = summarized_text
            st.session_state.video_processed = True
        except Exception as e:
            st.error(f"Error processing video: {e}")

    if st.session_state.video_processed:
        # Display the summarized text
        st.subheader("Summary")
        st.write(st.session_state.summarized_text)

        # Display conversation history
        if st.session_state.conversation_history:
            st.subheader("Conversation History")
            for i, (question, answer) in enumerate(st.session_state.conversation_history):
                st.write(f"**Q{i+1}:** {question}")
                st.write(f"**A{i+1}:** {answer}")

        # User input for chat
        user_input = st.text_input("Ask a question or continue the conversation", key="user_input")

        if st.button("Send"):
            if user_input:
                st.session_state.awaiting_response = True
                try:
                    # Get the response from Bedrock model
                    response = st.session_state.conversation({"input": user_input})

                    # Display the response
                    if "response" in response:
                        st.session_state.conversation_history.append((user_input, response["response"]))
                    else:
                        st.error("Error: Chat response does not contain 'response' key")
                except Exception as e:
                    st.error(f"Error during conversation: {e}")
                finally:
                    # Allow the next question
                    st.session_state.awaiting_response = False

                    # Reset the input field by clearing the key
                    st.session_state.pop("user_input", None)
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
