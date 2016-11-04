# Render template and change url string in browser

## 描述
controller :projects_controller

action :index, :edit, :update

update更新的时候出错，在edit中显示，页面内容显示正确，url跳转到却非edit_path

参考
[Render template and change url string in browser?](http://stackoverflow.com/questions/4707471/render-template-and-change-url-string-in-browser)

## 实现

-  config/routes.rb

```
match '/project/:id/edit' => "project#update", constraints: {id: /.+/}, :via => [:put], 
  :as => :put_project
```
- app/views/...

```
- if @error.present?
  .alert.alert-danger
    = @error
= form_for @project, :url => put_project_path, :method => "put" do |f|
  ...
```
- app/controller/...

```
def update
  ...
  if ...
    @error = ""
    render action: 'edit'
    return
  end
  ...
end
```
