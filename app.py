from random import randint
from flask import Flask, request
import logging

from opentelemetry import trace

# Acquire a tracer
tracer = trace.get_tracer("diceroller.tracer")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/rolldice")
def roll_dice():
    player = request.args.get('player', default=None, type=str)
    with tracer.start_as_current_span("roll") as rollspan:
        result = str(roll())
        rollspan.set_attribute("roll.value", result)
        if player:
            logger.warning("%s is rolling the dice: %s", player, result)
        else:
            logger.warning("Anonymous player is rolling the dice: %s", result)
        return result


def roll():
    return randint(1, 6)
