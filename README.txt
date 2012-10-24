xmlsort: swiss army knife xml ordering utility
==============================================


Goal
----

Sort an xml file or parts of it to avoid false positive differences comparing it with a previous version (stored in a version control system like GIT or Mercurial).

Did you have some experience changing 1 thing only in a server, dump again data and obtain dozens of changed files like this ?
---------------------------------------------------------
diff --git a/geonode.xml b/geonode.xml
index f4fc60f..ffcdbfc 100644
--- a/geonode.xml    2012-10-24 09:25:42.198961002 +0200
+++ b/geonode.xml    2012-10-24 09:26:58.034957830 +0200
@@ -19,12 +19,12 @@
     <entry key="namespace">http://geonode.org/</entry>
     <entry key="schema">the_schema</entry>
     <entry key="Loose bbox">true</entry>
-    <entry key="Expose primary keys">false</entry>
     <entry key="fetch size">1000</entry>
     <entry key="Max open prepared statements">50</entry>
+    <entry key="Expose primary keys">false</entry>
+    <entry key="user">MYUSER</entry>
     <entry key="preparedStatements">false</entry>
     <entry key="Estimated extends">true</entry>
-    <entry key="user">MYUSER</entry>
     <entry key="min connections">1</entry>
   </connectionParameters>
   <__default>false</__default>
---------------------------------------------------------

xmlsort helps you to avoid this very annoing situations.


Dependencies
------------

xmlsort depends from libxml2 and argparse libraries.


The program
-----------

xmlsort is a single python program.

It can work in some different ways:

    * called without filtering arguments sort all elements of the xml file
    * called with <-i|--include> <xpath> <depth> argument[s] sort matching <xpath> elements only and their children recurring <depth> times
    * called with <-x|--exclude> <xpath> argument[s] sort all elements except elements matching <xpath> and their children

How it works
------------
xmlsort follow few simple steps.

For each node matching –include <xpath> arguments or all if –include is not defined:

    * sort alphabetically attributes of the starting tag
    * if there are sub-elements:
      - recure into each of them (accordingly with the <depth> and with –exclude arguments)
      - sort all sub-elements following the rules:
        + sort all sub-elements comparing tag names
        + if equal comparing attributes name
        + if equal comparing attribute contents
        + if equal comparing sub-elements


Limitations
-----------
    * All kind of implicit sorted lists are not supported (defined by xml schema)
    * Standard input is not supported
    * Packaging is still missing
