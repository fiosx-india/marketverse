"""
MarketVerse AI
Master System Controller
"""

from modules.guardian import run_guardian
from modules.central_brain import CentralBrain


class SystemController:

    def __init__(self):
        self.brain = CentralBrain()

    def start(self, symbol):

        print("========== MARKETVERSE START ==========")

        # Health Check
        guardian_report = run_guardian()

        # Brain Analysis
        result = self.brain.think(symbol)

        return {
            "guardian": guardian_report,
            "analysis": result
        }
