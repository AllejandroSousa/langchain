from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_transformers import DoctranTextTranslator
from langchain_core.documents import Document
import os

# Configuração do FastAPI
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Configuração das variáveis de ambiente
os.environ["OPENAI_API_KEY"] = "..."

# Configuração do LangChain
system_template = "Translate the following sentence to Portuguese: {sentence}"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{sentence}')
])


@app.get('/')
async def read_root():
    return {'message': 'Home page'}

@app.get('/translate')
async def translate(text: str = Query(..., description="Text to be translated")):
    try:
        print('a')
        documents = [Document(page_content=text)]
        print('b')
        qa_translator = DoctranTextTranslator(language="portuguese")
        print('c')
        translated_document = qa_translator.transform_documents(documents)
        print('d')
        test = translated_document[0].page_content
        print('e')
        return {'output': test}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
