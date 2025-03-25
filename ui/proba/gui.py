import pyautogui
import tkinter as tk
from common.Cards import Hand, Table
from computer_vision.analyzeCards import CardsAnalyzer
import traceback

class Overlay(tk.Tk):
    def __init__(self, cards_analyzer : CardsAnalyzer, proba_computer):
        tk.Tk.__init__(self)

        self.last_table = None
        self.last_hand = None
        self.results = None
        self.last_nb_players = 0
        self.nb_try = 0
        self.cards_analyzer = cards_analyzer
        self.proba_computer = proba_computer

        # Create a transparent overlay window
        self.attributes("-alpha", 0.9)  # Set transparency (0.0 to 1.0)
        self.overrideredirect(True)  # Remove window decorations (title bar, etc.)

        # Set the overlay window to cover the entire screen
        screen_width, screen_height = pyautogui.size()
        self.dim_x, self.dim_y = screen_width//5, int(screen_height/2.8)
        self.geometry(f"{self.dim_x}x{self.dim_y}+0+0")

        # Your Python interface elements
        self.title_label = tk.Label(self, text="Objective Stats", font=("Helvetica", 16), fg="red")
        self.hand_label = tk.Label(self, text="Hand : Unknown", font=("Helvetica", 16))
        self.table_label = tk.Label(self, text="Table : Unknown", font=("Helvetica", 16))
        self.proba_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.mean_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.nbplayers_label = tk.Label(self, text="2 Players", font=("Helvetica", 16))
        self.distribution_canvas = tk.Canvas(self, width=self.dim_x, height=self.dim_y//2)
        self.title_label.pack(padx=10, pady=5)
        self.hand_label.pack(padx=10, pady=5)
        self.table_label.pack(padx=10, pady=5)
        self.nbplayers_label.pack(padx=10, pady=5)
        self.proba_label.pack(padx=10, pady=15)
        self.distribution_canvas.pack(anchor="s")
        #self.mean_label.pack(padx=10, pady=5)

        # Prevent the overlay window from losing focus
        self.attributes("-topmost", True)
        self.grab_set()

        # Allow dragging the overlay window
        self.bind("<B1-Motion>", self.drag_window)
        self.bind("<Escape>", lambda x: self.destroy())

        self.update()

    def setMean(self, pot, bet) :
        if pot is None or bet is None or self.nb_try == 0 :
            self.mean_label.config(text="??.??B (Ratio ??.??)")
        else :
            proba = self.count / self.nb_try
            value = (pot) * proba - bet * (1-proba)
            self.mean_label.config(text="{}{:.2f}B (Ratio {:.2f})".format("+" if value > 0 else "-", abs(value), 0 if bet == 0 else value/bet))
    def setHand(self, hand) :
        if hand is None :
            self.hand_label.config(text="Hand : Unknown")
        else :
            self.hand_label.config(text="Hand : "+str(hand))
    def setTable(self, table) :
        if table is None :
            self.table_label.config(text="Table : Unknown")
        else :
            self.table_label.config(text="Table : "+str(table))
    def setProba(self, proba) :
        if proba is None :
            self.proba_label.config(text="??.??%")
        else :
            self.proba_label.config(text="{:.2f}%".format(proba*100))
    def setNbPlayers(self, nbPlayers) :
        self.nbplayers_label.config(text="{} Players".format(nbPlayers))

    def displayProba(self, hand, table, nb_players) :
        #Computation Handler
        nb_try = 5000
        table = hand._cards+table._cards if hand is not None and table is not None else (hand._cards if hand is not None else None)
        if (not (self.last_table is None and table is None)) and ((nb_players != self.last_nb_players) or(table is None and self.last_table is not None) or (self.last_table is None and table is not None) or str(Table(self.last_table)) != str(Table(table))) :
            self.count = 0
            self.nb_try = 0
            self.last_table = table
            self.last_nb_players = nb_players

        if not table is None and not nb_players is None :
            self.count += self.proba_computer.estimateCountWithCards(nb_players, nb_try, table)
            self.nb_try += nb_try
            self.setProba(self.count/self.nb_try)
        else :
            self.setProba(None)

        """pot, bet = self.cards_analyzer.readPotAndCall()
        self.setMean(pot, bet)"""

    def draw_bar_chart(self, canvas : tk.Canvas, data, bar_width=30, bar_color='blue'):
        height = canvas.winfo_reqheight()
        width = canvas.winfo_reqwidth()
        num_bars = len(data)
        norm = max(data)

        # Calculate the width of each bar including spacing
        total_width = (num_bars * bar_width)

        canvas.delete("bar")
        offset = (width-total_width)/2
        for i,value in enumerate(data):
            x = i*bar_width + offset
            bar_height = value*height//norm
            canvas.create_rectangle(x, height - bar_height, x + bar_width, height, fill=bar_color, tags="bar")

    def displayNextProbaDistribution(self, hand, table, nb_players, nb_parts=10) :
        if self.hasChanged(self.last_table, table) or self.hasChanged(self.last_hand, hand) or self.last_nb_players != nb_players :
            self.results = [0]*nb_parts
            self.last_table = table
            self.last_hand = hand
            self.last_nb_players = nb_players
            self.nb_try = 0
            height = self.dim_y//2
            off = (self.distribution_canvas.winfo_reqwidth()-10*30)/2
            for i in range(10) :
                self.distribution_canvas.create_rectangle(off+i*30, 0, off+(i+1)*30, height, fill='#CBCAFF' if i%2==0 else "", tags="bg")
        
        cards = [str(card) for card in hand._cards+table._cards]
        
        if len(table) == 3 :
            n = 2
            nb_try = 10
        elif len(table) == 4 :
            n = 1
            nb_try = 50
        else :
            n = 0
            nb_try = 400

        results = self.proba_computer.estimateCountWithCardsNextNRounds(nb_players, nb_try, cards, n, nb_parts=nb_parts)
        self.results = [results[i]+self.results[i] for i in range(len(results))]
        self.draw_bar_chart(self.distribution_canvas, self.results)
        """plt.bar([i/nb_bins for i in range(nb_bins)], results, align='edge', width=1/nb_bins)
        plt.show()"""

    def displayKeyProba(self, hand, table) :
        if hand is None or table is None :
            self.proba_label.config(text="")
            return
        
        table = hand._cards+table._cards if hand is not None and table is not None else (hand._cards if hand is not None else None)
        if (not (self.last_table is None and table is None)) and ((table is None and self.last_table is not None) or (self.last_table is None and table is not None) or str(Table(self.last_table)) != str(Table(table))) :
            self.last_table = table

            dic = self.proba_computer.computeProbaOfKeys(table)
            sorted_keys = sorted(dic, key=dic.get, reverse=True)
            to_display = ""
            for i in range(1,6) :
                key = sorted_keys[i]
                count = dic[key]
                to_display += "{} : {:.2f}%\n".format(key, count/dic['nb']*100)
            to_display = to_display[:-1]
            self.proba_label.config(text=to_display)

    def displayPreFlopProba(self, hand, nb_players) :
        if hand is not None :
            self.setProba(self.proba_computer.retrievePreFlopProba(hand, nb_players)/100)
        else :
            self.setProba(None)

    def update(self) :
        #Hand Handler
        try :
            hand = self.cards_analyzer.readHand()
            hand = Hand(hand) if not self.cards_analyzer.hasNone(hand) else None
            self.setHand(hand)

            #Table Handler
            table = []
            flop = self.cards_analyzer.readFlop()
            if not self.cards_analyzer.hasNone(flop) :
                table.extend(flop)
            turn = self.cards_analyzer.readTurn()
            if not self.cards_analyzer.hasNone(turn) :
                table.append(turn[0])
            river = self.cards_analyzer.readRiver()
            if not self.cards_analyzer.hasNone(river) :
                table.append(river[0])
            table = Table(table) if table != [] else None 
            self.setTable(table)

            #Nb Player Handler
            nb_players = self.cards_analyzer.readNbPlayers()
            if nb_players <= 1 :
                nb_players = 2
            self.setNbPlayers(nbPlayers=nb_players)

            if table is None :
                self.distribution_canvas.pack_forget()
                self.proba_label.pack(padx=10, pady=15)
                self.displayPreFlopProba(hand, nb_players)
                #self.displayProba(hand, table, nb_players)
            elif hand is not None :
                self.proba_label.pack_forget()
                self.distribution_canvas.pack(anchor="s")
                self.displayNextProbaDistribution(hand, table, nb_players)
            else :
                self.distribution_canvas.pack_forget()
                self.proba_label.pack_forget()

        except Exception as e:
            print("An exception occurred:", e)
            traceback.print_exc()

        self.after(1000, self.update)

    def hasChanged(self, last, new) :
        if last is None or new is None :
            return True
        if str(last) != str(new) :
            return True
        return False

    def drag_window(self, event):
        x, y = event.x_root - self.winfo_width() / 2, event.y_root - self.winfo_height() / 2
        self.geometry("+%d+%d" % (x, y))

if __name__ == "__main__":
    overlay = Overlay(None)
    overlay.mainloop()
