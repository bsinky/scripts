'''
Org post to blog post conversationator
'''

import datetime
import os

def get_summary(summary_text):
    final_summary = ''
    break_word = False
    for ch in summary_text:
        if len(final_summary) >= 100:
            break_word = True
        if ch == '\n':
            final_summary += ' '
        elif ch == '*' or ch == '\r':
            pass
        elif break_word and (ch == ' ' or ch == '.'):
            final_summary += '...'
            break
        else:
            final_summary += ch
    return final_summary

orgfile = None
postdir = None

if os.name == 'posix':
    # TODO: handle Linux setup
    orgfile = '/home/bens/org/BrosGamingClub.org'
    postdir = '/home/bens/Documents/Development/bsinky.github.io/_posts'
else:
    # assume windows
    orgfile = 'C:\\Users\\Ben\\org\\BrosGamingClub.org'
    postdir = 'D:\\Users\\Ben\\Documents\\Development\\bsinky.github.io\\_posts'

searchfile = open(orgfile, 'r')
found_initial_week = False
is_within_week = False
found_string = ''

for line in searchfile:
    # print line
    if line.startswith("*** Week of"):
        found_initial_week = True
        is_within_week = True
        found_string = ''
        continue
    elif found_initial_week and line.startswith("** "):
        is_within_week = False
        break

    if is_within_week:
        found_string += line

frontmatter = '''---
layout: post
title: What I'm Playing - {0.month}/{0.day}
date: {0.year}-{0.month}-{0.day}
categories: ["gaming"]
tags: ["gaming"]
summary: {1}
comments: true
pinned: false
---
'''.format(datetime.datetime.today(), get_summary(found_string))
# print frontmatter + found_string

post_file = "what-im-playing-{0.year}-{0.month}-{0.day}.md".format(datetime.datetime.today())

with open(os.path.join(post_dir, post_file), 'w') as file:
    file.write(frontmatter + found_string)
