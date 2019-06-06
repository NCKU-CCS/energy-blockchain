import pymysql
from datetime import datetime
import json
import hashlib
import base64
import iota

db = pymysql.connect(host='140.116.163.9',
                     port=10002,
                     user='dltlab',
                     password='dltlab@nckucs',
                     db='epslab_ems',
                     charset='utf8')

cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

sql = 'SELECT * FROM bems_aggregator_distribution'

cursor.execute(sql)

data = cursor.fetchone()
# data = cursor.fetchall()

cursor.close()
db.close()

try:
    data['updated_at'] = data['updated_at'].strftime('%Y-%m-%dT%H:%M:%S')
except:
    print("No DateTime!")
json_data = json.dumps(data).encode('utf-8')
hash_data = hashlib.sha256(json_data).hexdigest().encode()
print(hash_data)
base64_data = base64.b64encode(hash_data)
print(base64_data)

# IOTA

MySeed = b"LUEMBUSKXRNZQO9ZFLHNVCRMJD9QISVRALLJZPMKXQCMJLSYTAGZR9ILUL9NODGKHLGWHZSKJQTMP9AOF"
TargetAddresses = []
TargetAddresses.append(
    b"VOBLCCGXZOHUWUWTYJBZUFQBTDEOC9UZTUCORAKPAXPZLXRVWDZDKOIQHWIYXSCMKFMWYYCZBUHRWQSHX")

NowIs = datetime.now()  # get a actual date & time - just to have some meaningfull info

# preparing transactions
pt = []
for targetaddress in TargetAddresses:
    pt.append(iota.ProposedTransaction(address=iota.Address(targetaddress),  # 81 trytes long address
                                       message=iota.TryteString.from_unicode(
                                           base64_data.decode()),
                                       # Up to 27 trytes
                                       tag=iota.Tag(b'RBTC9D9DCDEAKDCDFD9DSC'),
                                       value=0))

api = iota.Iota("https://nodes.thetangle.org:443")
# api = iota.Iota("http://140.116.247.123:14267")

print("\nPreparing/Broadcasting... Wait please...")
# the whole process initiated in a single call
FinalBundle = api.send_transfer(depth=3,
                                transfers=pt,
                                min_weight_magnitude=14)['bundle']  # it returns a dictionary with a bundle object

# bundle is broadcasted, let's print it
print("\nGenerated bundle hash: %s" % (FinalBundle.hash))
print("\nTail Transaction in the Bundle is a transaction #%s." %
      (FinalBundle.tail_transaction.current_index))

print("\nList of all transactions in the bundle:\n")
for txn in FinalBundle:
    print(vars(txn))
    print("")

endtime = datetime.now()
print("Cost time: %d s." % (endtime - NowIs).seconds)
