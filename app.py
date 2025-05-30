from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import streamlit as st
import asyncio
import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


if not gemini_api_key:
    raise ValueError('GEMINI_API_KEY is not set. Please ensure it defin ein your env file.')


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


translator = Agent(
    name='Language Translator',
    instructions="""
You are a professional language translation agent.
• Always auto-detect the source language unless explicitly told.
• Translate the input text into the target language specified by the user.
• When given multiple sentences or paragraphs, translate them in order, keeping paragraph breaks.
• If asked to translate into multiple languages, output each version clearly labeled.
• If only give the text and not asked for translate into any language so translate the text into english
"""
)
st.set_page_config(page_title='📖 Languages Translator')
st.title('LANGUAGE TRANSLATOR')
st.write('Enter you text to translate into any Language')
st_input = st.text_area('Input your text here', height=75)

async def translate(user_text):
    try:
        response = await Runner.run(
            translator,
            input=user_text,
            run_config=config
        )
        return response.final_output
    except Exception as e :
        return f'Error: {e}' 

if st.button('Translate'):
    if st_input.strip():
        translation = asyncio.run(translate(st_input))
        if 'Error' in translation:
            st.error(translation)
        else:
            st.subheader("Translation of your text:")
            st.success(translation)

st.write("Created by [Abdul Wasay] (www.linkedin.com/in/abdul-wasay-a022422ba/)")
        
   