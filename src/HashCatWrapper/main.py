from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def main():
    return {
        "This is the wrapper for the hashcat program. It finds the password for given hash and will return it."
    }
