
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple

import flwr as fl
import numpy as np

import optuna




class  Strategy:
    """
    A class representing a strategy for Federated Learning.

    Attributes:
        name (str): The name of the strategy. Default is "FedAvg".
        fraction_fit (float): Fraction of clients to use for training during each round. Default is 1.0.
        fraction_evaluate (float): Fraction of clients to use for evaluation during each round. Default is 1.0.
        min_fit_clients (int): Minimum number of clients to use for training during each round. Default is 2.
        min_evaluate_clients (int): Minimum number of clients to use for evaluation during each round. Default is 2.
        min_available_clients (int): Minimum number of available clients required to start a round. Default is 2.
        initial_parameters (Optional[]): The initial parameters of the server model 
    Methods:
     
    """

    def __init__(
        self,
        name: str = "FedAvg",
        fraction_fit: float = 1.0,
        fraction_evaluate: float = 1.0,
        min_fit_clients: int = 2,
        min_evaluate_clients: int = 2,
        min_available_clients: int = 2,
        initial_parameters = [],
        evaluation_methode = "centralized" , 
        config = None
    ) -> None:
        """
        Initialize a Strategy object with the specified parameters.

        Args:
            name (str): The name of the strategy. Default is "FedAvg".
            fraction_fit (float): Fraction of clients to use for training during each round. Default is 1.0.
            fraction_evaluate (float): Fraction of clients to use for evaluation during each round. Default is 1.0.
            min_fit_clients (int): Minimum number of clients to use for training during each round. Default is 2.
            min_evaluate_clients (int): Minimum number of clients to use for evaluation during each round. Default is 2.
            min_available_clients (int): Minimum number of available clients required to start a round. Default is 2.
            initial_parameters (Optional[]): The initial parametres of the server model 
            evaluation_methode ( "centralized" | "distributed")
        """
        self.fraction_fit = fraction_fit
        self.fraction_evaluate = fraction_evaluate
        self.min_fit_clients = min_fit_clients
        self.min_evaluate_clients = min_evaluate_clients
        self.min_available_clients = min_available_clients
        self.initial_parameters = initial_parameters
        self.evaluate_fn = None
        self.name = name 
        self.config = config
        self.server_round = 0

    def get_trial(self, trial_number):
        # Retrieve the trial from the study
        trial = next((t for t in self.study.trials if t.number == trial_number), None)
        if trial:
            return trial
        else:
            return "Trial not found"
        
    def fit_config(self , server_round: int):
        """Return training configuration dict for each round.

        Perform two rounds of training with one local epoch, increase to two local
        epochs afterwards.
        """
        config  = self.config 
        
        if hasattr(self, 'study'):
            if 0 < server_round <= 0.7*10  and (server_round - 1 ) % self.hpo_rate == 0 : 
                if(self.server_round < server_round):
                    self.server_round = server_round
                    self.trail = []
                    
                

                print('================= this is the server trails')
                print(self.trail)

                trail = self.study.ask()
                self.trail.append(trail)
                learning_rate = trail.suggest_float('learning_rate', 1e-5, 1e-1)
                print(self.study.trials)
                print(trail.number)
                config = {
                    "trail" : trail ,
                    "server_rounds":  5 , 
                    "server_round" : server_round , 
                    "HPO_factor" : 0.5 , 
                    "study" : self.study , 
                    "HPO_RATE" : self.hpo_rate , 
                    "params" : {
                    "learning_rate" : learning_rate
                  }
                  }
                
        return config

    def optuna_fed_optimization(self, direction:str , hpo_rate:int , hpo_factor ,  params_config , sampler="TPESampler" , metric='AUC'):
        self.study = optuna.create_study(direction=direction , sampler=self.get_sampler_by_name(sampler)())
        self.hpo_rate = hpo_rate
        self.HPO_factor = hpo_factor
        self.config = params_config
        self.opt_metric = metric
    
 
    def create_strategy(self):
        self.strategy_object = self.get_strategy_by_name()(
            fraction_fit=self.fraction_fit,
            fraction_evaluate=self.fraction_evaluate,
            min_fit_clients=self.min_fit_clients,
            min_evaluate_clients=self.min_evaluate_clients,
            min_available_clients=self.min_available_clients,
            initial_parameters=fl.common.ndarrays_to_parameters(self.initial_parameters),
            evaluate_fn=self.evaluate_fn , 
            on_fit_config_fn = self.fit_config ,
            on_evaluate_config_fn = self.fit_config
        )
    def get_strategy_by_name(self):
        return eval(f"fl.server.strategy.{self.name}")
    
    def get_sampler_by_name(self , name) : 
        return eval(f"optuna.samplers.{name}")
    
    

