"""
Test program for pre-processing schedule

The entry 'date' and 'currentWeek' feilds has been added 
"""
import arrow

base = arrow.now()
today = arrow.now()


def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  
    """
    field = None
    entry = { }
    cooked = [ ] 
    for line in raw:
        line = line.rstrip()
        if len(line) == 0:
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
                base = arrow.get(content,'MM/DD/YYYY')   #Get the date tha American way
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = { }
            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = content
            entry['date'] = base.format('MM/DD/YYYY')   # format the date so it will be acceptable by json
            nextWeek = base.replace(weeks=+1)           # add a week to the base date
            entry['currentWeek'] = today >= base and today < nextWeek   # if current week true else false
            base = nextWeek                             # Reset the base date to be next week's date

            

        elif field == 'topic' or field == 'project':
            entry[field] = content
            
        else:
            raise ValueError("Syntax error in line: {}".format(line))

    if entry:
        cooked.append(entry)

    return cooked


def main():
    f = open("static/schedule.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()

    
    
            
    
