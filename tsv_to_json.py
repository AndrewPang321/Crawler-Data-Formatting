import csv
import datetime

# save the json output
jsfile = open('imdb_data'+ str(datetime.datetime.now()).replace(' ', '_') + '.json', 'w')
jsfile.write('[\r\n')

print('opening file...')

with open('title.basics.tsv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')

    # get the total number of rows excluded the heading
    # row_count = len(list(reader))
    row_count = sum(1 for row in reader)
    idx = 0

    # back to first position
    f.seek(0)

    for row in reader:
        print('Running idx ', idx, ' out of ', row_count)

        # Skip the header line
        if idx == 0:
            idx += 1
            print('Skip header line...')
            continue

        idx += 1

        jsfile.write('\t{\r\n')

        tconst = '\t\t\"tconst\": \"' + row[0] + '\",\r\n'
        # averageRating = '\t\t\"averageRating\": \"' + averageRating + '\",\r\n'
        # numVotes = '\t\t\"numVotes\": \"' + numVotes + '\"\r\n'
        titleType = '\t\t\"titleType\": \"' + row[1] + '\",\r\n'
        primaryTitle = '\t\t\"primaryTitle\": \"' + row[2] + '\",\r\n'
        originalTitle = '\t\t\"originalTitle\": \"' + row[3] + '\",\r\n'
        isAdult = '\t\t\"isAdult\": \"' + row[4] + '\",\r\n'
        startYear = '\t\t\"startYear\": \"' + row[5] + '\",\r\n'
        endYear = '\t\t\"endYear\": \"' + row[6] + '\",\r\n'
        runtimeMinutes = '\t\t\"runtimeMinutes\": \"' + row[7] + '\",\r\n'
        genres = '\t\t\"genres\": \"' + row[8] + '\"\r\n'

        jsfile.write(tconst)
        # jsfile.write(averageRating)
        # jsfile.write(numVotes)
        jsfile.write(titleType)
        jsfile.write(primaryTitle)
        jsfile.write(originalTitle)
        jsfile.write(isAdult)
        jsfile.write(startYear)
        jsfile.write(endYear)
        jsfile.write(runtimeMinutes)
        jsfile.write(genres)

        jsfile.write('\t}')

        # omit comma for last row item
        if idx < row_count:
            jsfile.write(',\r\n')

        jsfile.write('\r\n')

jsfile.write(']')
jsfile.close()

