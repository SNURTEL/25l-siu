# encoding: utf8
import argparse
import random
import pickle
import turtlesim
import numpy as np
from collections import deque
from tensorflow import keras, constant
from keras.models import Sequential
from keras.layers import Conv3D, Permute, Dense, Flatten
from turtlesim_env_base import TurtlesimEnvBase
from dqn_multi import DqnMulti
import turtlesim_env_multi

class PlayMulti(DqnMulti):
   
   def run_turtle(self, tnames):
        agents = self.env.reset(tnames=tnames, sections=['random' for tname in tnames]) # Losuje punkt startowy, aby zawsze zaczynać od pierwszego zmienić na 'default'
        current_states={tname:agent.map for tname,agent in agents.items()}
        last_states={tname:agent.map for tname,agent in agents.items()}
        
        while True:                 
            actions = {} 
            for tname in tnames:                                       
                env.tapi.setPen(tname,turtlesim.srv.SetPenRequest(off=0))   # Rysuj trasę
                control = np.argmax(self.decision(self.model, last_states[tname], current_states[tname])) # Decyzja ruchu
                actions[tname] = self.ctl2act(control)

            results = self.env.step(actions)  #krok 
        
            for tname in tnames:                                       
                new_state, reward, done = results[tname]
                # if done:
                #     break
                last_states[tname] = current_states[tname]                                          # przejście do nowego stanu
                current_states[tname] = new_state                                           # z zapamiętaniem poprzedniego

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", required=True, help="Path to .tf model file")
    args = parser.parse_args()
    
    env=turtlesim_env_multi.provide_env()                      # utworzenie środowiska
    env.setup('routes.csv',agent_cnt=30)                       # połączenie z symulatorem
    env.SPEED_FINE_RATE = -5.0                                  # zmiana wybranych parametrów środowiska
    env.DETECT_COLLISION = True
    agents=env.reset()                                          # ustawienie agenta
    tnames=list(agents.keys())                                  # 'lista agentów' do wytrenowania
    playMulti=PlayMulti(env, seed=None)                       # Reset seed na potrzeby testów i różnych miejsc początkowych          
    playMulti.model=keras.models.load_model(args.model)        # albo załadowanie zapisanej wcześniej
    playMulti.run_turtle(tnames)