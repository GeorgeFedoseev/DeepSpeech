# =* coding: utf-8 *=
import os
import sys
reload(sys)

sys.setdefaultencoding("utf-8")

current_dir_path = os.path.dirname(os.path.realpath(__file__))
project_root_path = os.path.join(current_dir_path, os.pardir, os.pardir)
sys.path.insert(0, project_root_path)


import indexer
from utils import db_util

from pprint import pprint

import time

def search(q):
    db_util.init_db()

    results_all = []

    indexer_results = indexer.full_text_search(q)

    for r in indexer_results:
        db_item = db_util.get_item_by_id(r[0])

        results_all.append({
            "media_id": db_item.media_id,
            "time_start": db_item.time_start,
            "time_end": db_item.time_end,
            "highlight": r[1]
            })

        #print db_item.media_id

    media_ids = set(map(lambda x:x["media_id"], results_all))

    results_grouped_by_media = []

    for mid in media_ids:
        results_grouped_by_media.append({
            "media_id": mid,
            "results": [r for r in results_all if r["media_id"] == mid]
            })

    return results_grouped_by_media



if __name__ == "__main__":
    results = search("депозитов")
    #pprint(results)

    #print results[0]["results"][0]["highlight"]

    if len(results) > 0:
        res = results[0]["results"][0]
        print res["highlight"]

        print res["time_start"]

        formatted_timestart = time.strftime('%Mm%Ss', time.gmtime(res["time_start"]))
        print "https://youtu.be/%s?t=%s" % (res["media_id"],  formatted_timestart)
    else:
        print("no results")

    





