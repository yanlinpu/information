## Extend through Include 


```
#===============Extend through Include==================#
#http://www.dan-manges.com/blog/27
module BasicMath
  def add(number)
    self + number
  end
end

Fixnum.class_eval do
  include BasicMath   # instance method
end
p 3.add(4)    # => 7

module ExtendMe
  def verbal_object_id
    "my object id is #{self.object_id}"
  end
end

class Person
  extend ExtendMe   # class method
end
p Person.verbal_object_id    #=>  "my object id is ......"

# 添加实例方法和类方法
# self.included -> extend(one module(ClassMethods) in this module(ExtendThroughInclude))
# and the methods in ClassMethods are class_methods for which included ExtendThroughInclude(Person)
module ExtendThroughInclude
  def self.included(klass)
    klass.extend ClassMethods
  end

  def instance_method
    "this is an instance of #{self.class}"
  end

  module ClassMethods
    def class_method
      "this is a method on the #{self} class"
    end
  end
end

class Person
  include ExtendThroughInclude
end
p Person.new.instance_method  #=> "this is an instance of Person"
p Person.class_method         #=> "this is a method on the Person class"

class ABC
end

module Example
  def self.included(base)
    base.class_eval do
      def example
        "instance method"
      end

      def self.example
        "class method"
      end
    end
  end
end

ABC.include Example

ABC.example  # "class method"

ABC.new.example  #"instance method"

module A
  def my_method
    puts "method in A"
  end
end

module AA
  def my_method
    puts "method in AA"
  end
end

class B
  include A
  include AA
  def my_method
    puts "method in B"
  end
end

# ruby prepend 与 include 类似，
# 首先都是添加实例方法的，
# 不同的是扩展module在祖先链上的放置位置不同
class C
  prepend A
  def my_method
    puts "method in C"
  end
end

class D
  include A
  include AA
end

B.new.my_method   # => method in B
C.new.my_method   # => method in A
D.new.my_method   # => method in AA
puts B.ancestors  # => B AA A Object Kernel BasicObject
puts C.ancestors  # => A C Object Kernel BasicObject
puts D.ancestors  # => D AA A Object Kernel BasicObject
```

```
#b.rb
# The self.included function is called when the module is included.
# It allows methods to be executed in the context of the base (where the module is included)
module B
  def method_missing(action, *args, &block)
    p action.to_s
    p args
    yield if block_given?
  end

  def self.included(c)
    # 定义类方法
    # The magic here is the define_singleton_method that is new in Ruby 1.9.1 
    # - it works the same as define_method,
    # but for class methods instead of instance methods.
    def c.define_remote_methods(*args)
      args.each do |method_name|
        self.define_singleton_method(method_name) do |*method_args, &block|
          p method_name
          p method_args
          block.call unless block.nil?
          # cannot use yield inside a define_method block
          # https://banisterfiend.wordpress.com/2010/11/06/behavior-of-yield-in-define_method/
          # 不管是否存在block  block_given? = false 所以下面不执行
          yield if block_given?
        end
      end
    end

    def c.set_create_methods(*args)
      @create_methods = args
    end

    def c.create_methods
      @create_methods || []
    end
  end
end
```

```
# a.rb
require './b'
class A
  include B
  set_create_methods :a, :b, :c
  define_remote_methods :d, :e, :f
end

puts A.methods.grep /create/        # => set_create_methods create_methods
puts A.create_methods               # => a b c
A.new.a(1,2,3){p "block given"}     # => "a" [1,2,3] "block given"
A.new.b(2)                          # => "b" [2]

A.d(5,6,7) { p "block given" }      # => :d [5,6,7] "block given"
A.d(5,6,7)                          # => :d [5,6,7]
```

## define_method(meth) { |args, &block| if block ... else ... end ... } 
```
obj = Object.new
class << obj 
  define_method :a do
    yield
  end 

  define_method :b do |*args, &block|
    if block_given? # return false always
      puts 'block is exist'
      block.call(*args)
    else
      puts 'block not exist'
    end 
  end 

  define_method :c do |*args, &block|
    if block
      puts 'block is exist'
      block.call(*args)
    else
      puts 'block not exist'
    end 
  end 
end
#puts obj.a{puts 'hi'}
# => `block in singleton class': no block given (yield) (LocalJumpError)
puts obj.b
# => block not exist
puts obj.b("ylp") {|body| puts "hello #{body}"}
# => block not exist
puts obj.c
# => block not exist
puts obj.c("ylp") {|body| puts "hello #{body}"}
# => block is exist
# => hello ylp
```
