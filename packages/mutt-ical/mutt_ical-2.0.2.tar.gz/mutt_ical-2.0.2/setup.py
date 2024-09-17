# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mutt_ical']

package_data = \
{'': ['*']}

install_requires = \
['icalendar>=1.0', 'tzlocal>=3.0']

entry_points = \
{'console_scripts': ['viewical = mutt_ical.viewical:main']}

setup_kwargs = {
    'name': 'mutt-ical',
    'version': '2.0.2',
    'description': 'Scripts for helping mutt deal with iCalendar data',
    'long_description': 'mutt-ical\n=========\n\nThis is a collection of scripts that make it easier to work with\n[iCalendar][] files in [mutt][].  (Note that this is for calendar\ninformation in the iCalendar *file format*.  It has nothing to do with the\nOSX calendar program.)\n\n  [iCalendar]: https://en.wikipedia.org/wiki/iCalendar\n  [mutt]: http://www.mutt.org\n\n\nInstallation\n------------\n\nThe recommended installation method is to use [`pipx`][pipx] to install the\nmodule:\n\n    pipx install mutt-ical\n\n  [pipx]: https://pipx.pypa.io/\n\nYou can also use `pip`, which will mingle the module into the current\nPython environment:\n\n    pip install mutt-ical\n\nOr you can download the `.whl` file from the [latest release][].\n\n  [latest release]: https://github.com/asciipip/mutt-ical/releases\n\nFinally, there\'s the manual option:\n\n 1. Install [Poetry](https://python-poetry.org/)\n 2. Clone this repository (`git clone https://github.com/asciipip/mutt-ical.git`)\n 3. In the cloned repo, run `poetry build`\n 4. Install the `.whl` file from the `dist` directory\n\n\nviewical\n--------\n\n`viewical` takes an iCalendar file on standard input and prints out a more\nhuman-friendly rendering of the data in the file.  It\'s intended to be\nused as a display filter in mutt.\n\n### Usage\n\nThis is easiest if you maintain a mutt-specific mailcap, e.g. having this\nin your `~/.muttrc`:\n\n    set mailcap_path="${HOME}/.mutt/mailcap:/etc/mailcap"\n\nIn your mailcap, add entries for the appropriate MIME types:\n\n    text/calendar; viewical; copiousoutput\n    application/ics; viewical; copiousoutput\n\nIn your `.muttrc`, tell mutt to automatically display calendar data:\n\n    auto_view text/calendar\n    auto_view application/ics\n\nFinally, you need to add (or modify) the `alternative_order` setting in\nyour `.muttrc` to prefer iCalendar attachments over their HTML or text\nalternatives, for messages sent with such alternatives:\n\n    alternative_order text/calendar text/plain text/html\n\n### Output\n\nMost of the script\'s output should be self-explanatory.  Most fields are\noptional, so it\'ll only print information (from event end times to\nlocations to event descriptions) if they\'re present in the original data.\n\nOne thing to note is the encoding of attendees (or, in iCalendar\nterminology, "participants").  They\'re presented in a list with a checkbox\nof sorts next to them, something like this:\n\n    [ ] Barb Example <barb@example.com>\n\nPeople will get different boxes depending on the role defined for them in\nthe iCalendar data.  The boxes are as follows:\n\n* `{ }` - Event chairperson.\n* `[ ]` - Attendee, participation required.  (Most programs use this as\n          the default role.)\n* `< >` - Attendee, participation optional.\n* `( )` - Non-participant.  (The author of these scripts has never seen\n          this in actual use.)\n* `_ _` - No role defined in the data.\n* `? ?` - Unknown role.\n\nThe script places text in the box to indicate the status of the person.\nThe statuses are as follows:\n\n* blank - Unknown.  (Officially, this is "needs action", i.e. "waiting for\n          a response".)\n* `Y` - Attending.\n* `-` - Not attending.\n* `~` - Maybe attending.\n* `?` - Status not recognized by script.\n\n(In the event that the iCalendar data does not define a status, the box\nwill be empty, not just blank.  This is "status unknown to organizer":\n`[ ]`.  This is "status not present in data": `[]`.  That\'s not a huge\ndifference, but every file the script\'s author has observed has had some\nstatus defined for every person attached to an event.)\n\n#### Example\n\nHere\'s an event with a chairperson, two required attendees, and two\nnon-required attendees.  The chairperson and one required attendee have\nresponded that they will attend.  The other required attendee has not yet\nresponded.  One of the non-required attendees will not attend and the\nother is tentative.\n\n    Organizer: Admin Aid <admin@example.com>\n    Event:     Example Event\n    Date:      Thursday, August 4, 2016\n    Starts:    9:00 am\n    Ends:      10:00 am\n    Location:  Meeting Room 7\n    Attendees: {Y} Important Executive <exec@example.com>\n               [Y] Relevant Manager <mgr@example.com>\n               [ ] Relevant Subordinate <worker@example.com>\n               <-> Affiliated Manager <aff@example.com>\n               <~> Irrelevant Manager <irr@example.com>\n\n\nical-reply\n----------\n\n`ical-reply` is intended to facilitate responses to iCalendar emails.\nIt\'s not ready for use yet.\n\n\nRelease Process\n---------------\n\n * Update changelog\n * Update version number in `pyproject.toml`\n * Commit changes\n * Add release version tag\n * `poetry build`\n * `poetry publish`\n * Make a release on GitHub, attaching the wheel and tar files in `dist`\n',
    'author': 'Pip Gold',
    'author_email': 'pip@aperiodic.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/asciipip/mutt-ical',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
