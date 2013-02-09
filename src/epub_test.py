#! /usr/bin/env python3

#    Copyright (C) 2012 Vraj Mohan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from make_epub import replace_opening_and_closing_double_quotes

class EpubTest(unittest.TestCase):

    def test_pretty_quote(self):
        self.assertEqual('Hello', replace_opening_and_closing_double_quotes('Hello'), "Nothing to do")
        self.assertEqual('“How do you do?” he said.', replace_opening_and_closing_double_quotes('"How do you do?" he said.'), "Double quotes are replaced")
        self.assertEqual('“How do you do?', replace_opening_and_closing_double_quotes('"How do you do?'), "Opening quote left hanging")
        self.assertEqual("'How do you do?' he said.", replace_opening_and_closing_double_quotes("'How do you do?' he said."), "Single quotes are not replaced")
        

if __name__ == '__main__':
    unittest.main()
