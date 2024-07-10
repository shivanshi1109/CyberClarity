import os
import re
import streamlit as st
from langchain_community.llms import HuggingFaceEndpoint
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain.document_loaders import YoutubeLoader
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

load_dotenv()

os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# HuggingFaceEndpoints for summarization, translation, and Q&A
summarizer_repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
translator_repo_id="mistralai/Mistral-7B-Instruct-v0.2"
# translator_repo_id = "Telugu-LLM-Labs/Indic-gemma-7b-finetuned-sft-Navarasa-2.0"
qa_repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

summarizer = HuggingFaceEndpoint(repo_id=summarizer_repo_id, temperature=0.40, model_kwargs={'max_length': 8192}, max_new_tokens=4096)
translator = HuggingFaceEndpoint(repo_id=translator_repo_id, temperature=0.40, model_kwargs={'max_length': 8192}, max_new_tokens=4096)
qa_model = HuggingFaceEndpoint(repo_id=qa_repo_id, temperature=0.30, model_kwargs={'max_length': 8192}, max_new_tokens=4096)

# Prompts
summary_prompt = """As an expert summarizer, your job is to condense the following YouTube video transcript into a summary of 500-550 words. Focus on capturing the essential points and main ideas, leaving out any unnecessary details. Give the answer in points.

Example of a good summary:
---
Transcript: 
"In this video, we delve into the impact of climate change on global weather patterns. The speaker explains how rising temperatures are causing more frequent and severe weather events, including hurricanes, floods, and droughts. Scientific data is presented to show the correlation between human activities and climate change. The video also discusses possible solutions to mitigate these effects, such as reducing carbon emissions and adopting sustainable practices. Interviews with climate scientists provide further insights into the urgency of addressing climate change."

Summary:
"1. This video examines the effects of climate change on global weather patterns, highlighting the link between rising temperatures and increased frequency of extreme weather events. 
2. It presents scientific data demonstrating the human influence on climate change and discusses mitigation strategies like reducing carbon emissions and adopting sustainable practices. 
3. Insights from climate scientists underscore the urgency of taking action against climate change."
---

Here is the transcript you need to summarize:
"""

translation_prompt = """Translate the given text into conversational {language_needed}. Understand the text properly and correct any grammatical mistakes. Output the translated text in the form of points. Output the translated text. Here is the text you have to translate:\n{text}"""

# Prompt templates
summary_prompt_template = PromptTemplate(
    input_variables=["text"],
    template=summary_prompt + "\n{text}"
)

translation_prompt_template = PromptTemplate(
    input_variables=["text", "language_needed"],
    template=translation_prompt
)

qa_prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    Context:
    {context}

    Question:
    {question}
    """
)

# LLMChains
summary_chain = summary_prompt_template | summarizer
translation_chain = translation_prompt_template | translator
qa_chain = qa_prompt_template | qa_model

# Function to get YouTube transcript
def get_youtube_transcript(video_url):
    loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
    documents = loader.load()
    st.session_state.documents=documents
    transcript = documents[0].page_content
    return transcript

# Function to clean text
def clean_text(text):
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)
    cleaned_text = cleaned_text.strip()
    return cleaned_text

# Streamlit app interface
st.title("YouTube Video Summarizer, Translator, and Q&A")
st.write("Enter the URL of a YouTube video to get a summary, translation, and ask questions.")

# Input fields
video_url = st.text_input("YouTube URL")

if 'summary' not in st.session_state:
    st.session_state.summary = None

if st.button("Summarize"):
    if video_url:
        try:
            # Get transcript
            transcript = get_youtube_transcript(video_url)
            cleaned_transcript = clean_text(transcript)
            st.session_state.cleaned_transcript=cleaned_transcript

            # Summarize
            summary = summary_chain.invoke({"text": cleaned_transcript})
            st.session_state.summary = summary

            st.subheader("Summary:")
            st.write(st.session_state.summary)
        except Exception as e:
            st.write(f"An error occurred: {e}")
    else:
        st.write("Please enter a valid YouTube URL.")

if st.session_state.summary:
    language = st.selectbox("Select Translation Language", ["Kannada", "Hindi", "Telugu", "Tamil", "Sanskrit"])
    if st.button("Translate Summary"):
        # Translate
        tr_input={
            'text':st.session_state.summary,
            'language_needed':language
        }
        translation = translation_chain.invoke(tr_input)
        st.subheader(f"Translation in {language}:")
        st.write(translation)

    question = st.text_input("Ask a question about the video")
    question="Qn "+question
    if st.button("Get Answer"):
        # documents = [Document(page_content=chunk) for chunk in text_chunks]

        # Vectorize chunks for Q&A
        embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-l6-v2",
            multi_process=True,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        cdb = Chroma.from_documents(st.session_state.documents, embedding_model,persist_directory=None)
        qa = RetrievalQA.from_chain_type(llm=qa_model, chain_type="stuff", retriever=cdb.as_retriever(search_kwargs={"k": 1}))

        # Answer question
        answer = qa.invoke(question)

        st.subheader("Answer to your question:")
        st.write(f"Your Question:{answer['query']}\n\nAnswer:{answer['result']}")
        # st.write(f"Your Question: {answer['query']}\n\nAnswer: {answer['result']}")
