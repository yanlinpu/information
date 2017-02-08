```
class A                                                                                                                                                                                
  @type = "A" 
  @@t  = "AA"
  def self.type
    @type
  end 
  def self.t
    @@t 
  end 
end
class B < A 
  @type = "B" 
  @@t  = "BB"
end
puts "@@类变量共享 @类实例变量不共享"
puts "A.type :#{A.type}" 
puts "B.type :#{B.type}" 
puts "A.t :#{A.t}" 
puts "B.t :#{B.t}" 

class A
  @@t = "changed"
end
puts "A.t :#{A.t}" 
puts "B.t :#{B.t}" 


=begin
@@类变量共享 @类实例变量不共享
A.type :A
B.type :B
A.t :BB
B.t :BB
A.t :changed
B.t :changed
=end
```
