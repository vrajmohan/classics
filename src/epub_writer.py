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

import os
import shutil
import string
import tempfile
import zipfile

def prepare_output(output_dir):
    'Creates the directory structure and copies stock files'
    os.makedirs(output_dir + "/META-INF", exist_ok=True)
    os.makedirs(output_dir + "/OEBPS", exist_ok=True)
    shutil.copy("ref/mimetype", output_dir)
    shutil.copy("ref/META-INF/container.xml", output_dir + "/META-INF")
    shutil.copy("ref/OEBPS/style.css", output_dir + "/OEBPS")
    shutil.copy("ref/OEBPS/cc.png", output_dir + "/OEBPS")

def write_header(title, f):
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN' 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n")
    f.write("<html xmlns='http://www.w3.org/1999/xhtml'>\n")
    f.write("<head>\n")
    f.write("<title>" + title + "</title>\n")
    f.write("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>\n")
    f.write("<link type='text/css' rel='stylesheet' href='style.css' />\n")
    f.write("</head>\n")
    f.write("<body>\n")

def write_html(chunks, output_dir, title):
    for chunk in chunks:
        with open(output_dir + "/OEBPS/" + chunk.file_name(), "w") as f:
            write_header(title, f)
            f.write("<h2>")
            f.write(chunk.content[0])
            f.write("</h2>")
            for para in chunk.content[1:]:
                f.write("<p>")
                f.write(para)
                f.write("</p>")
                f.write("\n")
            f.write("</body>\n</html>")

def write_front_matter(output_dir, title, author):
    with open("ref/title.html") as f:
        title_txt =  f.read()
        title_template = string.Template(title_txt)
        output = title_template.safe_substitute(title = title, author = author)
        with open(output_dir + "/OEBPS/title.html", "w") as f:
            f.write(output)

    with open("ref/colophon.html") as f:
        colophon_txt =  f.read()
        colophon_template = string.Template(colophon_txt)
        output = colophon_template.safe_substitute(title = title)
        with open(output_dir + "/OEBPS/colophon.html", "w") as f:
            f.write(output)

def write_content_opf(chunks, output_dir, title, author, epub_id):
    manifest_contents = ""
    spine_contents = ""
    for chunk in chunks:
        manifest_contents += '\t<item id="' + chunk.name() + '" href="' + chunk.file_name() + '" media-type="application/xhtml+xml" />\n'
        spine_contents += '\t<itemref idref="' + chunk.name() + '"/>\n'
    
    with open("ref/content.opf") as f:
        content_opf_txt =  f.read()
        content_opf_template = string.Template(content_opf_txt)
        output = content_opf_template.safe_substitute(title = title, author = author, epub_id = epub_id, 
            manifest_contents = manifest_contents, spine_contents = spine_contents)
        with open(output_dir + "/OEBPS/content.opf", "w") as f:
            f.write(output)



def write_toc_ncx(chunks, output_dir, title):
    navPoints = ""
    for i, chunk in enumerate(chunks):
        play_order= i + 2 # Account for title which is 1
        navPoints += '\t\t<navPoint id="' + chunk.name() + '" playOrder="' + str(play_order) + '">\n' + '<navLabel> <text>' + chunk.title + '</text>\n' + '</navLabel>\n' + '<content src="' + chunk.file_name() + '"/>\n' + '</navPoint>\n'
 
    with open("ref/toc.ncx") as f:
        toc_ncx_txt =  f.read()
        toc_ncx_template = string.Template(toc_ncx_txt)
        output = toc_ncx_template.safe_substitute(title=title, navPoints = navPoints)
        with open(output_dir + "/OEBPS/toc.ncx", "w") as f:
            f.write(output)

def  generate_epub_name(title):
    epub_name = ''.join(x for x in title if x.isalnum() or x.isspace())
    epub_name = epub_name.replace(' ', '_')
    return epub_name + ".epub"

def create_epub(output_dir, title): 
    epub_name = generate_epub_name(title)
    with zipfile.ZipFile(epub_name, 'w') as zip_file:
        os.chdir(output_dir)
        zip_file.write('mimetype', compress_type=zipfile.ZIP_STORED)
        zip_file.write('META-INF/container.xml', compress_type=zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk('OEBPS'):
            for file_name in files:
                zip_file.write(os.path.join(root, file_name), compress_type=zipfile.ZIP_DEFLATED)

def write_output(chunks, title, author, epub_id):
    with tempfile.TemporaryDirectory() as output_dir:
        prepare_output(output_dir)
        write_html(chunks, output_dir, title)
        write_content_opf(chunks, output_dir, title, author, epub_id)
        write_toc_ncx(chunks, output_dir, title)
        write_front_matter(output_dir, title, author)
        create_epub(output_dir, title)
