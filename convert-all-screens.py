#! usr/bin/env python

import os
import os.path

screen_dir = "/home/bens/Pictures/3ds"
screen_suffix = "_top.bmp"

for filename in os.listdir(screen_dir):
    if not filename.endswith(screen_suffix):
        continue
    top_screen = os.path.join(screen_dir, filename)
    bot_screen = os.path.join(screen_dir, filename[:-len(screen_suffix)] + "_bot.bmp")
    output_screen = os.path.join(screen_dir, filename + "_combined.png")

    if os.path.isfile(top_screen) and os.path.isfile(bot_screen):
        pass
    else:
        print "couldn't find both parts, skipping...%s" % filename
        continue

    command = "convert \"{top}\" -gravity center -background None \"{bot}\" -append \"{out}\"".format(top=top_screen,bot=bot_screen,out=output_screen)
    result_code = os.system(command)

    if (result_code == 0):
        os.remove(top_screen)
        os.remove(bot_screen)
    else:
        print "Error, command returned: {}".format(result_code)

