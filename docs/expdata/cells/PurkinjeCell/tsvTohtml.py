# ~/docs/expdata/cells/PurkinjeCell/tsvTohtml.py
##############################################################################
#                        HOW TO USE THIS SCRIPT
# python tsvTohtml.py "desired_data.txt" "Some dummy title"
##############################################################################
from pdb import set_trace as breakpoint
import os
from sys import argv
import csv
from html import escape
from collections import OrderedDict
#from json2html import json2html
from bs4 import BeautifulSoup as bs

thispythonfile, filename, title_content = argv

pwd = os.getcwd() # ~/cerebunitdata/docs/expdata/cells/PurkinjeCell

######################### LOAD DATA, i.e., JSON FILE ##########################
os.chdir("../../../..") # this moves you to ~/cerebunitdata
filepath = os.getcwd()+ os.sep + "expdata" + os.sep + "cells" + os.sep + \
           "PurkinjeCell" + os.sep + filename #"Llinas_Sugimori_1980_soma_IvsV_Fig3E.txt"
#rawdata = open(filepath, "r", encoding="utf-8")
#jsondata = json.load(rawdata) # <- THIS WILL BE PASSED DOWN
#rawdata.close()
dlist = []
with open(filepath, newline="") as f:
    data = csv.DictReader(f, delimiter="\t")
    for row in data: # Note: Python >= 3.8 row is a dict
        #dlist.append(dict(row))
        dlist.append( OrderedDict(row) )
os.chdir(pwd) # return to ~/cerebunitdata/docs/expdata/cells/PurkinjeCell
#print( len(dlist) )
#breakpoint()
######################
def html_table(ddict): # dlist[0]
    "https://stackoverflow.com/questions/44320329/converting-csv-to-html-table-in-python"
    clmn_names = []
    for row in ddict:
        for name in row.keys():
            if name not in clmn_names:
                clmn_names.append( name )
    html_lines = []
    html_lines.append("<table>\n")
    html_lines.append("  <tr>\n")
    for name in clmn_names:
        html_lines.append("   <th>{}</th>\n".format(escape(name)))
    html_lines.append("  </tr>\n")
    for row in ddict:
        html_lines.append("  <tr>\n")
        for name in clmn_names:
            value = row.get(name, "")
            html_lines.append("   <td>{}</td>\n".format(escape(value)))
        html_lines.append("  </tr>\n")
    html_lines.append("</table>")
    return "".join(html_lines)

######################### CREATE THE HTML CONTAINER  ##########################
structure = """
            <html>
            <head><title>Dummy Title</title>
            <body></body>
            </html>
            """
soup = bs(structure, features="lxml")
title = soup.find("title")
body = soup.find("body")

###################### INSERT TITLE INTO HTML CONTAINER #######################
title.insert(0, title_content)

######################### CONVERT JSON DATA TO HTML  ##########################
#htmltable = json2html.convert(json = jsondata)
#htmltable = json2html.convert(json = dlist[0])
htmltable = html_table( dlist )
extrasoup = bs(htmltable, "html.parser")

###################### INSERT TABLE INTO HTML CONTAINER #######################
body.insert(0, extrasoup)

####################### FINALLY WRITE INTO HTML FILE  #########################
#savefile = pwd + os.sep + "rawhtmls" + os.sep + filename.replace(".json",".html")
savefile = pwd + os.sep + "rawhtmls" + os.sep + filename.replace(".txt",".html")
html = open( savefile, "w", encoding="utf-8" )
html.write( str(soup) )
