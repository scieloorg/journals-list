# coding: utf-8
import os
import csv
from articlemeta.client import ThriftClient


def journal_list(client, header, csv_utf_file, csv_iso_file, version):
    print('version =',version)
    with open(csv_utf_file, 'w') as csv_utf, open(csv_iso_file, 'w', encoding='iso-8859-1') as csv_iso:
        spamwriter_utf = csv.writer(csv_utf, delimiter='\t')
        spamwriter_iso = csv.writer(csv_iso, delimiter='\t')

        #Write the headers
        spamwriter_utf.writerow(header)
        spamwriter_iso.writerow(header)

        for journal in client.journals():
            collectiondata = client.collection(journal.collection_acronym)
            print(journal.collection_acronym+' '+journal.title)
            content=[
                #from version.1
                journal.collection_acronym or u'',
                journal.scielo_issn or u'',
                journal.print_issn or u'',
                journal.electronic_issn or u'',
                collectiondata.name or u'',
                journal.acronym or u'',
                journal.abbreviated_title or u'',
                journal.title or u'',
                journal.title_nlm or '',
                '; '.join(journal.publisher_name) or u'',
                journal.url() or u'',
                #from version.2
                journal.permissions['id'] if (journal.permissions is not None and version >= 2) else u'',
                #from version.3
                ', '.join([s for s in journal.editorial_standard]) if (journal.editorial_standard is not None and version >= 3) else u'',
                ', '.join([s for s in journal.languages]) if (journal.languages is not None and version >= 3) else u''
            ]
            #Writes the CSV files
            spamwriter_utf.writerow([l for l in content])
            spamwriter_iso.writerow([l.encode('iso-8859-1', 'replace').decode('iso-8859-1') for l in content])


def main():
    #Client Thriftpy
    client = ThriftClient()
    
    #Verify and create directorie if not exists
    dir_csv = 'csv'
    if os.path.exists(dir_csv):
        pass
    else:
        os.mkdir(dir_csv)


    # version.1
    version = 1
    header = ['Symbol','ISSN in use','Print ISSN','E-ISSN','Collection Name','Acronym','Short Title','Title','Short Title-NLM','Publisher','URL journal page']
    csv_utf_file = dir_csv + '/titles-tab-utf-8.csv'
    csv_iso_file = dir_csv + '/markup_journals.csv'
    journal_list(client, header, csv_utf_file, csv_iso_file, version)

    # version.2
    version = 2
    header = ['Symbol','ISSN in use','Print ISSN','E-ISSN','Collection Name','Acronym','Short Title','Title','Short Title-NLM','Publisher','URL journal page','License']
    csv_utf_file = dir_csv + '/titles-tab-v2-utf-8.csv'
    csv_iso_file = dir_csv + '/markup_journals_v2.csv'
    journal_list(client, header, csv_utf_file, csv_iso_file, version)

    # version.3
    version = 3
    header = ['Symbol','ISSN in use','Print ISSN','E-ISSN','Collection Name','Acronym','Short Title','Title','Short Title-NLM','Publisher','URL journal page','License','Editorial Standard','Languages']
    csv_utf_file = dir_csv + '/titles-tab-v3-utf-8.csv'
    csv_iso_file = dir_csv + '/markup_journals_v3.csv'
    journal_list(client, header, csv_utf_file, csv_iso_file, version)


if __name__ == "__main__":
    main()
    