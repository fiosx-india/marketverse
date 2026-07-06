"""
MarketVerse AI
Master System Controller
"""

from modules.central_brain import CentralBrain


class SystemController:

    def __init__(self):
        self.brain = CentralBrain()

    def start(self, symbol):

        print("========== MARKETVERSE START ==========")

        # Central Brain (Guardian runs internally)
        result = self.brain.think(symbol)

        return {
            "status": "ONLINE",
            "analysis": result
        }
