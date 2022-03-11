#!/usr/bin/python3

import json
#import yaml


class Setting:
    def __init__(self):
        f = open('./conf/settings.json')
        self.data = json.load(f)
        f.close()
    
    def getGatewayName(self):
        return self.data['gateway']['name']

    def getClientID(self):
        return self.data['gateway']['client_id']

    def getGatewayHost(self):
        return self.data['gateway']['host']

    def getDefaultKeys(self):
        return self.data['gateway']['default_keys']

    def getGatewayCredentials(self):
        userData = dict(); 
        userData['usr'] = ""
        userData['passwd'] = ""

        if self.isSecure() :
            userData['usr'] = self.data['gateway']['security']['username']
            userData['passwd'] = self.data['gateway']['security']['password']
        return userData
    
    def isSecure(self):
        return self.data['gateway']['security']['isSecure']

    def getSslStatus(self):
        return self.data['gateway']['ssl']['certificates']

    def getProtocolPort(self, protocol):
        return self.data['gateway']['protocols'][protocol]['port']

    def getProtocolTopic(self, protocol):
        return self.data['gateway']['protocols'][protocol]['topic_name']
    
    def getProtocolCredentials(self, protocol):
        userData = dict(); 
        userData['usr'] = ""
        userData['passwd'] = ""
        
        securityObj = self.data['gateway']['protocols'][protocol]['security']

        if self.isProtocolSecure(protocol):
            userData['usr'] = securityObj['username']
            userData['passwd'] = securityObj['password']
            
        return userData

    def isProtocolSecure(self, protocol):
        return self.data['gateway']['protocols'][protocol]['security']['isSecure']

    def getCertificates(self):
        if self.getSslStatus():
            caCert = self.data['gateway']['ssl']['caCert']
            cert = self.data['gateway']['ssl']['cert']

            return caCert,  cert

        return None


    def getBrokerInfo(self):
        return self.getBrokerName() + "\n" + self.getBrokerHost() + "\n" + self.getBrokerPort() + "\n" + self.getBrokerTopic() + "\n" +self.getBrokerID() + "\n" + str(self.isSecure()) + "\n" + str(self.getSslStatus())
