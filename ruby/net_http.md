## Net::HTTP post & get

```
require 'net/http'
require 'json'

class Api
  def self.get_allowed_with_http(url, params)
    post(url, params)
  end

  private

  class << self
    def get(url)
      uri = URI(url)
      request = net_http(uri, 'get')
      exec_request(uri, request)
    end

    def post(url, params)
      uri = URI(url)
      request = net_http(uri)
      request.body = params.to_json
      exec_request(uri, request)
    end

    def net_http(uri, type='post')
      request = type == 'post' ? Net::HTTP::Post.new(uri.request_uri) : Net::HTTP::Get.new(uri.request_uri)
      request['Content-Type'] = 'application/json;charset=utf-8'
      request['User-Agent'] = 'Mozilla/5.0 (Windows NT 5.1; rv:29.0) Gecko/20100101 Firefox/29.0'
      request['X-ACL-TOKEN'] = get_token
      # request['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0"
      # request['Connection'] = "keep-alive"
      # request['Cache-Control'] = "max-age=0"
      # request['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
      # request['Accept-Language'] = "en-US,en;q=0.5"
      return request
    end

    def exec_request(uri, request)
      http = Net::HTTP.new(uri.host, uri.port)
      if uri.scheme == "https"
        http.verify_mode = OpenSSL::SSL::VERIFY_NONE
        http.use_ssl = true
      end
      response = http.start { |http| http.request(request) }
      JSON.parse(response.body) rescue response.body
    rescue => e
      # Logger.info e.message
      puts e.message
      return nil
    end

    def get_token
      'token_value'
    end
  end
end

# post 请求
url = 'http://192.168.5.93:3000/api/v3/internal/allowed_with_http'
params = {
    username: 'ylp',
    password: '...',
    project: 'ylp/assdf',
    action: 'git-upload-pack'
}

puts Api.get_allowed_with_http(url, params)
```

\****************************************************************************************************************************************
 
\****************************************************************************************************************************************  

```
require 'net/http'
require 'json'

class Api

  def get_allowed_with_http(url, params)
    post(url, params)
  end

  private

  def get(url)
    uri = URI(url)
    http = Net::HTTP.new(uri.host, uri.port)
    if uri.scheme == "https"
      http.verify_mode = OpenSSL::SSL::VERIFY_NONE
      http.use_ssl = true
    end

    begin
      request = Net::HTTP::Get.new(uri.request_uri)
      request['Content-Type'] = 'application/json;charset=utf-8'
      request['User-Agent'] = 'Mozilla/5.0 (Windows NT 5.1; rv:29.0) Gecko/20100101 Firefox/29.0'
      request['X-ACL-TOKEN'] = get_token
      response = http.start {|http| http.request(request) }
      JSON.parse(response.body) rescue response.body
    rescue Exception => e
      # Logger.info e.message
      puts e.message
      return nil
    end
  end

  def post(url, params)
    begin
      uri = URI(url)
      http = Net::HTTP.new(uri.host, uri.port)
      if uri.scheme == "https"
        http.verify_mode = OpenSSL::SSL::VERIFY_NONE
        http.use_ssl = true
      end
      request = Net::HTTP::Post.new(uri.request_uri)
      request['Content-Type'] = 'application/json;charset=utf-8'
      request['User-Agent'] = 'Mozilla/5.0 (Windows NT 5.1; rv:29.0) Gecko/20100101 Firefox/29.0'
      request['X-ACL-TOKEN'] = get_token
      request.body = params.to_json
      response = http.start { |http| http.request(request) }
      JSON.parse(response.body) rescue response.body
    rescue => e
      # Logger.info e.message
      puts e.message
      return nil
    end
  end

  def get_token
    'token_value'
  end
end

url = 'http://192.168.5.93:3000/api/v3/internal/allowed_with_http'
params = {
    username: 'ylp',
    password: '...',
    project: 'ylp/assdf',
    action: 'git-upload-pack'
}

puts Api.new.get_allowed_with_http(url, params)
```
