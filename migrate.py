import sqlite3

con1 = sqlite3.connect('db_copy.sqlite3')
con2 = sqlite3.connect('db.sqlite3')

cur1 = con1.cursor()
cur2 = con2.cursor()

tables = [
    'mysite_user_groups',
    'mysite_user_user_permissions',
    'mysite_gestiondoc',
    'mysite_contact',
    'mysite_entreprise',
    'mysite_message',
    'mysite_ticket',
    'mysite_contrat',
    'mysite_autredoc',
    'mysite_connexion',
    'mysite_facture',
    'mysite_demande',
    'mysite_user'
]

for table in tables:
    i = 5
    for row1 in cur1.execute(f'SELECT * FROM {table}'):
        test = True
        for row2 in cur2.execute(f'SELECT * FROM {table}'):
            if row2 == row1:
                test = False

        # if table == 'mysite_user':
        #     row = list(row)
        #     row.append(None)
        #     print(row)
        #     row[-4], row[-3], row[-2], row[-1] = row[-1], row[-4], row[-3], row[-2]
        #     row = tuple(row)
        if test:
            row1 = list(row1)
            row1[0] = i
            row1 = tuple(row1)
            cur2.execute(f'INSERT INTO {table} VALUES {row1}'.replace('None', 'NULL'))
            i += 1

con2.commit()

con1.close()
con2.close()