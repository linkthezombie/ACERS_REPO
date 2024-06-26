# ACERS_REPO
The github for ACER'S developed programs

Requirement 15 is the document AbstractionLayer  
Requirement 16.1 is the document GameStrategy  
Requirement 16.2 is the document FSM  

Sprint 3:   
Requirement 24 is in hand.py  
Requirement 17 is both in FSM and GameStrategy  
Requirement 5 and 26 are in ComputerVision.py

Sprint 4:  
Requirement 8: ComputerVision.py  
Requirement 9.2.2 and 13.1: RobbotMotion.py  
Requiremnt 18: GameStrategy.py  
Requirement 22.1: FSM.py - completed ahead of schedule  

Sprint 5:  
Requirement 9.2.1, 34, 36: in RobotMotion.py and ComputerVision.py  
Requirement 22.2.1: ComputerVision.py - completed ahead of schedule  
Requirement 35: in FSM.py  

Sprint 6:  
Requirement 9.2.3: robotMotion.py  
Requirement 9.2.4.1: robotMotion.py - completed ahead of time  
Requirement 22.2.2: FSM.py, ComputerVision.py  
Requirement 25: FSM.py, robotSpeech.py  
Requirement 29.1: FSM.py, CommandDetection.py  
Requirement 33: FSM.py, robotMotion.py, ComputerVision.py  
Requirement 37: FSM.py, robotMotion.py, ComputerVision.py, CommandDetection.py  

Sprint 7:  
Requirement 9.2.4.2: robotMotion.py  
Requirement 13.2: robotMotion.py  
Requirement 29.2: CommandDetection.py  
Requirement 29.3: CommandDetection.py  
Requirement 31: CommandDetection.py, FSM.py, gameStrategy.py, RobotSpeech.py  
Requirement 32: gameStrategy.py - completed early  
Requirement 37.2: CommandDetection.py, FSM.py, gameStrategy.py, RobotSpeech.py  

Sprint 8:  
Requirement 38: RobotMotion.py  
Requirement 41: FSM.py, GameStrategy.py, CommandDetection.py  
Requirement 44: CommandDetection.py  
Requirement 45.1: CommandDetection.py  
Requirement 45.2: CommandDetection.py (finshed ahead of schedule)  
Requirement 46.1: Spring Requirements Folder  

Sprint 9:  
Requirement 40: FSM.py, GameStrategy.py, CommandDetection.py, AbstractionLayer.py  
Requirement 42: tested on 2/19 and 2/21  
Requirement 43: FSM.py, CommandDetection.py, AbstractionLayer.py (finished early)  
Requirement 46.2: printed and tested on 2/21  
Requirement 47: tested on 2/21 (done early)  
Requirement 49: FSM.py, GameStrategy.py, CommandDetection.py, AbstractionLayer.py, RobotSpeecg.py and tested on 2/19 and 2/21  
Requirement 51: FSM.py, CommandDetection.py, AbstractionLayer.py, RobotSpeech.py  
Requirement 52: FSM.py, CommandDetection.py, AbstractionLayer.py, RobotSpeech.py  
Requirement 53: CommandDetection.py, AbstractionLayer.py, RobotSpeech.py  
Requirement 54: CommandDetection.py, AbstractionLayer.py, RobotSpeech.py  

Sprint 10:  
Requirement 23: RobotSpeech.py  
Requirement 48: CommandDetection.py, AbstractionLayer.py, RobotSpeech.py  
Requirement 55: RobotMotion.py  
Requirement 56: CommandDetection.py, AbstractionLayer.py, FSM.py  
Requirement 57: CommandDetection.py, AbstractionLayer.py, RobotSpeech.py, FSM.py  
Requirement 58: RobotMotion.py, AbstractionLayer.py, FSM.py  
Requirement 59: 3D printed  
Requirement 60: CommandDetection.py, AbstractionLayer.py, RobotSpeech.py, ComputerVision.py, hand.py, GameStrategy.py, FSM.py and tested the week of 3/4  

Sprint 11:  
Requirement 21.1: FSM.py, GameStrategy.py, CommandDetection.py, AbstractionLayer.py, RobotSpeech.py  
Requirement 21.2: FSM.py, GameStrategy.py, CommandDetection.py, AbstractionLayer.py, RobotSpeech.py  
Requirement 39: FSM.py, GameStrategy.py, CommandDetection.py, AbstractionLayer.py, RobotSpeecg.py, RobotMotion.py, ComputerVision.py  
Requirement 50.1: work to be seen in video presentation next week(completed ahead of schedule)  
Requirement 50.1: work to be seen in video presentation next week (completed ahead of schedule)  
Requirement 61: RobotMotion.py, AbstractionLayer.py, FSM.py  
Requirement 62: GameStrategy.py  
Requirement 63: FSM.py  
Requirement 64: RobotMotion.py  

Sprint 12:  
Requirement 20: RobotSpeech.py, CommandDetection.py  
Requirement 28.1: in spring docuements folder  
Requirement 28.2: BlackJackLogic.py  
Requirement 50.3-50.6:  final work seen in video submitted on canvas  
Requirement 65: thorugh all files  

Sprint 13:  
Requirement 66: BlackJackLogic.py, BlackJackStrategy.py, CommandDetection.py, AbstractionLayer.py, RobotSpeech.py  
Requirement 67.1: BlackJackLogic.py, BlackJackStrategy.py, hand.py  
Requirement 67.2: BlackJackLogic.py, BlackJackStrategy.py, CommandDetection.py, AbstractionLayer.py, RobotSpeech.py, RobtotMotion.py  
Requirement 68:  throughout various files  
Requirement 69:  RobotSpeech.py  
Requirement 70:  RobotMotion.py  
Requirement 70.1:  ComputerVision.py, RobotSpeech.py  

   - Intro: 
      - First, we had to discuss potential ideas for interacting with the cards that would work in a human like way and allow the Nao to play a game.
	    - We knew the Nao must be able to draw a card from a pile, hold the card and move it around, set the card in his hand and in the draw pile, and draw a card from his hand to play.
      - We used the Choregraphe software to control his joints by hand to test his limitations and abilities.
      
   - Brainstorming methods to interact with card:
     - Without any aid:
        - Pros:
            No extra modifications required
	          No residue
	          Not bulky
	          Looks natural
        - Cons:
            No guarantee Nao’s fingers can keep grip on a card
     - Double sided tape:
        - Pros:
            Easy to draw a card from a pile or pick it up
            Not bulky
            Easy to attach to the Nao
         - Cons:
            Residue left on Nao
          	Must replace when no longer sticky
          	Hard to detach the card to set it down
     - Grippy/textured surface:
      	Like rubbers or sandpaper like material
         - Pros:
          	Easy to let go of the card
          	Easy to drag a card and move it into the Nao’s grip
          	No residue
        - Cons:
          	Hard to attach to the delicate fingers of the Nao
          	Bulky
          	Lifting the card up from horizontal position

   - Testing:
       - First, we decided to test the Nao without any additions to see is it was possible to pick up a card and hold it.
           - We held out a card and the Nao was guided to reach out and grab it then move their arm away.
           - This proved successful on multiple attempts proving he could hold and interact with cards without aid.
       - Next up was testing picking up a card from a stack.
           - We set up a stack of cards in front of the Nao to see if he would be able to separate one card from the stack.
           - We found if he applies too much pressure the stack becomes a mess, but if he sets his fingers on it and drags towards himself, he is able to separate a card that he can then grab the bottom by closing his grip and picking it up.
       - Finally, we tested letting go of a card.
           - We would place a card in his hand and see if he could set it down in the right orientation to be a discard pile.
           - It was difficult to figure out the way his joints should move, but we found if he picks it up with one hand then hands its off to his other hand then it will be in the right orientation.
           - He then can angle his hand down, open his fingers, and move his shoulder and elbow back to let go of the card and place it on the table.

   - Conclusions:
      - After testing we found that the Nao would be able to accomplish the required movements to complete his tasks without modification.  The next step will be to determine specific movements to regularly perform these actions with confidence.


