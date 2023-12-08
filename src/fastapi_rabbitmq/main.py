from fastapi import FastAPI, Request
from datetime import datetime

import json
app = FastAPI()


@app.get("/")
def index():
    return "Hello, world"

@app.get("/json")
def some_func():
    return {
        "some_json": "Some Json"
    }


#
# if __name__ == "__main__":
#     app.run(debug=True)
