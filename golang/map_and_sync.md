## 读写锁实现了 安全的map
### http://www.cnblogs.com/ghj1976/archive/2013/04/27/3047528.html

```
package main

import (
  "fmt"
  "strconv"
  "sync"
)

type BeeMap struct {
  Lock *sync.RWMutex
  Bm   map[interface{}]interface{}
}

func NewBeeMap() *BeeMap {
  return &BeeMap{
    Lock: new(sync.RWMutex),
    Bm:   make(map[interface{}]interface{}),
  }
}

//Get from maps return the k's value
func (m *BeeMap) Get(k interface{}) interface{} {
  m.Lock.RLock()
  defer m.Lock.RUnlock()
  if val, ok := m.Bm[k]; ok {
    return val 
  }
  return nil 
}

// Maps the given key and value. Returns false
// if the key is already in the map and changes nothing.
func (m *BeeMap) Set(k interface{}, v interface{}) bool {
  m.Lock.Lock()
  defer m.Lock.Unlock()
  if val, ok := m.Bm[k]; !ok {
    m.Bm[k] = v 
  } else if val != v { 
    m.Bm[k] = v 
  } else {
    return false
  }
  return true
}
// Returns true if k is exist in the map.
func (m *BeeMap) Check(k interface{}) bool {
  m.Lock.RLock()
  defer m.Lock.RUnlock()
  if _, ok := m.Bm[k]; !ok {
    return false
  }
  return true
}

func (m *BeeMap) Delete(k interface{}) {
  m.Lock.Lock()
  defer m.Lock.Unlock()
  delete(m.Bm, k)
}

func main() {
  nbm := NewBeeMap()
  wg := sync.WaitGroup{}
  wg.Add(10)
  for i := 0; i < 10; i++ {
    go func(i int) {
      defer wg.Done()
      k := "Key" + strconv.Itoa(i)
      v := "Value" + strconv.Itoa(i)
      _ = nbm.Set(k, v)
    }(i)
  }
  wg.Wait()
  fmt.Println("Key1 set to Value1: ", nbm.Get("Key1"))
  _ = nbm.Set("Key1", 22)
  fmt.Println("update the value of Key1 from stirng into integer:", nbm.Get("Key1"))
  fmt.Println("not exist: ", nbm.Get("Key"))
  nbm.Delete("Key1")
  fmt.Println("Delete the key Key1: ", nbm.Get("Key1"))
}

/*
======================================================
Key1 set to Value1:  Value1
update the value of Key1 from stirng into integer: 22
not exist:  <nil>
Delete the key Key1:  <nil>
======================================================
*/
```
