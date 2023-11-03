import subprocess
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


class Spell(BaseModel):
    text: str


class DecodedSpell(BaseModel):
    spell: str
    command: str


reserved_decoded_spell: Optional[DecodedSpell] = None

allow_commands = ["eject"]


@app.post("/reserve-spell")
def receive_spell(spell: Spell) -> Optional[DecodedSpell]:
    command = f"PATH=$PATH:/Users/goya/.nvm/versions/node/v21.0.0/bin /Users/goya/.nvm/versions/node/v21.0.0/bin/chant -d {spell.text}"
    decoded_command = subprocess.run(command, capture_output=True, text=True, shell=True).stdout.replace("\n", "")

    run_command = decoded_command.split(" ")[0]
    if run_command not in allow_commands:
        return None

    reserved_decoded_spell = DecodedSpell(spell=spell.text, command=decoded_command)

    return reserved_decoded_spell


@app.get("/reserved-spell")
def read_item() -> Optional[DecodedSpell]:
    if reserved_decoded_spell is None:
        return None

    return reserved_decoded_spell


@app.post("/chant-spell")
def read_item() -> Optional[DecodedSpell]:
    if reserved_decoded_spell is None:
        return None

    # コマンドを実行する

    return reserved_decoded_spell
