import os
from pathlib import Path
import yaml
from schema import Schema, And, Use, Optional, SchemaError
import rich_click as click
import copy
from typing import Self

class ConfigError(Exception):
    def __init__(self, message: str, errors):            
        super().__init__(message)
        self.errors = errors

class Config:
    def __init__(self):
        self.schema = Schema(Optional({
            'clients': {
                Optional(str): {
                    'user': And(Use(str)),
                    'client_id': And(Use(int)),
                    'token': And(Use(str))
                }
            },
            'active': {
                Optional('project'): And(Use(str)),
                Optional('client'): And(Use(str)),
            }
        }))

        with open(self.__get_file(), 'r') as file:
            config = yaml.safe_load(file)

        if not config:
            config = { 'clients': {}, 'active' : {}}

        self.__validate(config)
        self.obj = config
        self.changes = copy.deepcopy(config)

    def __validate(self, config: dict): 
        try:
            self.schema.validate(config)
        except SchemaError as err:
            raise ConfigError('Invalid CLI configuration file in ~/.wake-arena/config.yaml', [err])


    def __get_file(self):
        config_path = os.path.expanduser('~/.wake-arena/')
        config_file = config_path + 'config.yaml'

        Path(config_path).mkdir(parents=True, exist_ok=True)
        Path(config_file).touch(exist_ok=True)

        return config_file

    def add_client(self, name: str, user: str, client_id: str, token: str) -> Self:
        client_config = { 'user': user, 'client_id': client_id, 'token': token }
        self.changes['clients'].update({ name: client_config })
        return self

    def set_active_client(self, name: str) -> Self: 
        self.changes['active'].update({'client': name})
        return self
    
    def set_active_project(self, slug: str) -> Self: 
        self.changes['active'].update({'project': slug})
        return self
    
    def write(self) -> Self:
        self.__validate(self.changes)

        with open(self.__get_file(), 'w') as file:
            yaml.safe_dump(self.changes, file)

        self.obj = copy.deepcopy(self.changes)
        return self

    def get_clients(self) -> dict: 
        return self.obj.get('clients', {})
    
    def get_active(self) -> dict:
        return self.obj.get('active', {})
    
    def get_active_project(self) -> str | None:
        return self.get_active().get('project', None)
    
    def get_active_client(self) -> dict | None:
        active = self.get_active()
        clients = self.get_clients()

        name = active.get('client', None)

        if not name:
            return None
        
        if name in clients:
            return clients.get(name)
    
        raise ConfigError('Invalid configuration')
        



