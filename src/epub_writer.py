import os
import shutil
import string

def prepare_output(output_dir):
    'Creates the directory structure and copies stock files'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_dir + "/META-INF", exist_ok=True)
    os.makedirs(output_dir + "/OEBPS", exist_ok=True)
    shutil.copy("ref/mimetype", output_dir)
    shutil.copy("ref/META-INF/container.xml", output_dir + "/META-INF")

def write_header(title, f):
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.1//EN' 'http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd'>\n")
    f.write("<html xmlns='http://www.w3.org/1999/xhtml'>\n")
    f.write("<head>\n")
    f.write("<title>" + title + "</title>\n")
    f.write("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>\n")
    f.write("</head>\n")
    f.write("<body>\n")

def write_html(output_dir, title, chunks):
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

def write_content_opf(output_dir, title, chunks):
    manifest_contents = ""
    spine_contents = ""
    for chunk in chunks:
        manifest_contents += '\t<item id="' + chunk.name() + '" href="' + chunk.file_name() + '" media-type="application/xhtml+xml" />\n'
        spine_contents += '\t<itemref idref="' + chunk.name() + '"/>\n'
    
    with open("ref/content.opf") as f:
        content_opf_txt =  f.read()
        content_opf_template = string.Template(content_opf_txt)
        output = content_opf_template.safe_substitute(title=title, manifest_contents = manifest_contents, spine_contents = spine_contents)
        with open(output_dir + "/OEBPS/content.opf", "w") as f:
            f.write(output)



def write_toc_ncx(output_dir, title, chunks):
    navPoints = ""
    for i, chunk in enumerate(chunks):
        navPoints += '\t\t<navPoint id="' + chunk.name() + '" playOrder="' + str(i) + '">\n' + '<navLabel> <text>' + chunk.title + '</text>\n' + '</navLabel>\n' + '<content src="' + chunk.file_name() + '"/>\n' + '</navPoint>\n'
 
    with open("ref/toc.ncx") as f:
        toc_ncx_txt =  f.read()
        toc_ncx_template = string.Template(toc_ncx_txt)
        output = toc_ncx_template.safe_substitute(title=title, navPoints = navPoints)
        with open(output_dir + "/OEBPS/toc.ncx", "w") as f:
            f.write(output)

def write_output(output_dir, title, chunks):
    prepare_output(output_dir)
    write_html(output_dir, title, chunks)
    write_content_opf(output_dir, title, chunks)
    write_toc_ncx(output_dir, title, chunks)
