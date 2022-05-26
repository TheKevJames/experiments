from typing import Dict

import fastapi


app = fastapi.FastAPI()


@app.get('/')
async def root() -> Dict[str, str]:
    return {'message': 'Hello World!'}
