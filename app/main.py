from datetime import datetime
from typing import Text, Optional
import uvicorn
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from uuid import uuid5 as uuid

app = FastAPI()

clients = []


class Client(BaseModel):
    id: Optional[str]
    name: str
    surname: str
    description: Optional[Text]
    sing_up_date: datetime = datetime.now
    email: str
    active: bool = False


@app.get('/', status_code=status.HTTP_200_OK, tags=['index'])
def index():
    return {'This is the app index': 'For testing go to /docs'}


@app.get('/clients/get_all', status_code=status.HTTP_200_OK, tags=['Clients'])
def get_clients():
    return clients


@app.post('/clients/create', status_code=status.HTTP_201_CREATED, tags=['Clients'])
def create_client(client: Client):
    client.id = str(uuid())
    clients.append(client.dict())
    return clients[-1]


@app.get('/clients/{client_id}', status_code=status.HTTP_200_OK, tags=['Clients'])
def get_client(client_id: str):
    for client in clients:
        if client["id"] == client_id:
            return client
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")


@app.delete('/clients/delete/{client_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Clients'])
def delete_client(client_id: str):
    for i, client in enumerate(clients):
        if client["id"] == client_id:
            clients.pop(i)
            return {'Client deleted'}
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Client not found")


@app.put('/clients/updated/{client_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Clients'])
def update_client(client_id: str, updated_client: Client):
    for i, client in enumerate(clients):
        if client["id"] == client_id:
            clients[i]["name"] = updated_client.name
            clients[i]["surname"] = updated_client.surname
            clients[i]["email"] = updated_client.email
            return {'Client updated'}
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Client not found")


if __name__ == '__main__':
    uvicorn.run(app='main:app', port=9000, reload=True)
