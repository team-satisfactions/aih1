import subprocess
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Spell(BaseModel):
    text: str


class DecodedSpell(BaseModel):
    spell: str
    command: str


reserved_decoded_spell: Optional[DecodedSpell] = None

allow_commands = ["eject", "ls", "echo"]


@app.post("/reserve-spell")
def receive_spell(spell: Spell) -> DecodedSpell:
    global reserved_decoded_spell
    command = f"chant -d {spell.text}"
    decoded_command = subprocess.run(command, capture_output=True, text=True, shell=True).stdout.replace("\n", "")

    run_command = decoded_command.split(" ")[0]
    if run_command not in allow_commands:
        print(f"not allow command: {spell.text} => {run_command}")
        raise HTTPException(status_code=400, detail=f"not allow command: {spell.text} => {run_command}")

    reserved_decoded_spell = DecodedSpell(spell=spell.text, command=decoded_command)

    return reserved_decoded_spell


@app.get("/reserved-spell")
def reserved_spell() -> DecodedSpell:
    global reserved_decoded_spell
    if reserved_decoded_spell is None:
        raise HTTPException(status_code=400, detail="not reserved spell")

    return reserved_decoded_spell


@app.post("/chant-spell")
def chant_spell() -> str:
    global reserved_decoded_spell
    if reserved_decoded_spell is None:
        raise HTTPException(status_code=400, detail="not reserved spell")

    # コマンドを実行する
    runned_spell = reserved_decoded_spell
    reserved_decoded_spell = None
    result = subprocess.run(runned_spell.command, capture_output=True, text=True, shell=True).stdout

    return result
