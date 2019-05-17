"""
Pre-process a syllabus (class schedule) file. 

"""
import arrow   # Dates and times refernece: https://arrow.readthedocs.io/en/latest/#replace-shift
import logging
from datetime import timedelta # represents a duration, the difference between two dates or times.
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

base = arrow.now()   # Default, replaced if file has 'begin: ...'
listed_week = arrow.now() # Default, replaced if file has 'begin: ...' and continues to increase as we read more of the schedule.txt file

def is_this_week(date1, date2):

    #Soruce: https://stackoverflow.com/a/14191915/4967874
    monday1 = (date1 - timedelta(days=date1.weekday()))
    monday2 = (date2 - timedelta(days=date2.weekday()))
    return ((monday2-monday1).days / 7) == 0

def get_listed_week(base,content):
    #param: base -> arrow object of base date (when course started)
    #content: int 1-10 representing the most previous week # read by proccess(raw)
    listed_week = base.shift(weeks=+(int(content) - 1))  # subtract one from content because week 1 is the same date as our 'base' variable and does not need to be shifted
    temp = listed_week.date()
    list_month = temp.month
    list_day = temp.day
    return "{}/{}".format(list_month,list_day)



def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment ad skipped. 
    """
    field = None
    entry = {}
    cooked = []
    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            log.debug("Skipping")
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line + " "
            continue
        if len(parts) == 2:
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) +
                             "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:
                base = arrow.get(content, "MM/DD/YYYY")
                # print("Base date {}".format(base.isoformat()))
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = {}
            entry['topic'] = ""
            entry['project'] = ""

            listed_date = base.shift(weeks=+(int(content) - 1))  # subtract one from content because week 1 is the same date as our 'base' variable and does not need to be shifted
            list_month = listed_date.month
            list_day = listed_date.day
            entry['week'] = "{}/{}".format(list_month,list_day)
            entry['highlighted'] = is_this_week(arrow.now().date(),listed_date.date())


        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    if entry:
        cooked.append(entry)

    return cooked


def main():
    f = open("data/schedule.txt")
    parsed = process(f)
    print(parsed)


if __name__ == "__main__":
    main()
