## 类方法
new(str, safe_level=nil, trim_mode=nil, eoutvar='_erbout')

### trim_mode 

  - % enables Ruby code processing for lines beginning with %
  - <> `ERB.new("<%= 'a' %>\nb", nil, '<>').result #=> ab `
  - >  `ERB.new("<%= 'a' %>\nb", nil, '>').result #=> ab `
  - -  `ERB.new("<%= 'a' -%>\nb", nil, '-').result #=> ab `

## 实例方法
  `argument 'b' 把上文提及到的变量值绑定到erb文件中使用`

  - result(b=new_toplevel)
  - run(b=new_toplevel)

## 参考

  - <a href='http://ruby-doc.org/stdlib-2.3.1/libdoc/erb/rdoc/ERB.html' target='_blank'>erb api</a>
  - <a href='https://ruby-doc.org/core-2.2.0/Binding.html' target='_blank'>binding api</a>
  - <a href='http://stackoverflow.com/questions/7996695/what-is-the-difference-between-and-in-erb-in-rails' target='_blank'>'-' error in erb file</a>
  
## demo（生成tree）
#### a.rb
```
class HeadNote
  attr_accessor :title, :child, :index, :num, :link, :anchor
  def initialize(num, title, link, index, anchor=nil)
    @title, @num, @link, @index, @anchor = title, num, link, index, anchor
    @child = [] 
  end   
end
...
def index_to_html(heads)
  html = File.open('/home/git/b.html.erb').read
  template = ERB.new(html, nil, '-')
  template.result(binding)
end

def render(template, locals={})
  #heads = locals[:heads]
  #first_dir = locals[:first_dir]
  bind = binding
  locals.each do |k, v|
    bind.local_variable_set(k, v)
  end
  html = File.open(template).read
  template = ERB.new(html, nil, '-')
  template.result(bind)
end
...
heads = heads_array_obj(array)
=begin
heads ====>
[#<HeadNote:0x0000000280d598 @anchor="content", @index=1, @link="a.md", @num="1", @title=" Content", @child=[]>, 
#<HeadNote:0x0000000280c120 @anchor="content-1", @index=1, @link="b.md", @num="2", @title=" Content", 
@child=[#<HeadNote:0x000000027f6550 @anchor="cc", @index=2, @link="b.md", @num="2.1", @title=" cc", @child=[]>]>]
=end
puts index_to_html(heads)
```
#### b.html.erb
```
<div class="doc-project-menu-list">                                                       
  <h4 class="docu_contents">
    <a>Directory</a>
  </h4>
  <% unless heads.empty? -%> 
    <%= render '/home/git/a.html.erb', {first_dir: true, heads: heads} -%> 
  <% end -%> 
</div>
```
#### a.html.erb
```
<% unless heads.empty? -%>                                                                
  <ul class="<%= first_dir ? 'document_tree' : '' %>">
    <% heads.each do |head| -%> 
      <li title="<%= head.title %>" >
        <span class="number">
          <%= head.num %>. 
        </span>
        <a href=""><%= head.title %></a>
        <% unless head.child.empty? -%> 
          <%= render '/home/git/a.html.erb', {first_dir: false , heads: head.child}%>        
        <% end -%>
      </li> 
    <% end -%>
  </ul> 
<% end -%>
```
  
