from datetime import datetime, timedelta
import os
import time

import pygal
import duolingo


duo_pass = os.environ['PASSWD']
duo_username = os.environ.get('USERNAME', 'tschuy')


def generate_chart(calendar, filename):
    imps = {}
    for improvement in calendar:
        imp_date = datetime.fromtimestamp(
            int(improvement['datetime']/1000))
        print imp_date
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

    datey.render_to_file(filename, include_x_axis=True)


def update_charts():
    lingo  = duolingo.Duolingo(duo_username, password=duo_pass)
    user_info = lingo.get_user_info()
    generate_chart(lingo.get_calendar(), '{}-overall.svg'.format(duo_username))
    for language in lingo.get_languages(abbreviations=True):
        print language
        filename = '{}-{}.svg'.format(duo_username, language)
        generate_chart(lingo.get_calendar(language), filename)



if __name__ == '__main__':
    update_charts()
