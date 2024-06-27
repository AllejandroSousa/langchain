from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os


# Configuração das variáveis de ambiente
os.environ["OPENAI_API_KEY"] = "insert your key here"
        
llm = ChatOpenAI()

# Configuração do FastAPI
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server",
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

@app.get('/')
async def read_root():
    return {'message': 'Home page'}

@app.get('/translate')
async def translate(text: str = Query(..., description="Text to be translated")):
    try:
        prompt = ChatPromptTemplate.from_messages([
        ("system", "Translate the following sentence to Portuguese:"),
        ("user", "{input}")
        ])

        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        final = chain.invoke({"input" : text})

        return {'output': final}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
