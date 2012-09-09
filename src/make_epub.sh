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

EPUB_DIR=$1
EPUB_NAME=$2
ROOT_DIR=$PWD
rm $EPUB_NAME
cd $EPUB_DIR
zip -0Xq $EPUB_NAME mimetype 
zip -Xqr9D $EPUB_NAME META-INF/ OEBPS/
java -jar $ROOT_DIR/epubcheck/epubcheck-3.0b5 $EPUB_NAME
