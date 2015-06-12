import bayeslite
import bayeslite.bql as bql
import bayeslite.core as core
import bayeslite.crosscat
import bayeslite.parse as parse
import crosscat.LocalEngine as localengine
from prettytable import PrettyTable
import getopt
import sys


def bql_exec(bdb, string):
    import sys
    print >>sys.stderr, '--> %s' % (string.strip(),)
    phrases = parse.parse_bql_string(string)
    phrase = phrases.next()
    done = None
    try:
        phrases.next()
        done = False
    except StopIteration:
        done = True
    if done is not True:
        raise ValueError('>1 phrase: %s' % (string,))
    return bql.execute_phrase(bdb, phrase)

def try_query(query):
    c =  bdb.execute(query)
    print_cursors(c)
        
def print_cursors(curs):
    col_names = [cn[0] for cn in curs.description]
    rows = curs.fetchall()
    pt = PrettyTable()
    for col_num, col_name in enumerate(col_names):
        pt.add_column(col_name, [row[col_num] for row in rows])
    print(pt)

model_file = 'dha_models.pkl.gz'
table_name = 'dh_test'
generator_name = 'dh_test_cc'


# bayeslite
bdb = bayeslite.bayesdb_open()
bayeslite.bayesdb_register_metamodel(bdb, bayeslite.crosscat.CrosscatMetamodel(localengine.LocalEngine(seed=0)))
bayeslite.bayesdb_read_csv_file(bdb, table_name, 'dha.csv', header=True, create=True)
bayeslite.bayesdb_load_legacy_models(bdb, generator_name, table_name, 'crosscat', model_file, create=True)

try_query('estimate columns from {} order by dependence probability with MDCR_SPND_AMBLNC DESC limit 10'.format(generator_name))
try_query('estimate columns from {} order by dependence probability with QUAL_SCORE limit 10'.format(generator_name))
