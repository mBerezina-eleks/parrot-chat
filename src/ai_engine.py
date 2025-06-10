import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from src.rag_engine import get_similarity
from src.examples import examplesMultiplier, examplesPII
from src.constants import openai_api_key, azure_endpoint, openai_api_type, deployment_name, openai_api_version

model = AzureChatOpenAI(temperature=0.7, openai_api_key=openai_api_key, openai_api_type=openai_api_type, deployment_name=deployment_name, openai_api_version=openai_api_version, azure_endpoint=azure_endpoint)

def generate_few_shot_examples(examples, question):
    example_prompt = PromptTemplate(
        input_variables=["question", "answer"], template="Q: {question}\nA: {answer}"
    )
    
    few_shot_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix="Q: {user_question}",
        input_variables=["user_question"],
    )
    return few_shot_prompt.format(user_question=question)
  
def generate_response(question):
    rephrase_prompt = f"""
        You are a helpful AI that rewrites user questions for better semantic search.
        Original question: "{question}"
        Rewrite this query to be short and precise for vector similarity search:
        """
    rephrased = model.invoke(rephrase_prompt).content.strip()
    context = get_similarity(rephrased)
    few_shots = generate_few_shot_examples(examplesMultiplier, question)
    chat_history = "\n".join(
        [f"User: {q}\nAssistant: {a}" for q, a in st.session_state.chat_history]
    )

    template = """
        You MUST answer in short and precise sentences.
        You MUST answer without any additional information.
        You are a helpful assistant. Answer the user's question using the context and chat history below.
        1. If the context contains relevant information, use it.
        2. If the context is not enough, check the chat history.
        3. If neither the context nor history help, answer based on your own knowledge.
          
        Chat History: {chat_history}
        Context: {context}
        Examples: {few_shots}
        User Question: {question}
        """

    PROMPT = PromptTemplate(
        template=template,
        input_variables=["context", "question", "few_shots", "chat_history"]
    )

    formatted_prompt = PROMPT.format(
        context=context, question=question, few_shots=few_shots, chat_history=chat_history
    )
      
    res = model.invoke(formatted_prompt)
    st.session_state.chat_history.append((question, res.content))
    return res.content

def detect_pii(text):
    few_shots = generate_few_shot_examples(examplesPII, text);
    
    prompt = f"""
    You are a PII auditor. Analyze the text and extract ONLY actual instances of Personally Identifiable Information (PII) such as:

    - Full names
    - Email addresses
    - Phone numbers
    - Passport numbers
    - Full physical addresses
    - Dates of birth
    - Identity card numbers
    - IDs
    - Codes

    If it contains PII, list the types and examples. If not, say "No PII detected."
    You MUST include only summary of PII types and examples that are found in the text.
    You MUST mask all PII entities
    
    **Masking rule:**
    - Replace each PII entity with 🦜 symbols
    - Keep the last 2 characters (letters or digits) of each PII entity visible
    - Preserve original punctuation and formatting

    Examples:
    {few_shots}
    Text:
    {text}
    """
    response = model.invoke(prompt)
    return response.content.strip()