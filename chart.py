import pygal
import datetime
import duolingo
import time
from datetime import datetime, timedelta

import os
duo_pass = os.environ['PASSWD']

lingo  = duolingo.Duolingo('tschuy', password=duo_pass)

user_info = lingo.get_user_info()
improvements = user_info['language_data']['de']['calendar']

imps = {}
for improvement in improvements:
    imp_date = datetime.fromtimestamp(
        int(improvement['datetime']/1000))
    day = imps.get(str(imp_date.date()), {})
    if not day:
        imps[str(imp_date.date())] = {}
    points_of_day = day.get('points', 0)
    points_of_day += int(improvement['improvement'])
    imps[str(imp_date.date())]['points'] = points_of_day
    imps[str(imp_date.date())]['date'] = imp_date.date()

datey = pygal.DateY(range=(0), x_label_rotation=20)

datey.add("Points", sorted([
    (imps[key]['date'], imps[key]['points']) for key in imps],
    key=lambda variable: variable[0]))

datey.render_to_file('duo.svg', include_x_axis=True)
