from monte_carlo import ProbaComputer
from ui.proba.gui import Overlay
from ui.regions.region import TitledRegionGroupSequence, getRegionsTitles
from ui.regions.screenRegionChoser import ScreenRegionChoser
from computer_vision.analyzeCards import CardsAnalyzer

if __name__ == "__main__":
    sequence = TitledRegionGroupSequence(*getRegionsTitles())
    overlay = ScreenRegionChoser(sequence)
    overlay.mainloop()

    proba_computer = ProbaComputer.ProbaComputer()
    cards_analyzer = CardsAnalyzer(sequence)
    overlay = Overlay(cards_analyzer, proba_computer)
    overlay.mainloop()