"""
Artificial Intelligence to play Hanabi.
"""

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game


class Cheater(AI):
    """
    This player can see his own cards!

    Algorithm:
      * if 1-or-more card is playable: play the lowest one, then newest one
      * if blue_coin<8 and an unnecessary card present: discard it.
      * if blue_coin>0: give a clue on precious card (so a human can play with a Cheater)
      * if blue_coin<8: discard the largest one, except if it's the last of its kind or in chop position in his opponent.
    """

    def play(self):
        "Return the best cheater action."
        game = self.game
        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number ]

        if playable:
            # sort by ascending number, then newest
            playable.sort(key=lambda p: (p[1], -p[0]))
            print ('Cheater would play:', "p%d"%playable[0][0], end=' ')
            if (len(playable)>1):
                print('but could also pick:', playable[1:])
            else: print()

            return "p%d"%playable[0][0]
            

        discardable = [ i+1 for (i,card) in
                        enumerate(game.current_hand.cards)
                        if ( (card.number <= game.piles[card.color])
                             or (game.current_hand.cards.count(card)>1)
                        ) ]
        # discard already played cards, doubles in my hand
        # fixme: discard doubles, if I see it in partner's hand
        # fixme: il me manque les cartes sup d'une pile morte
        
        if discardable and (game.blue_coins<8):
            print ('Cheater would discard:', "d%d"%discardable[0], discardable)
            return "d%d"%discardable[0]

        ## 2nd type of discard: I have a card, and my partner too
        discardable2 = [ i+1 for (i,card) in enumerate(game.current_hand.cards)
                         if card in game.hands[game.other_player].cards
                       ]
        if discardable2 and (game.blue_coins<8):
            print ('Cheater would discard2:', "d%d"%discardable2[0], discardable2)
            return "d%d"%discardable2[0]
        

        ## Look at precious cards in other hand, to clue them
        precious = [ card for card in
                     game.hands[game.other_player].cards
                     if (1+game.discard_pile.cards.count(card))
                         == game.deck.card_count[card.number]
                   ]
        if precious:
            clue = False
            # this loop is such that we prefer to clue an card close to chop
            # would be nice to clue an unclued first, instead of a already clued
            for p in precious:
                #print (p, p.number_clue, p.color_clue)
                if p.number_clue is False:
                    clue = "c%d"%p.number
                    break
                if p.color_clue is False:
                    clue = "c%s"%p.color
                    break
                # this one was tricky:
                # don't want to give twice the same clue
            if clue:
                print ('Cheater would clue a precious:',
                       clue, precious)
                if game.blue_coins>0:
                    return clue
                print ("... but there's no blue coin left!")

        
        # if reach here, can't play, can't discard safely, no card to clue-save
        # Let's give a random clue, to see if partner can unblock me
        if game.blue_coins >0:
            print ('Cheater would clue randomly: cW')
            return 'cw'

        # If reach here, can't play, can't discard safely
        # No blue-coin left.
        # Must discard a card. Let's choose a non-precious one (preferably a 4)
        mynotprecious = [ (card.number,i+1) for (i,card) in
                          enumerate(game.current_hand.cards)
                          if not (
                                  (1+game.discard_pile.cards.count(card))
                                  == game.deck.card_count[card.number])
                     ]
        mynotprecious.sort(key=lambda p: (-p[0], p[1]))
        if mynotprecious:
            act = 'd%d'%mynotprecious[0][1]
            print('Cheater is trapped and must discard:', act, mynotprecious)
            return act

        # Oh boy, not even a safe discard, this is gonna hurt!
        # it's a loss. Discard the biggest
        myprecious = [ (card.number,i+1) for (i,card) in enumerate(game.current_hand.cards) ]
        myprecious.sort(key=lambda p: (-p[0], p[1]))
        act = 'd%d'%myprecious[0][1]
        print('Cheater is doomed and must discard:', act, myprecious)
        return act


class Random(AI):
    # Joue au hasard #

    def play(self):
        "Return the best cheater action."
        game = self.game

        #On tire au hasard un des 3 entiers associés aux actions : #
        # 1 : discard
        # 2 : play
        # 3 : clue

        actio=['d','p','c']
        tmp=rd.randint(0,2)
        act=actio(tmp)

        return(act)

class Safe(AI):

    def play(self):
        "Return the safest action to do "

        game = self.game

        #Indices possédés dans la main : liste de cartes#
        hand=self.current_hand.str_clue()

        #Piles sur la table#

        piles_act=self.piles

        #On cherche d'abord si on peut poser une carte#
        #Si j'ai bien compris : hand = une liste de 1 élément : voir papier pour exemple#

        #On doit donc séparer les différents cartes : 2 cartes sont séparées par un espace#

        split_hand=hand.split()

        #On parcourt la liste de cartes et on indique quelle carte est à jouée en priorité. On ressort de la boucle 
        # avec l'indice de la carte qui est à jouée  : idx_prio. Si pas 2 indices : pas de prio.

        idx_prio=-1


        for i in split_hand :

            #On sépare les 2 indices #
            split_clues=split_hand[i].split("")

            #On regarde combien d'indices on possède sur chaque carte#

            nb_clues=2-split_clues.count('*')
            if nb_clues==2:
                idx_prio=i

        #Si on a un idx_prio !=-1 : on joue cette carte#

        if idx_prio!=-1:
            return('p')







        
        

