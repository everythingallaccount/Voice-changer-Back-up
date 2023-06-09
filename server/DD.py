import multiprocessing
import logging
logger = multiprocessing.log_to_stderr(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(processName)-10s] [%(threadName)s] %(levelname)-8s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
# logger.addHandler(handler)

logger.error("testtttttttttttttttttttttttttttttttttt")




from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
