from ftplib import FTP

SERVER = 'ftp.ncbi.nlm.nih.gov'
DIR = 'pub/pmc/oa_bulk/'
FILENAMES = ['comm_use.0-9A-B.txt.tar.gz',
             'comm_use.A-B.xml.tar.gz',
             'comm_use.C-H.txt.tar.gz',
             'comm_use.C-H.xml.tar.gz',
             'comm_use.I-N.txt.tar.gz',
             'comm_use.I-N.xml.tar.gz',
             'comm_use.O-Z.txt.tar.gz',
             'comm_use.O-Z.xml.tar.gz',
             'non_comm_use.0-9A-B.txt.tar.gz',
             'non_comm_use.A-B.xml.tar.gz',
             'non_comm_use.C-H.txt.tar.gz',
             'non_comm_use.C-H.xml.tar.gz',
             'non_comm_use.I-N.txt.tar.gz',
             'non_comm_use.I-N.xml.tar.gz',
             'non_comm_use.O-Z.txt.tar.gz',
             'non_comm_use.O-Z.xml.tar.gz']

ftp = FTP(SERVER)     # connect to host, default port
ftp.login()           # user anonymous, passwd anonymous@
ftp.cwd(DIR)
print(ftp.retrlines('LIST'))
for filename in FILENAMES[1:]:
    print(filename)
    ftp.retrbinary('RETR ' + filename, open(filename, 'wb').write)
    # error_perm: 550 'comm_use.A-B.xml.tar.gz': No such file or directory
ftp.quit()
