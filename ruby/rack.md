# 1.ruby rack request & response

### hello.rb
```
# hello.rb
class HelloApp                                                                                                                                                                  
  def call(env)
    request = Rack::Request.new env
    p "name => #{request.params['name']}"
    p "name => #{request['name']}"
    case request.path_info
    when "/hello"
      return_result("Hello, Rack World!")
    when "/get_env"
      return_result(pp(env))
    when "/info"
      return_result(get_something_env(env))
    when "/response_write"
      response_write
    when "/response_body"
      response_body
    when "/baidu"
      redirect_to_baidu
    else
      return_result("you need input other info")
    end
  end

  private

  def return_result(res)
    [200, {"Content-Type"=>"text/plain"}, [res<<"\n"]]
  end 

  def pp(hash,mol="\n")
    hash.map {|key,value|
      "#{key} => #{value}"
    }.sort.join(mol) << mol 
  end 

  def get_something_env(env)
    "your request:\n  http_method => #{env['REQUEST_METHOD']}\n  path => #{env['PATH_INFO']}\n  params => #{env['QUERY_STRING']} \n"
  end 

  def response_body
    response = Rack::Response.new
    body = "=======header=========\n"
    body << "Rack::Response body\n"
    body << "=======footer=========\n"
    response.body = [body]
    # 直接设置body时，需要设置响应头Content-Length 为string
    response.headers['Content-Length'] = body.bytesize.to_s # string 
    response.finish
  end

  def response_write
    # write 时自动填充Content-Length值
    response = Rack::Response.new
    response.write("=======header=========\n")
    response.write("Rack::Response write\n")
    response.write("=======footer=========\n")
    response.finish
  end

  def redirect_to_baidu
    response = Rack::Response.new
    response.redirect("https://www.baidu.com")
    response.finish
  end
end
```

### hello.ru
```
# hello.ru
require 'rubygems'
require 'rack'
require './hello'
# run HelloApp.new # 9292 if default
Rack::Handler::WEBrick.run HelloApp.new, :Port=>3002
```

### 启动

```
$ rackup hello.ru || rackup hello.ru -p ...
```

### curl 访问
```
$ curl http://127.0.0.1:3002/baidu
```
# 2.中间件

```
# rack_app.rb
require 'rubygems'                                                                                                                                                              
require 'rack'
require './decorator'

rack_app = lambda{|env|
  request = Rack::Request.new(env)
  response = Rack::Response.new
  if request.path_info == "/" 
    response.write("root\n")
  else
    response.write("no route for #{request.path_info}\n")
  end 
  response.finish
}

Rack::Handler::WEBrick.run Decorator.new(rack_app), :Port=>3002
```

```
# decorator.rb
class Decorator                                                                                                                                                                 
  def initialize(app)
    @app = app 
  end 

  def call(env)
    status, headers, body = @app.call(env)
    new_body = "=====header=====\n"
    body.each {|str| new_body << str}
    new_body << "=====footer=====\n"
    headers['Content-Length'] = new_body.bytesize.to_s
    [status, headers, [new_body]]
  end 
end
```

### 启动

```
$ ruby rack_app.rb
```

# 3.Rack::Builder

```
require 'rubygems'                                                                                                                                                              
require 'rack'
require './decorator'

rack_app = lambda{|env|
  request = Rack::Request.new(env)
  response = Rack::Response.new
  if request.path_info == "/" 
    response.write("root\n")
  else
    response.write("no route for #{request.path_info}\n")
  end 
  response.finish
}

app = Rack::Builder.new {
  use Rack::ContentLength 
  use Decorator
  run rack_app
}.to_app

Rack::Handler::WEBrick.run app, :Port=>3002
```

# 4. rackup

```
map '/hello' do
  run lambda {|env| [200, {"Content-Type"=>"text/plain"}, ["hello"]]}
end 
```

# 5.demo 检查代理的可用性

### proxy.sh
```
#!/bin/sh                                                                                

PROXYS=(10.167.159.45:8889 10.57.89.177:8899 10.57.91.89:8889)
for i in "${PROXYS[@]}"
do
  curl -x http://$i --connect-timeout 1 www.baidu.com 1>/dev/null 2>&1
  if [ $? == 0 ]; then
    echo "$i"
  fi  
done
```

### 第一种web访问方法 proxy.rb
```
#调用 ruby proxy.ru 然后网页访问localhost:8080
require 'webrick'
server = WEBrick::HTTPServer.new Port: 8080

class Handler < WEBrick::HTTPServlet::AbstractServlet
  def do_GET req, res 

    if req.path == '/' 
      output = `bash proxy.sh`
      res.body = output.to_s
    else
      res.body = "hehe"
    end 
  end 
end

server.mount '/', Handler

trap 'INT' do server.shutdown end 

server.start
```

### 第二种web访问方法 proxy.rb
```
#调用 ruby proxy.rb 然后网页访问localhost:8080
require 'rack'                                                                           

class ProxyUseful
  def call(env)
    output = `bash proxy.sh`
    ['200', {'Content-Type' => 'text/html'}, [output.to_s]]
  end 
end

Rack::Handler::WEBrick.run ProxyUseful.new, :Port => 8080
```

### 第三种web访问方法 proxy.ru
```
#调用 rackup proxy.ru -p 8080 然后网页访问localhost:8080
require 'rack'                                                                           

class ProxyUseful
  def call(env)
    output = `bash proxy.sh`
    ['200', {'Content-Type' => 'text/html'}, [output.to_s]]
  end 
end

run ProxyUseful.new
```

# 6.资料

http://dl2.iteye.com/upload/attachment/0021/1135/a90b29e3-53dd-37fa-b2b3-f16b6bfee18b.pdf
