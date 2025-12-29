from random import randint
from flask import Flask, request
import logging

from opentelemetry import trace, metrics

# Acquire a tracer
tracer = trace.get_tracer("diceroller.tracer")
meter = metrics.get_meter("dicecontroller.meter")

roll_counter = meter.create_counter(
    "dice.rolls",
    description="The number of rolls by value",
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/rolldice")
def roll_dice():
    with tracer.start_as_current_span("roll") as rollspan:
        player = request.args.get('player', default=None, type=str)
        result = str(roll())
        rollspan.set_attribute("roll.value", result)
        roll_counter.add(1, {'roll.value':result})
        if player:
            logger.warning("%s is rolling the dice: %s", player, result)
        else:
            logger.warning("Anonymous player is rolling the dice: %s", result)
        return result


def roll():
    return randint(1, 6)
