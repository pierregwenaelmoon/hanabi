"""
Unitary testin of Deck.
"""

import unittest
import hanabi


class DeckTest(unittest.TestCase):
    def setUp(self):
        pass


    def test_shuffle(self):
        Paquet = hanabi.Deck()
        b=0
        Paquet_aux = hanabi.Deck()
        Paquet_aux.cards = Paquet.cards
        
        for k in range(10): 
            
            # On test si sur 10 mélange le deck est bien différent au moins 2 fois

            Paquet_aux.cards = Paquet.cards
            Paquet.shuffle()
            if Paquet!=Paquet_aux:
                b+=1
        self.assertTrue(b>2)

    def test_draw(self):

        # On teste si la carte piochée est la bonne et si le deck a bien été délesté d'une carte

        Paquet = hanabi.Deck()
        Paquet.shuffle()
        LaCarte = Paquet.cards[0]
        nombre_cartes = len(Paquet.cards)
        LaCarte2 = Paquet.draw()
        self.assertEqual(len(Paquet.cards),nombre_cartes-1)
        self.assertEqual(LaCarte,LaCarte2)


    def test_deal(self):

        #On test si le nombre de carte par main est le bon pour 5, 4 et 3 et si les mains retournées sont de la classe Hand

        Paquet = hanabi.Deck()
        Hands = Paquet.deal(5)
        b = True
        for x in Hands:
            self.assertTrue(isinstance(x,hanabi.deck.Hand))
            if len(x)!=4:
                b = False
        self.assertEqual(b,True)
        
        Paquet = hanabi.Deck()        
        Hands = Paquet.deal(3)
        b = True
        for x in Hands:
            self.assertTrue(isinstance(x,hanabi.deck.Hand))
            if len(x)!=5:
                b = False
        self.assertEqual(b,True)
         
        Paquet = hanabi.Deck() 
        Hands = Paquet.deal(4)
        
        b = True
        for x in Hands:
            self.assertTrue(isinstance(x,hanabi.deck.Hand))
            if len(x)!=4:
                b = False
        self.assertEqual(b,True)






if __name__ == '__main__':
    unittest.main()
