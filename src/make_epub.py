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

import argparse
import codecs
import re
import sys
import epub_writer

class Chunk:
    def __init__(self, number, title, content):
        self.number = number
        self.title = title
        self.content = content

    def name(self):
        return "chunk_{:03d}".format(self.number)
        
    def file_name(self):
        return self.name() + ".html"

def replace_opening_and_closing_double_quotes(str):
    'Replaces alternate " in str with “ and ”'
    in_quotes = False
    quoted_str = ""
    for c in str:
        if c == '"':
            if in_quotes:
                quoted_str += '”'
                in_quotes = False
            else:
                quoted_str += '“'
                in_quotes = True
        else:
                quoted_str += c
    return quoted_str

def extract_paragraphs(source_file):
    'Returns the contents of source_file as a list of paragraphs assuming that paragraphs are separated by blank lines'
    with open(source_file, "rb") as f:
        paragraphs = []
        para = ""
        for line in f:
            line = codecs.decode(line, 'utf_8_sig')
            if line.isspace():
                paragraphs.append(para)
                para = ""
            else:
                para += line
        paragraphs.append(para)
        return paragraphs
    
def make_pretty(paragraphs):
    translation_map = str.maketrans("'\n", "’ ")
    pretty_paragraphs = []
    for para in paragraphs:
        joined_str = para.translate(translation_map)
        em_dashed_str = joined_str.replace('--', '—')
        pretty_quoted_str = replace_opening_and_closing_double_quotes(em_dashed_str)
        italicized_str = re.sub(r'_(.*?)_', r'<i>\1</i>', pretty_quoted_str)
        pretty_paragraphs.append(italicized_str)
    return pretty_paragraphs

def split_into_chunks(paragraphs, chapter_regex):
    if chapter_regex:
        chapter_pat = re.compile(chapter_regex)
    else:
        chapter_pat = re.compile('chapter [A-Z]+|chapter [0-9]+|book [A-Z]+|book [0-9]+|part [A-Z]+|part [0-9]+|[0-9]+\.', 
            flags = re.IGNORECASE)

    chunks = []
    i = 0
    content = [paragraphs[0]]
    title = ""
    for para in paragraphs[1:]:
        match = chapter_pat.match(para)
        if match:
            chunk = Chunk(i, title, content)
            chunks.append(chunk)
            i += 1
            content = [para]
            title = para
        else:
            content.append(para)
    chunk = Chunk(i, title, content)
    chunks.append(chunk)
    return chunks


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Create epub from Project Gutenberg style text")
    arg_parser.add_argument("source", help = "the source text file to parse")
    arg_parser.add_argument("-t", "--title", help = "the epub title to create", required=True)
    arg_parser.add_argument("-a", "--author", help = "the author of the title", required=True)
    arg_parser.add_argument("-i", "--epub_id", help = "the epub id of the title", required=True)
    arg_parser.add_argument("-r", "--chapter_regex", help = "the regular expression that identifies the chapters")
    arg_parser.add_argument("-m", "--use_magick", help = "indicates whether imagemagick is to be used to generate the cover", action='store_true')
    return arg_parser.parse_args()

def main():
    args = parse_args()
    source_file=args.source

    raw_paragraphs = extract_paragraphs(source_file)
    pretty_paragraphs = make_pretty(raw_paragraphs)
    chunks = split_into_chunks(pretty_paragraphs, args.chapter_regex)
    epub_writer.write_output(chunks, args.title, args.author, args.epub_id, args.use_magick)

if __name__ == '__main__':
    main()
