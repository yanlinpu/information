## enum 用法

- app/models/report.rb

```
class Report < ApplicationRecord
  def initialize(*)
    super
  rescue ArgumentError
    raise if valid?
  end

  enum category: [:irrational, :smoking, :take_photo, :vulgar, :garbarge, :toilet, :loudly, :jump_queue, :norespect, :spitting, :others]
end

  validates :category, inclusion: { in: categories, message: "%{value} is not valid,please select in #{ApplicationController.helpers.enum_validation(Report, :category)}" }

```
- app/helpers/enum_i18n_helper.rb

```
module EnumI18nHelper

  # Returns an array of the possible key/i18n values for the enum
  # Example usage:
  # enum_options_for_select(Report, :category)
  def enum_options_for_select(class_name, enum)
    class_name.send(enum.to_s.pluralize).map do |key, _|
      [enum_i18n(class_name, enum, key), key]
    end
  end
  # Returns the i18n version the the models current enum key
  # Example usage:
  # enum_l(report, :category)
  def enum_l(model, enum)
    enum_i18n(model.class, enum, model.send(enum))
  end

  # Returns the i18n string for the enum key
  # Example usage:
  # enum_i18n(Report, :approval_state, :unprocessed)
  def enum_i18n(class_name, enum, key)
    I18n.t("activerecord.attributes.#{class_name.model_name.i18n_key}/#{enum.to_s}.#{key}")
  end

  def enum_validation(class_name, enum)
    result = []
    enum_options_for_select(class_name, enum).each_with_index do |value, index|
      result << [index, value.first]
    end
    result
  end
end

```

- app/views/reports/_form.html.erb

```
<%= form_with(model: report, local: true) do |form| %>
  <%# select %>
  <div class="field">
    <%= form.label :category %>
    <%= form.select :category, enum_options_for_select(Report, :category) %>
  </div>
  <%# redio %>
  <% enum_options_for_select(Report, :category).each_with_index do |cg, i| %>
    <% if @report.category.nil? %>
      <%= form.radio_button(:category, cg.last, { checked: i==0 }) %>
    <% else %>
      <%= form.radio_button(:category, cg.last) %>
    <% end %>
    <%= cg.first %>
  <% end %>
<% end %>
```

- app/views/reports/show.html.erb

```
...
<p>
  <strong>Category:</strong>
  <%= enum_l(@report, :category) %>
</p>
...
```

- config/application.rb

```
config.active_record.default_timezone = :local

# Whitelist locales available for the application
I18n.available_locales = [:en, "zh-CN"]

# Set default locale to something other than :en
I18n.default_locale = "zh-CN"
```

- config/locales/zh-CN.yml

```
# coding: utf-8
zh-CN:
  activerecord:
    attributes:
      report/category: #参考注意事项
        irrational: "对待服务不周等情况不理智"
        smoking: "公共场合吸烟"
        take_photo: "在禁止拍照区域拍照"
        vulgar: "言语粗俗"
        garbarge: "随地扔垃圾"
        toilet: "随地大小便"
        loudly: "公共场合大声喧哗"
        jump_queue: "随意插队"
        norespect: "不尊重当地居民风俗"
        spitting: "随地吐痰"
        others: "其他"
```

- 注意事项

  - http://stackoverflow.com/questions/43116134/rails-i18n-how-to-translate-enum-of-a-model
    `<%= form.label :category %> error zh-CN.yml`
  - https://mikerogers.io/2016/05/19/improving-rails-enums-using-i18n.html
    `show helpers`
  - https://github.com/rails/rails/issues/13971 
    `validation with enum: ActiveRecord enum: use validation if exists instead of raising ArgumentError`
