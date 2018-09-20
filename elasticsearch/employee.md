# CONTENT

创建一个雇员目录

我们受雇于 Megacorp 公司，作为 HR 部门新的 “热爱无人机” （_"We love our drones!"_）激励项目的一部分，我们的任务是为此创建一个雇员目录。该目录应当能培养雇员认同感及支持实时、高效、动态协作，因此有一些业务需求：

- 支持包含多值标签、数值、以及全文本的数据
- 检索任一雇员的完整信息
- 允许结构化搜索，比如查询 30 岁以上的员工
- 允许简单的全文搜索以及较复杂的短语搜索
- 支持在匹配文档内容中高亮显示搜索片段
- 支持基于数据创建和管理分析仪表盘


## STEP1. 索引雇员文档 增改

- 每个雇员索引(megacorp)(database)一个文档(employee)，包含该雇员的所有信息。
- 每个文档都将是 employee 类型(table) 。
- 该类型位于 索引 megacorp 内。
- 该索引保存在我们的 Elasticsearch 集群中。

```
curl -XPUT http://10.8.1.8:9200/megacorp/employee/1 \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
    "first_name" : "John",
    "last_name" :  "Smith",
    "age" :        25,
    "about" :      "I love to go rock climbing",
    "interests": [ "sports", "music" ]
}
'
# {"_index":"megacorp","_type":"employee","_id":"1","_version":1,"result":"created","_shards":{"total":2,"successful":1,"failed":0},"_seq_no":0,"_primary_term":1}
```

```
curl -XPUT http://10.8.1.8:9200/megacorp/employee/2 \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
    "first_name" :  "Jane",
    "last_name" :   "Smith",
    "age" :         32,
    "about" :       "I like to collect rock albums",
    "interests":  [ "music" ]
}
'
```
```
curl -XPUT http://10.8.1.8:9200/megacorp/employee/3 \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
    "first_name" :  "Douglas",
    "last_name" :   "Fir",
    "age" :         35,
    "about":        "I like to build cabinets",
    "interests":  [ "forestry" ]
}
'
```

## STEP2. 索引雇员文档 删查（GET DELETE）

```
curl -XGET http://10.8.1.8:9200/megacorp/employee/1?pretty
```

get result
```
{
  "_index" : "megacorp",
  "_type" : "employee",
  "_id" : "1",
  "_version" : 1,
  "found" : true,
  "_source" : {
    "first_name" : "John",
    "last_name" : "Smith",
    "age" : 25,
    "about" : "I love to go rock climbing",
    "interests" : [
      "sports",
      "music"
    ]
  }
}
```
## STEP3. 轻量索引 _search 一个搜索默认返回十条结果
```
curl -XGET http://10.8.1.8:9200/megacorp/employee/_search?pretty
curl -XGET http://10.8.1.8:9200/megacorp/employee/_search?q=last_name:Smith&pretty
curl -XGET http://10.8.1.8:9200/megacorp/employee/_search?q={last_name:Smith}&pretty
curl -XGET http://10.8.1.8:9200/megacorp/employee/_search?q={last_name:Smith,first_name:Jane}&pretty
```

result
```
{
  "took" : 0,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : 3,
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "megacorp",
        "_type" : "employee",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "first_name" : "Jane",
          "last_name" : "Smith",
          "age" : 32,
          "about" : "I like to collect rock albums",
          "interests" : [
            "music"
          ]
        }
      },
      ...
    ]
  }
}
```
## STEP4. 使用查询表达式搜索(DSL语句查询)

- match             全文搜索    在全文属性上搜索并返回相关性最强的结果。_score排序
- match_phrase      短语搜索    仅匹配同时包含 “rock” 和 “climbing” ，并且 二者以短语 “rock climbing” 的形式紧挨着
- filter            用于执行区间搜索
- highlight         高亮搜索    这个部分包含了 about 属性匹配的文本片段，并以 HTML 标签 <em></em> 封装
- aggregation       分析（聚合） 聚合与 SQL 中的 GROUP BY 类似但更强大。

```
curl -XGET http://10.8.1.8:9200/megacorp/employee/_search?pretty \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
    "query" : {
        "bool": {
            "must": {
                "match":{
                    "last_name": "Smith"
                }
            },
            "filter": {
                "range": {
                    "age": {"gt": 30}
                }
            }
        }
    }
}'

curl -XGET http://10.8.1.8:9200/megacorp/employee/_search?pretty \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
    "query" : {
        "match_phrase":{
            "about": "rock climbing"
        }
    },
    "highlight": {
        "fields" : {
            "about" : {}
        }
    }
}
'


curl -XGET http://10.8.1.8:9200/megacorp/employee/_search?pretty \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
    "aggs": {
        "all_interests": {
            "terms": { "field": "interests" }
        }
    }
}
'
```

## STEP5. 索引雇员文档
## STEP2. 索引雇员文档
## STEP2. 索引雇员文档
## STEP2. 索引雇员文档