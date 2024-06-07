from fastapi import FastAPI, HTTPException, responses
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from shortcuts import dy_parser

class ParsingResult(BaseModel):
    status_code: int
    urls: list[str]

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(dy_parser.ParsingError)
async def unicorn_exception_handler(request, exc: dy_parser.ParsingError):
    return responses.JSONResponse(
        status_code=500,
        content={
            "status_code": 500,
            "message": f"ParsingError: {exc.msg}",
            "input": exc.input
        },
    )

@app.get("/")
async def root():
    return responses.FileResponse('static/index.html')

@app.get('/dy_parse', response_model=ParsingResult)
async def dy_parse(url: str):
    urls = dy_parser.parse_url(url)
    return ParsingResult(status_code=200, urls=urls)
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=80
    )