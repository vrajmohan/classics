#! /usr/bin/env python3
import argparse
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

def pretty_quote(str):
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
    with open(source_file) as f:
        paragraphs = []
        para = ""
        for line in f:
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
        pretty_quoted_str = pretty_quote(em_dashed_str)
        italicized_str = re.sub(r'_(.*?)_', r'<i>\1</i>', pretty_quoted_str)
        pretty_paragraphs.append(italicized_str)
    return pretty_paragraphs

def split_into_chunks(paragraphs):
    #chapter_pat = re.compile('[IVXLC]+\.|Book the')
    chapter_pat = re.compile('CHAPTER [A-Z]+|BOOK [A-Z]+')
    #chapter_pat = re.compile('THE STORY [ A-Z]*|THE NARRATIVE [ A-Z]*')
    #chapter_pat = re.compile('Chapter [0-9]+|Part [0-9]+')
    #chapter_pat = re.compile('[0-9]+ .*')
    #chapter_pat = re.compile('^CHAPTER [0-9]+')
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

arg_parser = argparse.ArgumentParser(description="Create epub from Project Gutenberg style text")
arg_parser.add_argument("source", help = "the source text file to parse")
arg_parser.add_argument("title", help = "the epub title to create")
arg_parser.add_argument("output", help = "the directory in which the exploded epub will be created")
args = arg_parser.parse_args()

source_file=args.source
title=args.title
output_dir=args.output

raw_paragraphs = extract_paragraphs(source_file)
pretty_paragraphs = make_pretty(raw_paragraphs)
chunks = split_into_chunks(pretty_paragraphs)
epub_writer.write_output(output_dir, title, chunks)

