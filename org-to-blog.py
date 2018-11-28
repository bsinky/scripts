'''
Org post to blog post conversationator

TODO: don't hardcode paths, enforce config file or env variables, etc.
TODO: figure out how to do feature image
TODO: figure out how to do embedded images
TODO: it would be nice to make everything more OOP - e.g. OrgFile, Entry, EntryGame classes...?
'''

import datetime
import os

class Game:
    def __init__(self, text, images):
        self.text = text
        self.images = images

    def to_jekyll(self):
        jekyll_string = self.text
        jekyll_string += '\n'
        if len(self.images) > 0:
            for image in self.images:
                jekyll_string += '\n'
                jekyll_string += '![image]({image})'.format(image=image)
                jekyll_string += '\n'
        jekyll_string += '\n'
        return jekyll_string

def parse_entry(summary_text):
    final_summary = ''
    break_word = False
    potential_image_link = False
    in_image_link = False
    for ch in summary_text:
        if len(final_summary) >= 650:
            break_word = True
        if ch == '\n':
            final_summary += ' '
        elif ch in ['*', '\r', '[']:
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
            else:
                pass
        elif break_word and (ch == ' ' or ch == '.'):
            final_summary += '...'
            break
        else:
            final_summary += ch
    return final_summary

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

def parse_games(entry_text):
    games = []
    found_images = []
    current_image = ''
    potential_image_link = False
    in_image_link = False
    last_char_was_newline = False
    final_summary = ''
    for ch in entry_text:
        if ch == '\n':
            if last_char_was_newline:
                last_char_was_newline = False
                games.append(Game(final_summary, found_images))
                final_summary = ''
                found_images = []
                current_image = ''
            else:
                last_char_was_newline = True
            continue
        elif ch == '[':
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
        else:
            final_summary += ch
    return games

orgfile = None
post_dir = None

if os.name == 'posix':
    orgfile = '/home/bens/org/BrosGamingClub.org'
    post_dir = '/home/bens/Documents/Development/bsinky.github.io/_posts'
else:
    # assume windows
    orgfile = 'C:\\Users\\Ben\\org\\BrosGamingClub.org'
    post_dir = 'D:\\Users\\Ben\\Documents\\Development\\bsinky.github.io\\_posts'

found_entry = parse_org_file(orgfile)
found_summary = parse_entry(found_entry)
found_games = parse_games(found_entry)

image_frontmatter = ''

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
    file.write(frontmatter)
    for game in found_games:
        file.write(game.to_jekyll())
