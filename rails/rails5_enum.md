## enum 用法

- app/models/report.rb

```
class Report < ApplicationRecord
  enum category: [:irrational, :smoking, :take_photo, :vulgar, :garbarge, :toilet, :loudly, :jump_queue, :norespect, :spitting, :others]
end
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
  <% enum_options_for_select(Report, :category).each do |cg| %>
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

- 注意事项

  - http://stackoverflow.com/questions/43116134/rails-i18n-how-to-translate-enum-of-a-model
    `<%= form.label :category %> error zh-CN.yml`
  - https://mikerogers.io/2016/05/19/improving-rails-enums-using-i18n.html
    `show helpers`

