EPUB_DIR=$1
EPUB_NAME=$2
ROOT_DIR=$PWD
rm $EPUB_NAME
cd $EPUB_DIR
zip -0Xq $EPUB_NAME mimetype 
zip -Xqr9D $EPUB_NAME META-INF/ OEBPS/
java -jar $ROOT_DIR/epubcheck/epubcheck-1.2.jar $EPUB_NAME
