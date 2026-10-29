from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI(title="Contact Management System")
db = {}

class Contact(BaseModel):
    name: str
    email: str
    phone_number: str
    company: Optional[str] = None

class ContactOut(Contact):
    id: str

@app.post("/contacts/", response_model=ContactOut)
def create_contact(contact: Contact):
    cid = str(uuid4())
    db[cid] = {"id": cid, **contact.model_dump()}
    return db[cid]

@app.get("/contacts/", response_model=List[ContactOut])
def get_contacts():
    return list(db.values())

@app.put("/contacts/{cid}", response_model=ContactOut)
def update_contact(cid: str, contact: Contact):
    if cid not in db: raise HTTPException(status_code=404, detail="Not found")
    db[cid] = {"id": cid, **contact.model_dump()}
    return db[cid]

@app.delete("/contacts/{cid}")
def delete_contact(cid: str):
    if cid not in db: raise HTTPException(status_code=404, detail="Not found")
    del db[cid]
    return {"message": "Contact deleted"}