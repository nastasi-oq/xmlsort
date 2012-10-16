#!/bin/bash
#
# xmlsort - regress.sh
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

#
# DESCRIPTION
#
#   This script is provided as facility to test xmlsort.
#
# HOW TO ADD A NEW CASE
#
#   1. create a new xml source if needed and save it into "xml" directory
#   2. create a new couple of "com" and "exp" variables with the command-
#      line that you want to test and with exp+=('xxx') to force the dump
#      of the xmlsort output
#   3. run the regress.sh script and verify if the output is correct
#   4. to add dumped result into the exp-ected array run:
#      ./regress.sh | sed 's/\\/\\\\/g;s/$/\\n/g' | tr -d '\n'
#      and copy the received part into the new 'exp' element
#

declare -a exp com

verbose=0
if [ "$1" = "-v" ]; then
    verbose=1
fi

echo
echo "Regression of --include option"

com+=('./xmlsort.py xml/sample06.xml - -i "/a" 1')
exp+=("$(echo -e "<a>\n  <e>\n    <sub_e>SUB_E CONT</sub_e>\n  </e>\n  <d>\n    <sub_d>SUB_D CONT</sub_d>\n  </d>\n  <c>\n    <g>G CONT</g>\n    <f>F CONT</f>\n  </c>\n  <b>\n    B CONT\n  </b>\n</a>")")

com+=('./xmlsort.py xml/sample06.xml - -i "/a" 2')
exp+=("$(echo -e "<a>\n  <b>\n    B CONT\n  </b>\n  <c>\n    <g>G CONT</g>\n    <f>F CONT</f>\n  </c>\n  <d>\n    <sub_d>SUB_D CONT</sub_d>\n  </d>\n  <e>\n    <sub_e>SUB_E CONT</sub_e>\n  </e>\n</a>\n")")

com+=('./xmlsort.py xml/sample06.xml - -i "/a" 3')
exp+=("$(echo -e "<a>\n  <b>\n    B CONT\n  </b>\n  <c>\n    <f>F CONT</f>\n    <g>G CONT</g>\n  </c>\n  <d>\n    <sub_d>SUB_D CONT</sub_d>\n  </d>\n  <e>\n    <sub_e>SUB_E CONT</sub_e>\n  </e>\n</a>")")

# com+=('./xmlsort.py xml/sample06.xml - -i "/a",1')
# exp+=('xxx')

to=$((${#com[*]} - 1))
for i in $(seq 0 $to); do
    echo -n "  \"${com[$i]}\" ... "
    ret="$(eval ${com[$i]})"
    if [ "$ret" != "${exp[$i]}" ]; then
        echo "Ko."
        echo "expected [${exp[$i]}]"
        echo "received [$ret]"
        exit 1
    else
        echo Ok.
        if [ $verbose -eq 1 ]; then
            echo "expected [${exp[$i]}]"
            echo "received [$ret]"
        fi
    fi
done

exit 0