# -*- coding: utf-8 -*-
import abc

"""
Interface class of property file operation class.
"""
class DbCoreRepository(metaclass=abc.ABCMeta):
    """ abstract class of the database repository class.
    :author: T.Minami
    :version: 1.0.0
    :since: 1.0.0
    :note:
        The abstract class for database repository classes. When developing database repositories,
        define this as an interface to standardize them.
    """

    @abc.abstractmethod
    def dbConnection(self,
                     dbhost:str,
                     port:int,
                     serviceName:str,
                     userName:str,
                     userPass:str) -> object:
        """ DB connection instance """
        raise NotImplementedError()

    @abc.abstractmethod
    def insertRecord(self, insertDto:list) -> object:
        """ Insert record """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def keySelectRecord(self) -> object:
        """ Single record search """
        raise NotImplementedError()

    @abc.abstractmethod
    def multipleSelectRecord(self) -> object:
        """ Multiple record search """
        raise NotImplementedError()

    @abc.abstractmethod
    def updateRecord(self) -> object:
        """ Record update """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def deleteRecord(self) -> object:
        """ Record delete """
        raise NotImplementedError()



