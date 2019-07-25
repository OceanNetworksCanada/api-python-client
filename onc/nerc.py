#-------------------------------------------------------------------------------
# Name:        nerc
# Purpose:     This class provides access to NERC vocabulary server collections and terms
#
# Author:      ryanross
#
# Created:     17/11/2016
# Copyright:   (c) Ocean Networks Canada 2016
# Licence:     none
# Requires:    requests library - [Python Install]\scripts\pip install requests
#              xmljson library - [Python Install]\scripts\pip install xmljson
#-------------------------------------------------------------------------------

import requests
import json
from xml.etree.ElementTree import fromstring, ElementTree
import sys
if sys.version_info.major == 2:
    from V2 import util
else:
    from onc.V3 import util

import xmljson

#Example URLs
#Device : http://vocab.nerc.ac.uk/collection/L22/current/TOOL0861/
#Device Category: http://vocab.nerc.ac.uk/collection/L05/current/130/
#

skos = '{http://www.w3.org/2004/02/skos/core#}'
rdf = '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'
dc = '{http://purl.org/dc/terms/}'
owl="{http://www.w3.org/2002/07/owl#}"
grg="{http://www.isotc211.org/schemas/grg/}"
rdfs="{http://www.w3.org/2000/01/rdf-schema#}"

class NERC:
    def __init__(self, url= "http://vocab.nerc.ac.uk/"):
        self.baseUrl = url

    def main(self):
        pass

    def getCollections(self):
    
        coll = []
        url='{}collection'.format(self.baseUrl)
        parameters = {}
    
        response = requests.get(url,params=parameters)
        if (response.ok):
            payload = fromstring(response.content)
            
            bf = xmljson.BadgerFish()
            dict = bf.data(payload)
            
            for collection in dict['{0}RDF'.format(rdf)]['{}Collection'.format(skos)]:
                dicCol = {'url':collection['@{}about'.format(rdf)]}
                
                tags=[[skos,'prefLabel'],
                      [dc,'title'],
                      [skos,'altLabel'],
                      [dc,'alternative'],
                      [dc,'description'],
                      [dc,'creator'],
                      [grg,'RE_RegisterOwner'],
                      [rdfs,'comment'],
                      [dc,'publisher'],
                      [owl,'versionInfo'],
                      [dc,'date']]
                for tag in tags:
                    key='{}{}'.format(tag[0],tag[1])
                    if key in collection:
                        val = collection[key]
                        if val is not None: dicCol[tag[1]]=val['$']                        
                  
                for t in ['broader','narrower','sameAs','related']:
                    key='{0}{1}'.format(skos,t)
                    if (key in collection.keys()):
                        term = collection[key]
                        if (term):
                            if (len(term)==1):
                                dicCol['{}Term'.format(t)]=term['@{}resource'.format(rdf)]
                            else:
                                terms = [i["@{}resource".format(rdf)] for i in term]
                                dicCol['{}Term'.format(t)]=[s for s in sorted(terms)]
    
                coll.append(dicCol)  
        else:
            util.printErrorMessage(response,{})
    
        return coll
    
    
    def getTerm(self,collection,version,term):
        url='{}collection/{}/{}/{}/'.format(self.baseUrl,collection,version,term)
        return self.getTermFromUrl(url)
    
    def getTermFromUrl(self,url):
        dicTerm = None
        response = requests.get(url,params={})
        if (response.ok):
            payload = fromstring(response.content)
            
            bf = xmljson.BadgerFish()
            dict = bf.data(payload)
            concept = dict['{0}RDF'.format(rdf)]['{0}Concept'.format(skos)]
            if concept:
                dicTerm = {'url':concept['@{}about'.format(rdf)]}
                
                tags=[[skos,'prefLabel'],
                      [skos,'definition'],
                      [dc,'identifier'],
                      [owl,'versionInfo']]
                for tag in tags:
                    key='{}{}'.format(tag[0],tag[1])
                    try:
                        if key in concept:
                            val = concept[key]
                            if val is not None: dicTerm[tag[1]]=val['$']
                    except:
                        print('error retrieving key: {}'.key)                    
                  
                for t in ['broader','narrower','sameAs','related']:
                    key='{0}{1}'.format(skos,t)
                    if (key in concept.keys()):
                        term = concept[key]
                        if (term):
                            if (len(term)==1):
                                dicTerm['{}Term'.format(t)]=term['@{}resource'.format(rdf)]
                            else:
                                terms = [i["@{}resource".format(rdf)] for i in term]
                                dicTerm['{}Term'.format(t)]=[s for s in sorted(terms)]
    
        else:
            util.printErrorMessage(response,{})
    
    
        return dicTerm
    
    
    def getBroaderTerm(self,collection,version,term):
        lstTerms = []
        url='{}collection/{}/{}/{}/'.format(self.baseUrl,collection,version,term)
    
        response = requests.get(url,params={})
        if (response.ok):
            payload = fromstring(response.content)
            
            bf = xmljson.BadgerFish()
            dict = bf.data(payload)
            concept = dict['{0}RDF'.format(rdf)]['{0}Concept'.format(skos)]
            if concept:
                broaderTerms=[]
                key='{0}broader'.format(skos)
                if (key in concept.keys()):
                    term = concept[key]
                    if (term):
                        if (len(term)==1):
                            broaderTerms=[term['@{}resource'.format(rdf)]]
                        else:
                            terms = [i["@{}resource".format(rdf)] for i in term]
                            broaderTerms=[s for s in sorted(terms)]
                
                lstTerms = [self.getTermFromUrl(t) for t in broaderTerms]
    
        return lstTerms

if __name__ == '__main__':
    pass
    
