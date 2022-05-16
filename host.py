from typing import List
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
from crontab import CronTab


# Cron Tab instance
cron = CronTab(user="panda")

# FastAPI instance
app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Host Endpoint
@app.post("/host/{duration}/{path}")
async def host(duration: str, path: str, file: List[UploadFile]):
    for f in file:
        async with aiofiles.open(f"content/{path}/{f.filename}", "wb") as out:
            content = await f.read()
            await out.write(content)

    job = cron.new(command=f"python3 /home/panda/kodash/purge.py {path}")

    if duration.endswith("h"):
        duration = duration[:-1]
        job.hour.on(duration)
    else:
        duration = duration[:-1]
        job.day.on(duration)

    return {
        "status": "success",
    }
