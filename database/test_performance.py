import pymysql
from datetime import datetime
import json
import hashlib
import base64
import iota
import numpy as np

db = pymysql.connect(host='140.116.163.9',
                     port=10002,
                     user='dltlab',
                     password='dltlab@nckucs',
                     db='epslab_ems',
                     charset='utf8')

cursor = db.cursor(cursor=pymysql.cursors.DictCursor)

sql = 'SELECT * FROM bems_aggregator_dr_event'

cursor.execute(sql)

# data = cursor.fetchone()
# data = cursor.fetchall()
datas = cursor.fetchmany(size=25)

cursor.close()
db.close()

hash_data = []
base64_data = []

for data in datas:
    try:
        data['inserted_at'] = data['inserted_at'].strftime('%Y-%m-%dT%H:%M:%S')
        data['eventdate'] = data['eventdate'].strftime('%Y-%m-%d')
        data['start_at'] = data['start_at'].strftime('%Y-%m-%d %H:%M:%S')
        data['end_at'] = data['end_at'].strftime('%Y-%m-%d %H:%M:%S')
    except:
        # print("datetime error")
        pass
    json_data = json.dumps(data).encode('utf-8')
    hash_data.append(hashlib.sha256(json_data).hexdigest().encode())
    base64_data.append(base64.b64encode(hash_data[-1]))


base64_data_tests = []
base64_data_tests.append(base64_data[:5])
base64_data_tests.append(base64_data[:10])

for i in range(1, 6):
    base64_data_tests.append(base64_data*i)

# IOTA
MySeed = b"LUEMBUSKXRNZQO9ZFLHNVCRMJD9QISVRALLJZPMKXQCMJLSYTAGZR9ILUL9NODGKHLGWHZSKJQTMP9AOF"
# TargetAddresses = []
# TargetAddresses.append(
#     b"VOBLCCGXZOHUWUWTYJBZUFQBTDEOC9UZTUCORAKPAXPZLXRVWDZDKOIQHWIYXSCMKFMWYYCZBUHRWQSHX")
targetaddress = b"VOBLCCGXZOHUWUWTYJBZUFQBTDEOC9UZTUCORAKPAXPZLXRVWDZDKOIQHWIYXSCMKFMWYYCZBUHRWQSHX"

NowIs = datetime.now()  # get a actual date & time - just to have some meaningfull info

# preparing transactions
pt = []

apis = []
# apis.append('http://localhost:14267')
# apis.append('http://node10.puyuma.org:14265')
apis.append('https://nodes.thetangle.org:443')

apis_names = []
# apis_names.append('eb')
# apis_names.append('dlt')
apis_names.append('public')

cost_time_all = []

# for targetaddress in TargetAddresses:
for api_url, api_name in zip(apis, apis_names):
    for send_datas in base64_data_tests:
        cost_time = []
        i = 0
        for send_data in send_datas:
            i += 1
            print("%d/%d" % (i, len(send_datas)))
            starttime = datetime.now()
            print(starttime)
            pt.append(iota.ProposedTransaction(address=iota.Address(targetaddress),  # 81 trytes long address
                                               message=iota.TryteString.from_unicode(
                send_data.decode()),
                # Up to 27 trytes
                tag=iota.Tag(b'RBTC9D9DCDEAKDCDFD9DSC'),
                value=0))

            api = iota.Iota(api_url)

            # print("\nPreparing/Broadcasting... Wait please...")
            # the whole process initiated in a single call
            FinalBundle = api.send_transfer(depth=3,
                                            transfers=pt,
                                            min_weight_magnitude=14)['bundle']  # it returns a dictionary with a bundle object

            # bundle is broadcasted, let's print it
            print("\nGenerated bundle hash: %s" % (FinalBundle.hash))
            # print("\nTail Transaction in the Bundle is a transaction #%s." %
            #       (FinalBundle.tail_transaction.current_index))

            # print("\nList of all transactions in the bundle:\n")
            for txn in FinalBundle:
                print(vars(txn))
                print("")

            endtime = datetime.now()
            print("Cost time: %f s." %
                  ((endtime - starttime).seconds+(endtime - starttime).microseconds/10**6))
            cost_time.append((endtime - starttime).seconds +
                             (endtime - starttime).microseconds/10**6)
        cost_time_all.append(cost_time)
        print("%-10s\t%f\t%f\t%f\t%f" % ((api_name+'-'+str(len(send_datas))),
                                         np.max(cost_time), np.min(cost_time), np.mean(cost_time), np.std(cost_time, ddof=1)))

print("%-10s\tMax\tmin\tavg\tSD" % "Trial")

# for api_url, time_tests in zip(apis_names, cost_time_all):
api_show = apis_names[-1]
for cost_time in cost_time_all:
    print("%-10s\t%f\t%f\t%f\t%f" % ((api_show+'-'+str(len(cost_time))),
                                     np.max(cost_time), np.min(cost_time), np.mean(cost_time), np.std(cost_time, ddof=1)))
