import common
from dateutil import parser


records = [('2019-04-15 02:16:00', 'INFO'), ('2019-04-15 01:01:15', 'ERROR'),
    ('2019-04-15 01:23:33', 'ERROR'), ('2019-04-15 01:12:00', 'ERROR'),
    ('2019-04-15 01:45:44', 'ERROR'), ('2019-04-15 01:13:00', 'ERROR'),
    ('2019-04-15 01:14:00', 'ERROR'), ('2019-04-15 01:14:00', 'ERROR'),
    ('2019-04-15 02:15:00', 'ERROR'), ('2019-04-15 02:16:00', 'WARN'),
    ('2019-04-15 02:16:00', 'INFO'), ('2019-04-15 02:16:00', 'WARN'),
    ('2019-04-15 02:16:00', 'WARN'), ('2019-04-15 02:17:00', 'DEBUG')]

for ts, l in records:
    common.insert_log(parser.parse(ts), l, "some_text")