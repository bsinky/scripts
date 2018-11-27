'''
Org post to blog post conversationator

TODO: don't hardcode paths, enforce config file or env variables, etc.
TODO: figure out how to do feature image
TODO: figure out how to do embedded images
TODO: it would be nice to make everything more OOP - e.g. OrgFile, Entry, EntryGame classes...?
'''

import datetime
import os

def parse_entry(summary_text):
    final_summary = ''
    found_images = []
    current_image = ''
    break_word = False
    potential_image_link = False
    in_image_link = False
    for ch in summary_text:
        if len(final_summary) >= 650:
            break_word = True
        if ch == '\n':
            final_summary += ' '
        elif ch == '*' or ch == '\r' or ch == '[':
            pass
        elif ch == ']':
            potential_image_link = True
        elif ch == '(':
            if potential_image_link:
                in_image_link = True
            else:
                final_summary += ch
            potential_image_link = False
        elif in_image_link:
            if ch == ')':
                in_image_link = False
                found_images.append(current_image)
                current_image = ''
            else:
                current_image += ch
        elif break_word and (ch == ' ' or ch == '.'):
            final_summary += '...'
            break
        else:
            final_summary += ch
    return (final_summary, found_images)

def parse_org_file(org_file_path):
    found_string = ''

    with open(org_file_path, 'r') as searchfile:
        found_initial_week = False
        is_within_week = False

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

    return found_string

orgfile = None
post_dir = None

if os.name == 'posix':
    # TODO: handle Linux setup
    orgfile = '/home/bens/org/BrosGamingClub.org'
    post_dir = '/home/bens/Documents/Development/bsinky.github.io/_posts'
else:
    # assume windows
    orgfile = 'C:\\Users\\Ben\\org\\BrosGamingClub.org'
    post_dir = 'D:\\Users\\Ben\\Documents\\Development\\bsinky.github.io\\_posts'

found_entry = parse_org_file(orgfile)
(found_summary,found_images) = parse_entry(found_entry)

print found_images

image_frontmatter = '''image:
  feature: {}'''.format(found_images[0]) if len(found_images) > 0 else ''

frontmatter = '''---
layout: post
title: What I'm Playing - {date.month}/{date.day}/{date.year}
date: {date.year}-{date.month}-{date.day}
categories: ["What I'm Playing"]
tags: ["video games"]{image}
summary: {summary}
comments: true
pinned: false
---
'''.format(date=datetime.datetime.today(), summary=found_summary, image='')
# print frontmatter + found_string

post_file = "{0.year}-{0.month}-{0.day}-what-im-playing.md".format(datetime.datetime.today())

with open(os.path.join(post_dir, post_file), 'w') as file:
    file.write(frontmatter + found_entry)
