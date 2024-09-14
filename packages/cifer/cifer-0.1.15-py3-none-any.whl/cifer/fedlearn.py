import flwr as fl
import numpy as np
import torch
import json
from typing import Callable, Dict, Tuple
from flwr.common.logger import log
import importlib
import tensorflow as tf

class FedLearn:
    def __init__(self, config):
        self.config = config
        self.model = None
        self.server = None
        self.trainloader = None
        self.testloader = None
        print("FedLearn initialized with config:", self.config)
    
    def set_model(self, model: torch.nn.Module):
        """
        Set the model for the FedLearn instance.
        
        Args:
            model (torch.nn.Module): The PyTorch model to set.
        """
        self.model = model
        print("Model set successfully.")
    
    def set_data(self, trainloader, testloader):
        """
        Set the training and test data loaders.
        
        Args:
            trainloader: DataLoader for training data.
            testloader: DataLoader for testing data.
        """
        self.trainloader = trainloader
        self.testloader = testloader
        print("Data loaders set successfully.")

    def start_client(self):
        """
        Start the federated learning client.
        """
        if self.model is None or self.trainloader is None or self.testloader is None:
            raise ValueError("Model or data not set. Please set the model and data loaders first.")
        
        # Define the client class
        class CiferClient(fl.client.NumPyClient):
            def __init__(self, model, trainloader, testloader):
                self.model = model
                self.trainloader = trainloader
                self.testloader = testloader
            
            def get_parameters(self) -> np.ndarray:
                log("Getting parameters.")
                return get_parameters(self.model)
            
            def set_parameters(self, parameters: np.ndarray):
                log("Setting parameters.")
                set_parameters(self.model, parameters)
            
            def fit(self, parameters: np.ndarray, config: Dict[str, int]) -> Tuple[np.ndarray, int, Dict]:
                log("Starting training.")
                set_parameters(self.model, parameters)
                self.model.train()
                optimizer = torch.optim.SGD(self.model.parameters(), lr=config["lr"])
                for data, target in self.trainloader:
                    output = self.model(data)
                    loss = torch.nn.functional.cross_entropy(output, target)
                    loss.backward()
                    optimizer.step()
                    optimizer.zero_grad()
                log("Training complete.")
                return get_parameters(self.model), len(self.trainloader.dataset), {}
            
            def evaluate(self, parameters: np.ndarray, config: Dict[str, int]) -> Tuple[float, int, Dict]:
                log("Starting evaluation.")
                set_parameters(self.model, parameters)
                loss, accuracy = get_eval_fn(self.model, self.testloader)()
                log("Evaluation complete.")
                return loss, len(self.testloader.dataset), {"accuracy": accuracy}
        
        # Create a client instance
        client = CiferClient(self.model, self.trainloader, self.testloader)
        
        # Start the client
        fl.client.start_client(server_address=self.config.get('server_address', 'localhost:8080'), client=client)

    def start_server(self):
        """
        Initializes and starts the FedLearn server.
        """
        # Extract server configuration details
        server_address = self.config.get('server_address', 'localhost:8080')
        num_rounds = self.config.get('num_rounds', 10)
        strategy = self.config.get('strategy', 'FedAvg')
        grpc_max_message_length = self.config.get('grpc_max_message_length', 104857600)
        
        # Setup the strategy
        if strategy == 'FedAvg':
            strategy = fl.server.strategy.FedAvg(
                min_fit_clients=self.config.get('num_clients', 3),
                min_available_clients=self.config.get('num_clients', 3),
                # Additional strategy parameters can be set here
            )
        else:
            raise ValueError(f"Strategy {strategy} is not supported.")
        
        # Start the server
        fl.server.start_server(
            server_address=server_address,
            strategy=strategy,
            grpc_max_message_length=grpc_max_message_length,
        )
        print(f"FedLearn server started at {server_address} with strategy {strategy}.")

    def set_model(self, model: torch.nn.Module):
        """
        Set the model for FedLearn
        """
        self.model = model
        print("Model set successfully.")

    def run(self, train_dataset, test_dataset):
        """
        Run federated learning process

        Args:
            train_dataset: The training dataset to use.
            test_dataset: The test dataset to use.
        """
        if self.model is None:
            raise ValueError("Model is not set. Please set the model using set_model method.")

        # Create train and test loaders
        trainloader = torch.utils.data.DataLoader(train_dataset, batch_size=self.config.get('batch_size', 32), shuffle=True)
        testloader = torch.utils.data.DataLoader(test_dataset, batch_size=self.config.get('batch_size', 32))

        # Create federated learning client
        client = create_cifer_client(self.model, trainloader, testloader)

        # Start federated learning
        fl.client.start_client(server_address=self.config.get('server_address', 'localhost:8080'), client=client)



def load_and_initialize(config_path='config.json'):
    """
    Load configuration file and initialize FedLearn
    """
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        fl = FedLearn(config)
        return fl

    except FileNotFoundError:
        print(f"Configuration file {config_path} not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from the configuration file.")
    except Exception as e:
        print(f"An error occurred: {e}")

def check_gpu_support():
    """
    Check if the system supports GPU
    """
    if tf.config.list_physical_devices('GPU'):
        print("GPU is supported and available.")
    else:
        print("No GPU support found on this machine.")

def check_tpu_support():
    """
    Check if the system supports TPU
    """
    try:
        tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
        print(f"TPU is supported and available: {tpu}")
    except ValueError:
        print("No TPU support found on this machine.")

def check_installation():
    """
    Check if all necessary libraries are installed
    """
    libraries = ['numpy', 'pandas', 'scikit-learn', 'grpcio-tools']
    missing_libraries = []

    for lib in libraries:
        if importlib.util.find_spec(lib) is None:
            missing_libraries.append(lib)
    
    if not missing_libraries:
        print("All necessary libraries are installed correctly.")
    else:
        print("The following libraries are missing or not installed properly:")
        for lib in missing_libraries:
            print(f"- {lib}")

def get_eval_fn(model: torch.nn.Module, testloader: torch.utils.data.DataLoader) -> Callable[[], Tuple[float, float]]:
    """
    Returns an evaluation function for server-side evaluation.
    
    Args:
        model (torch.nn.Module): The PyTorch model to evaluate.
        testloader (torch.utils.data.DataLoader): The DataLoader for the test dataset.
    
    Returns:
        Callable: A function that returns a tuple (loss, accuracy) when called.
    """
    def evaluate() -> Tuple[float, float]:
        model.eval()
        loss, correct = 0, 0
        criterion = torch.nn.CrossEntropyLoss()
        with torch.no_grad():
            for data, target in testloader:
                output = model(data)
                loss += criterion(output, target).item() * data.size(0)
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
        loss /= len(testloader.dataset)
        accuracy = correct / len(testloader.dataset)
        log("Evaluation complete: loss={:.4f}, accuracy={:.4f}".format(loss, accuracy))
        return loss, accuracy
    
    return evaluate

def set_initial_parameters(model: torch.nn.Module, init: np.ndarray):
    """
    Set initial parameters for the model from a NumPy array.
    
    Args:
        model (torch.nn.Module): The PyTorch model to update.
        init (np.ndarray): The initial parameters to set.
    """
    params = torch.tensor(init, dtype=torch.float32)
    with torch.no_grad():
        for param, init_param in zip(model.parameters(), params):
            param.copy_(init_param)
    log("Initial parameters set.")

def get_parameters(model: torch.nn.Module) -> np.ndarray:
    """
    Get the parameters of the model as a NumPy array.
    
    Args:
        model (torch.nn.Module): The PyTorch model to extract parameters from.
    
    Returns:
        np.ndarray: The model parameters as a NumPy array.
    """
    params = np.concatenate([param.detach().numpy().ravel() for param in model.parameters()])
    log("Parameters retrieved.")
    return params

def set_parameters(model: torch.nn.Module, params: np.ndarray):
    """
    Set the model parameters from a NumPy array.
    
    Args:
        model (torch.nn.Module): The PyTorch model to update.
        params (np.ndarray): The parameters to set.
    """
    params = torch.tensor(params, dtype=torch.float32)
    with torch.no_grad():
        for param, param_data in zip(model.parameters(), params):
            param.copy_(param_data.reshape(param.size()))
    log("Parameters updated.")

def create_cifer_client(model: torch.nn.Module, trainloader: torch.utils.data.DataLoader, testloader: torch.utils.data.DataLoader) -> fl.client.Client:
    """
    Create a Cifer client for Federated Learning.
    
    Args:
        model (torch.nn.Module): The PyTorch model used by the client.
        trainloader (torch.utils.data.DataLoader): The DataLoader for the training dataset.
        testloader (torch.utils.data.DataLoader): The DataLoader for the test dataset.
    
    Returns:
        fl.client.Client: A Cifer client that can participate in Federated Learning.
    """
    class CiferClient(fl.client.NumPyClient):
        def get_parameters(self) -> np.ndarray:
            log("Getting parameters.")
            return get_parameters(model)

        def set_parameters(self, parameters: np.ndarray):
            log("Setting parameters.")
            set_parameters(model, parameters)

        def fit(self, parameters: np.ndarray, config: Dict[str, int]) -> Tuple[np.ndarray, int, Dict]:
            log("Starting training.")
            set_parameters(model, parameters)
            model.train()
            optimizer = torch.optim.SGD(model.parameters(), lr=config["lr"])
            for data, target in trainloader:
                output = model(data)
                loss = torch.nn.functional.cross_entropy(output, target)
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
            log("Training complete.")
            return get_parameters(model), len(trainloader.dataset), {}

        def evaluate(self, parameters: np.ndarray, config: Dict[str, int]) -> Tuple[float, int, Dict]:
            log("Starting evaluation.")
            set_parameters(model, parameters)
            loss, accuracy = get_eval_fn(model, testloader)()
            log("Evaluation complete.")
            return loss, len(testloader.dataset), {"accuracy": accuracy}
    
    return CiferClient()
