#!/usr/bin/python
#
# Copyright (c) 2012, GEM Foundation.
#
# Author, Matteo Nastasi <nastasi@openquake.org>, 
#                        <nastasi@alternativeoutput.it>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABLILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details. 
#

import libxml2
import sys


def swap_elements(doc, el_a, el_b):
    tmp_a = el_a.docCopyNode(doc, 1);
    tmp_b = el_b.docCopyNode(doc, 1);

    el_a.replaceNode(tmp_b);
    el_b.replaceNode(tmp_a);

    return (tmp_b, tmp_a)

def compare_elements(el_a, el_b):
    if el_a == None or el_b == None:
        return 0

    if el_a.type == 'text' or el_b.type == 'text':
        # if elements are both strings compare them
        if el_a.type == el_b.type:
            if el_a.content > el_b.content:
                return 1
            elif el_a.content < el_b.content:
                return -1
            else:
                return 0
        else:
            return 0

    # --- compare tag name ---
    if el_a.name > el_b.name:
        return 1
    elif el_a.name < el_b.name:
        return -1
    
    # --- if tags are equals compare attributes ---
    at_a = el_a.properties
    at_b = el_b.properties
    
    while at_a != None and at_b != None:
        if at_a.name > at_b.name:
            return 1
        elif at_a.name < at_b.name:
            return -1
        at_a = at_a.next
        at_b = at_b.next

    if (at_a == None and at_b != None) or (at_a != None and at_b == None):
        if at_a == None:
            return -1
        else:
            return 1

    # --- if attributes are equal try to compare content of attrs ---
    at_a = el_a.properties
    at_b = el_b.properties
        
    while at_a != None and at_b != None:
        if at_a.content > at_b.content:
            return 1
        elif at_a.content < at_b.content:
            return -1
        at_a = at_a.next
        at_b = at_b.next

    # --- if all tag, attributes and attributes values are equal start to compare elements ---
    sub_a = el_a.get_children()
    sub_b = el_b.get_children()
    while sub_a != None and sub_b != None:
        ret = compare_elements(sub_a, sub_b)
        if ret != 0:
            return ret
        sub_a = sub_a.next
        sub_b = sub_b.next
        

    # print "compare_elements return EQUAL: "
    # el_a.debugDumpNode(sys.stdout, 5)
    # print "---------------------------"
    # el_b.debugDumpNode(sys.stdout, 5)
    # print "---------------------------"

    return 0

def sort_element(doc, el):
    # print "ENTER"
    if el == None:
        # print "EXIT"
        return True
    
    if el.type == 'text':
        # print "EXIT"
        return True

    # print "sort element: [%s]" % el.name
    # --- sort attributes ---
    attr_a = el.get_properties()
    while attr_a != None:
        # print "attr_a: %s\n" % attr_a.name
        attr_b = attr_a.next
        while attr_b != None:
            # print "Compare: %s %s\n" % (attr_b.name, attr_a.name)
            
            #  or ( attr_a.name == attr_b.name and attr_a.content > attr_b.content) -> redifinition is denied
            if attr_a.name > attr_b.name: 
                # print "Swap attr: %s %s" % (attr_b.name, attr_a.name)
                (attr_a, attr_b) = swap_elements(doc, attr_a, attr_b)
            attr_b = attr_b.next
        attr_a = attr_a.next

    # --- sort children ---
    sub = el.get_children()
    while sub != None:
        sort_element(doc, sub)
        sub = sub.next

    # doc.dump(sys.stdout)
    # print "---------------------\n"

    sub_a = el.get_children()
    # print "EL: %s" % el.name
    while sub_a != None:
        # print "Zub_a: %s" % (sub_a.name)
        sub_a = sub_a.next
    # print

    sub_a = el.get_children()
    ct=1
    while sub_a != None:
        # print "sub_a: %s (%d)" % (sub_a.name, ct)
        if sub_a.type == 'text':
            sub_a = sub_a.next
            ct += 1
            continue
        sub_b = sub_a.next
        while sub_b != None:
            if sub_b.type == 'text':
                sub_b = sub_b.next
                continue
            # print "  sub_b: %s" % sub_b.name
            # print "Compare: %s %s" % (sub_a.name, sub_b.name)
            if compare_elements(sub_a, sub_b) > 0:
                # print "Swap elem: %s(%s) %s(%s)" % (sub_a.name, sub_a.content, sub_b.name, sub_b.content)            
                (sub_a, sub_b) = swap_elements(doc, sub_a, sub_b)
                
            sub_b = sub_b.next
        sub_a = sub_a.next
        # print
        ct += 1

    # print "EXIT"
    return True



#
#  MAIN
#

def main():
    debug=False
    
    doc = libxml2.parseFile(sys.argv[1])
    if debug:
        sys.stderr.write("vvvvvvv\n")
        sys.stderr.write(doc.serialize(None, 2)[22:])
        sys.stderr.write("^^^^^^^\n")

    root = doc.getRootElement() 
    sort_element(doc, root)
    ret = doc.serialize(None, 2)[22:]
    if debug:
        sys.stderr.write("vvvvvvv\n")
        sys.stderr.write("%s" % ret)
        sys.stderr.write("^^^^^^^\n")

    if len(sys.argv) > 2:
        fout = file(sys.argv[2], "w")
    else:
        fout = sys.stdout

    fout.write("%s" % ret)
    fout.close()

    sys.exit(0)

main()
