#! usr/bin/env python

import os
import os.path

screen_dir = "/home/bens/Pictures/3ds" if os.name == "posix" else "F:\\Pictures\\Screenshots\\3ds"
screen_suffix = "_top.bmp"
ntr_screen_prefix = "top_"

for filename in os.listdir(screen_dir):
    is_luma = filename.endswith(screen_suffix)
    is_ntr = filename.startswith(ntr_screen_prefix)

    if not is_luma and not is_ntr:
        continue

    top_screen = os.path.join(screen_dir, filename)
    bot_screen = os.path.join(screen_dir, filename[:-len(screen_suffix)] + "_bot.bmp") if is_luma else os.path.join(screen_dir, "bot_" + filename[len(ntr_screen_prefix):])
    output_screen = os.path.join(screen_dir, filename + "_combined.png")

    if os.path.isfile(top_screen) and os.path.isfile(bot_screen):
        pass
    else:
        print "couldn't find both parts, skipping...%s" % filename
        continue

    command = "magick convert \"{top}\" -gravity center -background None \"{bot}\" -append \"{out}\"".format(top=top_screen,bot=bot_screen,out=output_screen)
    result_code = os.system(command)

    if (result_code == 0):
        pass
        os.remove(top_screen)
        os.remove(bot_screen)
    else:
        print "Error, command returned: {}".format(result_code)

