=begin
写一个操作方法类似attr_accessor的attr_checked的类宏，该类宏用来对属性值做检验

1. 使用eval方法编写一个名为add_checked_attribute的内核方法，为指定类添加经过简单校验的属性
2. 重构add_checked_attribute方法，去掉eval方法，改用其它手段实现
3. 添加代码块校验功能
4. 修改add_checked_attribute为要求的attr_checked,并使其对所有类都可用
5. 通过引入模块的方式，只对引入该功能模块的类添加attr_checked方法

https://ruby-china.org/topics/27426
=end

# STEP1. 实现attr_accessor
def add_checked_attribute(klass, attribute)
    eval "
      class #{klass}
        def #{attribute}=(value)
          raise 'Invalid attribute' unless value
          @#{attribute} = value
        end
        def #{attribute}()
          @#{attribute}
        end
      end
    "
end
  
add_checked_attribute(String, :my_attr)
t = "hello,kitty"
t.my_attr = 100
puts t.my_attr
# t.my_attr = false
# puts t.my_attr
# (eval):4:in `my_attr=': Invalid attribute (RuntimeError)
# from attr_check.rb:34:in `<main>'


# STEP2. 重构add_checked_attribute方法
def add_checked_attribute(klass, attribute)
    klass.class_eval do
        define_method "#{attribute}=" do |value|
            raise "Invaild attribute" unless value
            instance_variable_set("@#{attribute}", value)
        end
    
        define_method attribute do
            instance_variable_get "@#{attribute}"
        end
    end
end

# STEP3. 校验功能
def add_checked_attribute(klass, attribute, &validation)
    klass.class_eval do
        define_method "#{attribute}=" do |value|
            raise "Invaild attribute" unless validation.call(value)
            instance_variable_set("@#{attribute}", value)
        end
    
        define_method attribute do
            instance_variable_get "@#{attribute}"
        end
    end
end

add_checked_attribute(String, :my_attr){|v| v >= 180 }
t = "hello,kitty"

# t.my_attr = 100  #Invaild attribute (RuntimeError)
# puts t.my_attr
# attr_check.rb:56:in `block (2 levels) in add_checked_attribute': Invaild attribute (RuntimeError)
# from attr_check.rb:69:in `<main>
t.my_attr = 200
puts t.my_attr

# STEP4. 修改add_checked_attribute为要求的attr_checked,并使其对所有类都可用
class Class
    def add_checked(attribute, &validation)
        define_method "#{attribute}=" do |value|
            raise "Invaild attribute" unless validation.call(value)
            instance_variable_set("@#{attribute}", value)
        end
  
        define_method attribute do
            instance_variable_get "@#{attribute}"
        end
    end
end

String.add_checked(:my_attr){|v| v >= 180 }
t = "hello,kitty"

# t.my_attr = 100  #Invaild attribute (RuntimeError)
# puts t.my_attr
# attr_check.rb:80:in `block in add_checked': Invaild attribute (RuntimeError)
# from attr_check.rb:93:in `<main>'

t.my_attr = 200
puts t.my_attr  #200

# STEP.5 通过引入模块的方式，只对引入该功能模块的类添加attr_checked方法
module CheckedAttributes
    def self.included(base)
        base.extend ClassMethods
    end

    module ClassMethods
        def attr_checked(attribute, &validation)
            define_method "#{attribute}=" do |value|
                raise "Invaild attribute" unless validation.call(value)
                instance_variable_set("@#{attribute}", value)
            end
      
            define_method attribute do
                instance_variable_get "@#{attribute}"
            end
        end
    end
end

class Person
    include CheckedAttributes
    attr_checked :age do |v|
        v >= 18
    end
end

me = Person.new
me.age = 39  #ok
p me.age
# me.age = 12  #抛出异常
# p me.age
# attr_check.rb:110:in `block in attr_checked': Invaild attribute (RuntimeError)
# from attr_check.rb:131:in `<main>'