'''
Org post to blog post conversationator

TODO: don't hardcode paths, enforce config file or env variables, etc.
TODO: figure out how to do feature image
TODO: figure out how to do embedded images
TODO: it would be nice to make everything more OOP - e.g. OrgFile, Entry, EntryGame classes...?
'''

import datetime
import os
import re

class Image:
    def __init__(self, text, link):
        self.text = text
        self.link = link
        self.thumbnail_image = self.link if 'imgur' not in self.link else self.link[:-4] + 'm' + self.link[-4:]

    def to_jekyll(self):
        return '''
[![{caption}]({thumbnail})]({link})
        '''.format(caption=self.text, link=self.link, thumbnail=self.thumbnail_image)

class EntryPart:
    def __init__(self, text, images):
        self.text = text
        self.images = images

    def to_jekyll(self):
        jekyll_string = self.text + '\n'

        if len(self.images) > 0:
            for image in self.images[0:2]:
                jekyll_string += image.to_jekyll()

        return jekyll_string

class Game:
    def __init__(self, title, platform, parts):
        self.title = title
        self.platform = platform
        self.parts = parts

    def to_jekyll(self):
        jekyll_string = '### ' + self.title + ' ' + '*(' + self.platform + ')*'
        jekyll_string += '\n\n'
        for part in self.parts:
            jekyll_string += part.to_jekyll()
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
        elif ch in ['*', '\r', '[', ':']:
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
    title_prog = re.compile('\*\*(.+)\*\* \*\((.+)\)\* - ')
    prog = re.compile('(\\[([^\\[\\]]+)\\])(\\(([^\\(\\)]+)\\))')
    for line in entry_text.split('\n'):
        if len(line) == 0:
            continue

        parts = []
        title_match = title_prog.match(line)
        title = title_match.group(1)
        platform = title_match.group(2)
        line = line.replace(title_match.group(0), '')

        part_text = ''
        images = []

        for part in line.split('. '):
            for match in prog.findall(part):
                part = part.replace(match[0], match[1])
                part = part.replace(match[2], '')
                images.append(Image(match[1], match[3]))
            part_text += part + '. '
            if len(images) > 0:
                parts.append(EntryPart(part_text, images))
                part_text = ''
                images = []

        if len(part_text) > 0:
            parts.append(EntryPart(part_text, images))

        games.append(Game(title, platform, parts))
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

frontmatter = '''---
layout: post
title: What I'm Playing - {date.month}/{date.day}/{date.year}
date: {date.year}-{date.month}-{date.day}
categories: ["What I'm Playing"]
tags: ["video games"]
summary: {summary}
comments: true
pinned: false
---
'''.format(date=datetime.datetime.today(), summary=found_summary)

post_file = "{0.year}-{0.month}-{0.day}-what-im-playing.md".format(datetime.datetime.today())

with open(os.path.join(post_dir, post_file), 'w') as file:
    file.write(frontmatter)
    for game in found_games:
        file.write(game.to_jekyll())
