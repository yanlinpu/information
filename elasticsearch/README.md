

# 概念
## 和传统关系型数据库对比

|       |       |       |       |       |
|:-----:|:-----:|:-----:|:-----:|:-----:|
|Relational DB|Databases|Tables|Rows|Columns|
|Elasticsearch|Indices|Types|Documents|Fields|

Elasticsearch集群可以包含多个索引(indices)（数据库），每一个索引可以包含多个类型(types)（表），每一个类型包含多个文档(documents)（行），然后每个文档包含多个字段(Fields)（列）。

## 索引（index）
在Elasticsearch中存储数据的行为就叫做索引(indexing)         
- 索引（名词） 一个索引(index)就像是传统关系数据库中的数据库，它是相关文档存储的地方，index的复数是indices 或indexes。
- 索引（动词） 「索引一个文档」表示把一个文档存储到索引（名词）里，以便它可以被检索或者查询。这很像SQL中的INSERT关键字，差别是，如果文档已经存在，新的文档将覆盖旧的文档。
- 倒排索引 传统数据库为特定列增加一个索引，例如B-Tree索引来加速检索。Elasticsearch和Lucene使用一种叫做倒排索引(inverted index)的数据结构来达到相同目的。

## 索引词（term）
## 文本（text）
## 分析（analysis） 将文本转换为索引词的过程，分析的结果依赖分词器
## 集群（cluster）
## 节点（node）
## 路由（routing）
## 分片（shard） 分片是单个lucene实例   索引是指向主分片和副本分片的逻辑空间。
## 主分片（primary shard）
## 副本分片（replica shard）
## 复制（replica）
## 类型（type）
## 文档（document）
## 映射（mapping）