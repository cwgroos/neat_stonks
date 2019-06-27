from __future__ import print_function
import os
import neat
from stonks_bot import stonks_bot as bot
from stonks_data import stonks_data as data

_INITIAL_MONEY = 10000
_DEFAULT_WOA = 1
start = 0
stocks = data('table_nflx.csv')

def eval_genomes(genomes, config):
    global start
    global stocks
    start = stocks.set_window_start(_DEFAULT_WOA)
    for genome_id, genome in genomes:
      try:
        window = 0
        trader = bot(genome, config, _INITIAL_MONEY, stocks)
        ending_balance = 0
        while window < _DEFAULT_WOA:
          window = window + 1
          ending_balance = trader.take_action()
        genome.fitness = ending_balance
        print(ending_balance)
      except KeyboardInterrupt:
        exit()

def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    config_path = os.path.join(os.getcwd(), 'config')
    print(config_path)
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    global start
    start = stocks.set_window_start(start)
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    # Checkpoint every 25 generations or 900 seconds.
    pop.add_reporter(neat.Checkpointer(25, 900))

    # find best genome
    pop.run(eval_genomes, 10)

if __name__ == "__main__":
        #env.reset()    
        #state, reward, done, info = env.step(env.action_space.sample())
        #print(state.flatten().shape)
        run()
