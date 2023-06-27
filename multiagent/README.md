AI LAB2
1)reflex agent
python3 pacman.py -p ReflexAgent -l testClassic
python3 pacman.py --frameTime 0 -p ReflexAgent -k 1 
python3 pacman.py --frameTime 0 -p ReflexAgent -k 2
python3 autograder.py -q q1 --no-graphics
python3 autograder.py -q q1
2)Minimax
python3 autograder.py -q q2 --no-graphics
python3 autograder.py -q q2 
3)alpha-beta pruning
python3 pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic
python3 autograder.py -q q3 --no-graphics
python3 autograder.py -q q3 
4)Expectimax
python3 autograder.py -q q4
python3 pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3
python3 pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10 
python3 pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
5)evaluation function
python3 autograder.py -q q5
