from .implements.fight_decision_maker import FightDecisionMaker, FightDecision

import numpy as np


def sendImageToAPI(image: np.ndarray) -> FightDecision:
    # returns some json response object
    return FightDecision({"cardIndex": 0, "location": (0, 0)})


class ClientFightDecisionMaker(FightDecisionMaker):
    def make_decision(self) -> FightDecision:
        image = self.inputs[-1]
        response = sendImageToAPI(image)

        # process response and return decision
        return response

def main() -> None:
    decision_maker = ClientFightDecisionMaker()
    image = np.random.rand(100, 100)
    decision_maker.add_input(image)
    decision = decision_maker.make_decision()
    print(decision)
