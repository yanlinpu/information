# 出自ruby元编程附录C法术手册

## No.1 环绕别名
> 从一个重新定义的方法中调用原始的、被重名的版本

```
class String
  alias_method :old_reverse, :reverse
  def reverse
    "x#{old_reverse}x"
  end
end
```
## No.2 白板类
> 移除一个对象中所有方法，以便把它们转换成幽灵方法

```
class D < BasicObject
  def method_missing(name, *args, &block)
    "a ghost method."
  end
end
D.new.to_s            # => 'a ghost method.'
```
## No.3 类扩展
> 通过向类的单件类中加入模块类定义类方法

```
class C; end
module M 
  def my_method
    'a class method'
  end
end
class <<　C
  include M
end
C.my_method
```
## No.4 类实例变量
> 在一个class对象的实例变量中存储类级别的状态

```
class C
  @my_class_instance_variable = 'abc'
  class << C
    def abc
      @my_class_instance_variable
    end
  end
end
C.abc         # => 'abc'
```
## No.5 类宏
> 在类定义中使用类方法（class << MyClass）

## No.6 洁净室
> 使用一个对象作为执行一个代码块的环境

```
class CleanRoom
  def a_useful_method(x); x * 2; end
end
CleanRoom.new.instance_eval{ a_useful_method(4) }
```
## No.7 代码处理器
> 处理从外部获得的代码字符串（eval）

## No.8 上下文探针
> 执行一个代码块来获取一个对象上下文中的信息（instance_eval）

## No.9 延迟执行
> 在proc或lambda中存储一段代码及上下文，用于以后执行

> - return: proc 从定义Proc作用域返回；lambda仅从这个lambda返回
> - 参数检验：lambda比Proc更严格，适应能力更强
> - lambda 更像方法，对参数数量比较严格，而且在调用return时，只从代码中返回，所以lambda为第一选择

## No.10 动态派发
> 在运行时决定用哪个方法（send）

## No.11 动态方法
> 在运行时决定怎样定义一个方法（define_method :my_method do ...）

## No.12 动态代理
> 把不能对应某个方法名的消息转发给另外一个对象（send）

## No.13 扁平化作用域
> 使用闭包在两个作用域之间的变量共享

## No.14 幽灵方法
> 响应一个没有关联方法的消息 method_missing(name, *args, &block)

## No.15 钩子方法
> 复写一个方法来截获对象模型事件（像钩子一样，钩住一个特定事件）

> - Class#inherited
> - Module#included
> - Module#prepended
> - ...

## No.16 内核方法
> Kernel模块中定义的方法，所有对象都可使用

```
module Kernel
  def a_method
    'abc'
  end
end
a_method          #＝> 'abc'
```
## No.17 惰性实例变量
> 等第一次访问一个实例变量时，才对他进行初始化

## No.18 拟态方法
> 把一个方法伪装成另外一种语言构建

```
def BaseClass(name)
  name == "string" ? String : Object
end

class C < BaseClass "string"            # => 一个看起来像类的方法
  attr_accessor :an_attribute           # => 一个看起来像关键字的方法（类宏）
end
obj = C.new
obj.an_attribute = 1                    # => 一个看起来像属性的方法
```
## No.19 猴子补丁
> 修改已有类的特性

## No.20 命名空间
> 在一个模块中定义常量，以防止命名冲突

```
module MyNamespace
  class Array
    def to_s
      'my class'
    end
  end
end
```
## No.21 空指针保护
> 用“或”操作符复写一个空引用（不能区分false和nil，不能在变量值可能为false时使用空指针保护）

```
x ||= 'not a nil value'
```
## No.22 对象扩展
> 通过给一个对象的单件类混入模块来定义单件方法

```
obj = Object.new
module M
  def my_method
    'a singleton method'
  end
end
class << obj
  include M
end
obj.my_method       # => "a singleton method"
```
## No.23 打开类
> 修改已有的类

```
class String
  def my_string_method
    'myslef method'
  end
end
```
## No.24 下包含包装器
> 调用一个prepend方式复写的方法

```
module M
  def reverse
    "x#{super}x"
  end
end
String.class_eval do
  prepend M
end
String.ancestors        # => [M, String, Comparable, Object, Kernel, BasicObject]
'abc'.reverse           # => "xcbax" 
```
## No.25 细化
> 为类打补丁，作用范围仅到文件结束，或仅限于包含模块的作用域中

```
# a.rb
module MyRefinement
  refine String do
    def reverse
      'my reverse'
    end
  end
end
puts 'abc'.reverse      # => 'cba'
using MyRefinement
puts 'abc'.reverse      # => 'my reverse'
```
## No.26 细化封装器
> 再细化中调用非细化的方法

```
# a.rb
module StringRefinement
  refine String do
    def reverse
      "x#{super}x"
    end
  end
end
using StringRefinement
puts "abc".reverse      # => 'xcbax'
```
## No.27 沙盒
> 在一个安全的环境中执行未授信的代码

```
def sandbox(&code)
  proc {
    $SAFE = 2
    yield
  }.call
end
begin
  sandbox { File.delete 'a.file' }
rescue Exception => ex
  ex
end
# => #<SecurityError: Insecure operation `delete' at level 2>
```
## No.28 作用域门
> 用class、module或def关键字来隔离作用域

```
a = 1
defined? a        # => "local-variable"
module MyModule
  b = 1
  defined? a      # => nil
  defined? b      # => "local-variable"
end
defined? a        # => "local-variable"
defined? b        # => nil
```
## No.29 self yield
> 把self传给当前代码块

```
class Person
  attr_accessor :name, :surname
  def initialize
    yield self
  end
end
joe = Person.new do |p|
  p.name = "Joe"
  p.surname = "Smith"
end
# => #<Person:0x00000001f32e00 @name="Joe", @surname="Smith">
```
## No.30 共享作用域
> 在同一个扁平作用域的多个上下文中共享变量

```
lambda {
  shared = 10
  puts self
  self.class.class_eval do
    define_method :counter do
      shared
    end
    define_method :down do
      shared -= 1
    end
  end
}.call
counter         # => 10
3.times { down }
counter         # => 7
```
## No.31 单件方法
> 在一个对象上定义一个方法

```
obj = "abc"
class << obj
  def my_singleton_method
    "xxxx"
  end
end
obj.my_singleton_method       # => 'xxxx'
```
## No.32 代码字符串
> 执行一段表示Ruby代码的字符串 eval

```
eval("1 + 1")
```
## No.33 符号到Proc（Symbol#to_proc）
> 把一个调用单个方法的块转换为一个符号

```
[1,2,3,4].map(&:even?)                          # => [false, true, false, true]
names = ['bob','bill']
names.map(&:capitalize.to_proc)
names.map(&:capitalize)                         # & 将对象转换为Proc
```

## No.33 binding

```
def get_binding                                                                                                                                                                        
  a = 1 
  b = 2 
  binding
end
a = 100 
eval("puts a + b", get_binding)
#= > 3
```

## No.34 send

```
class Quote
  def initialize
    @str = "The quick brown fox"
  end 
end
def create_method_using_a_closure
  str2 = "jumps over the lazy dog."
  Quote.send(:define_method, :display) do
    puts "#{@str} #{str2}"
  end 
end

create_method_using_a_closure
Quote.new.display
# => The quick brown fox jumps over the lazy dog.

class Quote2
  def initialize
    @str = "The quick brown fox"
  end 
end
def create_method_using_a_closure2
  str2 = "jumps over the lazy dog."
  lambda do
    puts "#{@str} #{str2}"
  end 
end
Quote2.send(:define_method, :display, create_method_using_a_closure2) 

Quote2.new.display
# => The quick brown fox jumps over the lazy dog.
```
