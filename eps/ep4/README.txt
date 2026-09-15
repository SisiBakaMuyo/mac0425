Para iniciar use o comando:

python gridworld.py -m

Código 1 - Iteração de Valor

python gridworld.py -a value -i 100 -k 10

media: 0.4676815372671002

BridgeGrid

python gridworld.py -a value -i 100 -k 10 -g BridgeGrid --discount 1 --noise 0.2

média: -49.5

python gridworld.py -a value -i 100 -k 10 -g BridgeGrid --discount 0.9 --noise 0

média: 5.9049000000000005


DiscountGrid

MDP 1
python gridworld.py -g DiscountGrid -a value --discount 0.1 --noise 0 --livingReward 0 -k 10

média: 0.0010000000000000005

MDP2
python gridworld.py -g DiscountGrid -a value --discount 0.5 --noise 0.2 --livingReward -2 -k 10

média: -3.833251953125

MDP 3
python gridworld.py -g DiscountGrid -a value --discount 1 --noise 0 --livingReward -1 -k 10

média: 5.0

MDP 4
python gridworld.py -g DiscountGrid -a value --discount 0.9 --noise 0.2 --livingReward 0 -k 10

média: 2.933479970890735

MDP 5
python gridworld.py -g DiscountGrid -a value --discount 1 --noise 0.2 --livingReward 10 -k 10

média: não termina nunca, fica em looping


Código 2 - Q-Learning

python gridworld.py -a q -k 100

média: 0.20299142771121748

python gridworld.py -a q -k 100 --noise 0.0 -e 0.1

média: 0.4927890234790868

python gridworld.py -a q -k 100 --noise 0.0 -e 0.9

média: 0.015071614215058697

Pac-Man

python pacman.py -p PacmanQAgent -x 2000 -n 2010 -l smallGrid

média: 499.8

GreedyAgent

python pacman.py -p GreedyAgent -l smallGrid -n 100

média: 251.33

python pacman.py -p GreedyAgent -l tinyCorners -n 100

média: -164,41























