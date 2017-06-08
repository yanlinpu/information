https://github.com/functionscope/Node-Excel-Export

```
'use strict';

var async = require("async");
var _ = require("lodash");
var moment = require("moment");
var nodeExcel = require('excel-export');
var that = {};

function getExcel(data, callback) {
    var conf ={};
    conf.cols = [
        {caption:'string', type:'string'},
        {caption:'date', type:'date'},
        {caption:'bool', type:'bool'},
        {
            caption:'number',
            //width: 30,
            type:'number'
        }               
    ];  
    conf.rows = data;
    var result = nodeExcel.execute(conf);
    callback(null, result);
}

//格式化数据
function formatListForExport(list) {
    return _.map(list, function (item) {
        var result = [
            item.attr1,
            item.attr2,
            item.attr3,
            item.attr4
        ];
        return result;
    });
};

function genExecl(list, callback) {
    list = formatListForExport(list);
    getExcel(list, function (err, buffer) {
        callback(err, buffer);
    });
};

that.exportRegisterguide = function(req, res, next){
    //获取对象数组
    var list = [
        {attr1: 'pi', attr2: (new Date(2013, 4, 1)).getJulian(), attr3: true, attr4: 3.14},
        {attr1: "e", attr2: (new Date(2012, 4, 1)).getJulian(), attr3: false, attr4: 2.7182}
    ];
    genExecl(list, function (err, buffer) {
        var fileName = "attachment; filename=export_" + moment().format("YYYYMMDDHHMM") + ".xlsx";
        res.setHeader('Content-Type', 'application/vnd.openxmlformats');
        res.setHeader("Content-Disposition", fileName);
        res.end(buffer, 'binary');
    })
}

module.exports = that;
```
