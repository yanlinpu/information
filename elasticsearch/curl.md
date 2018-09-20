## CURL 用法

```
curl -X<VERB> '<PROTOCOL>://<HOST>:<PORT>/<PATH>?<QUERY_STRING>' -d '<BODY>'
# VERB          适当的 HTTP 方法 或 谓词 : GET`、 `POST`、 `PUT`、 `HEAD 或者 `DELETE`。
# PROTOCOL      http 或者 https`（如果你在 Elasticsearch 前面有一个 `https 代理）
# HOST          Elasticsearch 集群中任意节点的主机名，或者用 localhost 代表本地机器上的节点。
# PORT          运行 Elasticsearch HTTP 服务的端口号，默认是 9200 。
# PATH          API 的终端路径（例如 _count 将返回集群中文档数量）。Path 可能包含多个组件，例如：_cluster/stats 和 _nodes/stats/jvm 。
# QUERY_STRING  任意可选的查询字符串参数 (例如 ?pretty 将格式化地输出 JSON 返回值，使其更容易阅读)
# BODY          一个 JSON 格式的请求体 (如果请求需要的话)
```

## 计算集群中文档的数量
```
curl -XGET http://10.8.1.8:9200/_count?pretty \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
    "query": {
        "match_all": {}
    }
}
'
```



```
curl -XGET http://10.8.1.8:9200/_analyze?pretty \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
    "analyzer": "standard",
    "text": "Text to analyze test_abc(5) test2-abc2(6)"
}
'
```


bool must must_not should(score) filter(不评分、过滤模式)
