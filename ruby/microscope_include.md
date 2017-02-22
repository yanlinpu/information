## Ruby原理剖析(ruby under a microscope)

page.165 and page.158

```
module A
  def a
    "aa"
  end 
end

module B
  include A
  def b
    "bb"
  end 
end

class C
  include B
end

c = C.new
puts c.a 
puts c.b 

module D
  def d
    'dd'
  end 
end

module B
  include D
  def bb
    "bbbbbbb"
  end 
end

c2 = C.new
puts c.bb
puts c2.bb
#puts c.d
#undefined method `d' for #<C:0x0000000114a978> (NoMethodError)
puts c2.d 
# undefined method `d' for #<C:0x0000000114a978> (NoMethodError)
# module D 是被include到原始的module B中， 而不是class C用的那本被include B的副本中。
```
