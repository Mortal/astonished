import os
import re
import shutil
import textwrap
import subprocess

import mutagen.easymp4


def main():
    pattern = r'^Dream Theater [-–] (.*) \(Audio\)-.{11}\.m4a$'

    titles = textwrap.dedent("""
        Descent of the NOMACS
        Dystopian Overture
        The Gift of Music
        The Answer
        A Better Life
        Lord Nafaryus
        A Savior in the Square
        When Your Time Has Come
        Act of Faythe
        Three Days
        The Hovering Sojourn
        Brother, Can You Hear Me?
        A Life Left Behind
        Ravenskill
        Chosen
        A Tempting Offer
        Digital Discord
        The X Aspect
        A New Beginning
        The Road to Revolution
        2285 Entr'acte
        Moment of Betrayal
        Heaven's Cove
        Begin Again
        The Path That Divides
        Machine Chatter
        The Walking Shadow
        My Last Farewell
        Losing Faythe
        Whispers in the Wind
        Hymn of a Thousand Voices
        Our New World
        Power Down
        Astonishing
    """.strip('\n')).splitlines()
    titles_lower = [t.lower().strip('?') for t in titles]
    indir = 'orig'
    for filename in os.listdir(indir):
        mo = re.match(pattern, filename)
        if not mo:
            continue
        i = titles_lower.index(mo.group(1).lower())
        infile = os.path.join(indir, filename)
        tagger = mutagen.easymp4.EasyMP4(infile)
        tagger['artist'] = 'Dream Theater'
        tagger['album'] = 'The Astonishing'
        tagger['date'] = '2016'
        if titles[i] == 'Whispers in the Wind':
            tagger['title'] = titles[i].replace('in', 'on')
        else:
            tagger['title'] = titles[i]
        if i < 20:
            t = i + 1
            tot = 20
            d = 1
        else:
            t = i - 19
            tot = 14
            d = 2
        tagger['tracknumber'] = '%s/%s' % (t, tot)
        tagger['discnumber'] = '%s/2' % d
        f = '%d-%02d. %s.m4a' % (d, t, mo.group(1))
        print('%s -> %s' % (infile, f))
        shutil.copyfile(infile, f)
        shutil.copystat(infile, f)
        tagger.save(f)


if __name__ == "__main__":
    main()
