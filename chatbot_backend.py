# from langchain.llms.bedrock import Bedrock
from langchain_aws import ChatBedrock
from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

template = """
    ### Instruction: You're an AI assistant that is talking to a client and answer client question in English.
    
    Use only the chat history and the following information
    {context}
    to answer in a helpful manner to the question. If you don't know the answer -
    say that you don't know. Keep your replies short, compassionate and informative.
    
    {chat_history}
    ### Input: {question}
    ### Response:
    """.strip()

def getRetriever():
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id="QN6IZHRJG8",
        retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},
    )
    return retriever

def chatbot():
    llm = ChatBedrock(
        credentials_profile_name='default',
        model_id='anthropic.claude-3-haiku-20240307-v1:0',
        model_kwargs= {
            "temperature": 0.9,
            "top_p": 0.5,
            "max_tokens": 512
        }
    )
    # llm = ChatBedrock(
    #     credentials_profile_name='default',
    #     model_id='meta.llama2-70b-chat-v1',
    #     model_kwargs= {
    #         "temperature": 0.9,
    #         "top_p": 0.5,
    #         "max_gen_len": 512
    #     }
    # )
    return llm
#     return llm.predict(input_text)
# response = chatbot('what is temperature in bangkok ?')
# print(response)

def chat_memory():
    llm = chatbot()
    memory = ConversationBufferMemory(llm=llm,
                                      max_token_limit=512,
                                      memory_key="chat_history",
                                      human_prefix="### Input",
                                      ai_prefix="### Response",
                                      output_key="answer",
                                      return_messages=True)
    return memory

def chat_conversation(input_text, memory):
    prompt = PromptTemplate(
        input_variables=["context", "question", "chat_history"], template=template
    )

    llm = chatbot()
    retriever = getRetriever()

    # llm_conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
    # chat_reply = llm_conversation.predict(input=input_text)

    chain = ConversationalRetrievalChain.from_llm(llm,
                                                  chain_type="stuff",
                                                  retriever=retriever,
                                                  memory=memory,
                                                  combine_docs_chain_kwargs={"prompt": prompt},
                                                  return_source_documents=True,
                                                  verbose=True)

    chat_reply = chain(input_text)
    return chat_reply["answer"]