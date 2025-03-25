from common.Cards import Card
from computer_vision.captureScreen import captureRegion
from computer_vision.inference import load_model, run_inference, normalizeToProbabilities, getLabelFromProbabilities, format_input, format_input_OCR
from computer_vision.inference import idx_to_class_cards, idx_to_class_colors, idx_to_class_nbplayers
import easyocr

class CardsAnalyzer :

    region_order = [4,0,1,2,3,5]
    path_nbplayers = "./Classes/CustomResnet18_PokerNbPlayers_v1.2.onnx"
    path_cards = "./Classes/CustomResnet18_PokerValue_v4.0.onnx"
    path_colors = "./Classes/CustomResnet18_PokerColor_v2.4.onnx"

    def __init__(self, sequence):
        self.model_cards = load_model(self.path_cards)
        self.model_colors = load_model(self.path_colors)
        self.model_nbplayers = load_model(self.path_nbplayers)
        self.reader = easyocr.Reader(['en'])
        self.region_groups = sequence.region_groups
        
    def inference(self, model, formatted_input, idx_to_class):
        probas = normalizeToProbabilities(run_inference(model, formatted_input)[0])[0]
        predicted, proba = getLabelFromProbabilities(probas, idx_to_class)
        return (predicted, proba)
    
    def predictPlayerFold(self, unformatted_input) :
        input = format_input(unformatted_input)
        playerFoldInfo = self.inference(self.model_nbplayers, input, idx_to_class_nbplayers)
        return 1 if playerFoldInfo[0] == "P" else 0
    
    def predictCard(self, unformatted_input):
        input = format_input(unformatted_input)
        cardInfo = self.inference(self.model_cards, input, idx_to_class_cards)
        colorInfo = self.inference(self.model_colors, input, idx_to_class_colors)
        card = None
        if cardInfo[0] != "Unknown" and colorInfo[0] != "Unknown" :
            card = Card.initFromStr(cardInfo[0]+colorInfo[0])
        return card
    
    def predictTotalPot(self, unformatted_input) :
        input = format_input_OCR(unformatted_input)
        results = self.reader.readtext(input)
        results = [result[1].lower() for result in results]
        results = " ".join(results).split(" ")
        pots = []
        for i,result in enumerate(results) :
            if "bb" in result and i > 0 :
                pots.append(float(results[i-1].replace(",",".")))

        return max(pots) if len(pots) > 0 else None
    
    def predictActionValue(self, unformatted_input) :
        input = format_input_OCR(unformatted_input)
        results = self.reader.readtext(input)
        results = [result[1].lower() for result in results]
        results = " ".join(results).split(" ")

        if "check" in results :
            return 0

        for i,result in enumerate(results) :
            if "bb" in result and i > 0 :
                return float(results[i-1].replace(",","."))
    
    def readGroup(self, region_order_index) :
        cards = []
        for region in self.region_groups[self.region_order[region_order_index]] :
            screenshot = captureRegion(region)
            predicted_card = self.predictCard(screenshot)
            cards.append(predicted_card)
        return cards
    
    def readHand(self) :
        return self.readGroup(0)
    
    def readFlop(self) :
        return self.readGroup(1)
    
    def readTurn(self) :
        return self.readGroup(2)
    
    def readRiver(self) :
        return self.readGroup(3)
    
    def readNbPlayers(self) :
        nbPlayers = 1
        regions = self.region_groups[self.region_order[4]]
        for region in regions :
            screenshot = captureRegion(region)
            nbPlayers += self.predictPlayerFold(screenshot)
        return nbPlayers
    
    def readPotAndCall(self) :
        regions = self.region_groups[self.region_order[5]]
        #Total pot
        screenshot = captureRegion(regions[0])
        pot = self.predictTotalPot(screenshot)

        screenshot = captureRegion(regions[1])
        bet = self.predictActionValue(screenshot)

        return pot, bet
    
    def hasNone(self, cards) :
        return None in cards
