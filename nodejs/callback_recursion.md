## callback递归（tree 从低级到高级）

```
that.getGovPermissionByGovType = function (gov_type, callback) {
    let client = db_manager.getClient();
    async.waterfall(
        [
            function (cb) {
                db.getGovPermissionByGovType(client, gov_type, cb);
            },
            function (list, cb) {
                getParentGovPermission(client, list, cb);
            }
        ], function (err, result) {
            callback(err, result);
        }
    );
};

function getParentGovPermission(client, list, callback) {
    async.mapSeries(list, function (item, cb) {
        if(!item.parent_id){
            cb(null, item);
            return;
        }
        db.getParentGovPermission(client, item.parent_id, function (err, parentItem){
            if(err){
                cb(err);
                return;
            }
            if(!parentItem){
                cb('查找根节点失败');
                return
            }
            delete item.pid;
            delete item.parent_id;
            parentItem.sub = [];
            parentItem.sub.push(item);
            cb(err, parentItem);
        })
    }, function (err, results) {
        if(err){
            callback(err);
            return;
        }
        var newList = [], rootFlag = true;
        _.each(results, function (item) {
            if(rootFlag && item.parent_id){
                rootFlag = false;
            }
            var parent = _.find(newList, {pid: item.pid});
            if(parent){
                parent.sub.push(item.sub);
            }else{
                newList.push(item);
            }
        });
        if(rootFlag){
            _.each(newList, function (item) {
                delete item.pid;
                delete item.parent_id;
            })
            callback(null, newList);
        }else{
            getParentGovPermission(client, newList, callback);
        }
    })
}
```