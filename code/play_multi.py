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
from dqn_single import DqnSingle
import turtlesim_env_single

class PlaySingle(DqnSingle):
   
   def run_turtle(self, tname):
        current_state = self.env.reset(tnames=[tname], sections=['random'])[tname].map # Losuje punkt startowy, aby zawsze zaczynać od pierwszego zmienić na 'default'
        last_state=[i.copy() for i in current_state]
        env.tapi.setPen(tname,turtlesim.srv.SetPenRequest(off=0))   # Rysuj trasę
        
        while True:                                                             
            control = np.argmax(self.decision(self.model, last_state, current_state)) # Decyzja ruchu

            new_state, reward, done = self.env.step({tname:self.ctl2act(control)})  #krok 
            
            # if done:
            #     break
            last_state = current_state                                          # przejście do nowego stanu
            current_state = new_state                                           # z zapamiętaniem poprzedniego

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", required=True, help="Path to .tf model file")
    args = parser.parse_args()
    
    env=turtlesim_env_single.provide_env()                      # utworzenie środowiska
    env.setup('routes.csv',agent_cnt=1)                         # połączenie z symulatorem
    env.SPEED_FINE_RATE = -5.0                                  # zmiana wybranych parametrów środowiska
    agents=env.reset()                                          # ustawienie agenta
    tname=list(agents.keys())[0]                                # 'lista agentów' do wytrenowania
    playSingle=PlaySingle(env, seed=None)                       # Reset seed na potrzeby testów i różnych miejsc początkowych          
    playSingle.model=keras.models.load_model(args.model)                          # albo załadowanie zapisanej wcześniej
    playSingle.run_turtle(tname)