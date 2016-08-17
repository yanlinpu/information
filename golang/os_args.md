```
package main

import (
  "fmt"
  "os"
  "strings"
)

func main() {
  // os.Args[0] 命令本身 
  // os.Args[1:] 命令参数
  fmt.Println(os.Args[0])
  var s, sep string
  for i := 1; i < len(os.Args); i++ {
    s += sep + os.Args[i]
    sep = " " 
  }
  for _, arg := range os.Args[1:] {                                                                                                                                                    
    s += sep + arg 
  }
  fmt.Println(s)
  // 如果不断链接的数据量很大，那么上面这种操作成本非常高，更简单有效的方法是strings Join函數
  fmt.Println(strings.Join(os.Args[1:], " "))
}

// => go run args.go  a b c   d
// => /tmp/go-build753550718/command-line-arguments/_obj/exe/args
// => a b c d a b c d
// => a b c d
```

