curl -XPUT http://10.8.1.8:9200/twitter \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
  "mappings": {
    "user": {
      "properties": {
        "name": { "type": "text" },
        "user_name": { "type": "keyword" },
        "email": { "type": "keyword" }
      }
    },
    "tweet": {
      "properties": {
        "content": { "type": "text" },
        "user_name": { "type": "keyword" },
        "tweeted_at": { "type": "date" }
      }
    }
  }
}
'





curl -XGET http://10.8.1.8:9200/twitter/user,tweet/_search?pretty \
--header "Content-Type:application/json" \
-H "session_id:123456789xxx" \
-d '
{
    "query": {
        "match": {
            "user_name": "kimchy"
        }
    }
}'



（包、、导游、），失败时返回失败原因（如1、查无此证；2、未打开全国导游之家APP，无法确定导游真伪，请导游打开全国导游之家APP；3、未能获得该导游的位置信息，无法确定导游真伪，请导游打开APP的位置上传功能；4、未能获得扫描终端的位置信息，请工作人员打开扫码APP的位置上传功能；5、全国导游之家APP当前距离景区较远，无法确定导游真伪等。）


导游二维码信息，终端类型（窗口或移动端），终端位置（换票窗口信息／移动端位置信息）,时间戳 
{
    qr_str: '',
    ter_type: 0, //0窗口 1移动端
    ter_position: {
        longitude: ''
        latitude: ''
    },
    timestamp: 1526971081845 //时间戳
}


{
    error_code: 0,
    result:{
        pic_avatar: '导游照片',
        user_name: '导游姓名',
        guide_card: '导游证号',
        star_level: '导游星级',
        level: '导游级别',
        lang_level_list: [{"languages":"普通话","level":"初级"}], //'语种及级别',
        cert_issued_at: '导游证签发日期',
        cert_expired_at: '导游证过期时间'
    }
}

{
    error_code: 12301001,
    error_msg: '查无此证'
}

{
    error_code: 12301002,
    error_msg: '未打开全国导游之家APP，无法确定导游真伪，请导游打开全国导游之家APP'
}

{
    error_code: 12301003,
    error_msg: '未能获得该导游的位置信息，无法确定导游真伪，请导游打开APP的位置上传功能'
}

{
    error_code: 12301004,
    error_msg: '未能获得扫描终端的位置信息，请工作人员打开扫码APP的位置上传功能'
}

{
    error_code: 12301005,
    error_msg: '全国导游之家APP当前距离景区较远，无法确定导游真伪'
}