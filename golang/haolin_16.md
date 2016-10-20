## demo.1 天内开始时间的相关常量
```
const (
  MIN_START_TIME_OF_DAY     = time.Duration(0)
  MAX_START_TIME_OF_DAY     = time.Hour*23 + time.Minute*59 + time.Second*59
  DEFAULT_START_TIME_OF_DAY = time.Hour * 2 
  DAY                       = time.Hour * 24
)
```
## demo.2
```
var storagePool store.SPool

var rwmutex sync.RWMutex

var defaultServer string
var defaultPassword string
```
## demo.3 获取断续器的信号，信号来临之前该方法会阻塞
```
func (dTicker *DynamicTicker) Sign() {
  timeout := time.NewTimer(TIMEOUT_DURATION)
  for {
    ticker := dTicker.tickerValue.Load().(*time.Ticker)
    …  
  }
}
```
## demo.4 
```
…
var value interface{}
…
s, ok = value.(string)
i, ok = value.(int)
d, ok = value.(time.Duration)
b, ok = value.(bool)
…
```
## demo.5 根据值的实际类型写入临时缓存
```
…
v := factorMap[k]
switch i := v.(type) {
case int64:
  buffer.WriteString(strconv.FormatInt(i, 10))
case string:
  buffer.WriteString(i)
}
if i <= connectorCount {
  buffer.WriteRune('&')
}
…
```
## demo.6 
```
……
for field, _ := range fieldMap {
  originalUrl := GetServiceUrlWithDefault(field)
  if originalUrl == "" {
    t.Logf("The original url (%s) is empty.", field)
  } else {
    t.Logf("The original url (%s) is %s.", field, originalUrl)
  }
}
……

```
## demo.7 
```
func init() {
  const KEY_PREFIX = base.KEY_PREFIX_SENDING_RESULT
  // 当即执行一次旧记录清理任务
  removeOldRecord(KEY_PREFIX)
  // 计划实施下一次旧记录清理任务
  ……
}
```
## demo.8 存储器连接接口
```
type SConn interface {
  Name() string
  Close() error
  GetValueOfFieldInHash(hashKey SKey, field SField) (string, error)
  GetAllValuesInHash(hashKey SKey) (map[SField]string, error)
  ……
}
```
## demo.9 
```
……
  originalMap, err := redisConn.GetAllValuesInHash(testingKey)
  if err != nil {
    t.Fatalf("Can not get values from the redis: %s\n", err)
  }
……
```
## demo.10 
```
func AddRecords(newResults ...SendingResult) []error {
  if newResults == nil {
    return []error{errors.New("Invalid sending result slice!")}
  }
  if len(newResults) == 0 {
    log.DLogger().Warn("Empty sending result! Ignore the add operation!")
    return nil
  }
  ……
}
```
## demo.11 
```
……
newResults := make([]SendingResult, number)
……
errs := AddRecords(newResults...)
if errs != nil && len(errs) > 0 {
  t.Fatalf("Can not add records %#v (key: '%s'), errors: %#v\n",
    newResults, hashKey, errs)
}
……
```
## demo.12 
```
func AddRecord(newResult SendingResult) error {
  pool := base.GetStoragePool()
  conn := pool.Get()
  defer conn.Close()
  ……
}
```
## demo.13 
```
func (controller *AccessTokenController) Get() {
  defer func() {
    if p := recover(); p != nil {
      panicMsg := fmt.Sprintf("Fatal error: %s\n", p)
      beego.Critical(panicMsg)
      controller.Ctx.WriteString(generateRespForFatalError(panicMsg))
    }
  }()
  ……
  logger := log.Logger(log.GLOG)
}
```
## demo.14
```
// 发送结果的判小函数。
type LessFunc func(p1, p2 *SendingResult) bool

// 生成基于时间的判小函数。
func GenerateTimeBasedLessFunc(reverse bool) LessFunc {
  return func(p1, p2 *SendingResult) bool {
    if !reverse {
      return timeBasedLessFunc(p1, p2)
    } else {
      return timeBasedLessFunc(p2, p1)
    }
  }
}
```
## demo.15  
```
……
go func(phoneNumber string, retInfo SmsSendingRetInfo) {
  err = recordResult(phoneNumber, retInfo)
  if err != nil {
    errMsg :=
      fmt.Sprintf("Can not record the sending result"+
        " (phoneNumber: %s, ret: %d, msg: %s): %s \n",
        phoneNumber, retInfo.Ret, retInfo.Msg, err)
     log.DLogger().Errorln(errMsg)
  }
}(smsSendingInfo.PhoneNumber, *smsSendingRetInfo)
……
```
## demo.16 
```
……
sendingResults := make([]SendingResult, 0)
......
var wgForGetting sync.WaitGroup
wgForGetting.Add(len(keys))
resultCh := make(chan SendingResult, keysLen)
for _, key := range keys {
  go func(hashKey store.SKey) {
    defer wgForGetting.Done()
    ......
    for _, result := range currentResults {
      result.PhoneNumber = phoneNumber
      result.FormattedDate = formattedDate
      resultCh <- result
    }
  }(key)
}
wgForGetting.Wait()
close(resultCh)
……
```
