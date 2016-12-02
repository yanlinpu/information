## 邮件发送设置 读取数据库和配置文件可切换

- db

```
class AddEmailConfigInSystemConfigs < ActiveRecord::Migration
  def up
    SystemConfig.create(item_name:"email_config_enable", item_value:"false", item_desc:"是否使用email的数据库配置")
    email_conf = SystemConfig.where(["item_name=?", "email_config_enable"]).first

    SystemConfig.create(item_name:"email_config_user_name", item_value: "", item_desc:"发送邮件的邮箱",parent_id:email_conf.id)
    SystemConfig.create(item_name:"email_config_password", item_value: "", item_desc:"发送邮件的密码",parent_id:email_conf.id)
    SystemConfig.create(item_name:"email_config_address", item_value: "", item_desc:"发送邮件的地址",parent_id:email_conf.id)
    SystemConfig.create(item_name:"email_config_domain", item_value: "", item_desc:"发送邮件的域名",parent_id:email_conf.id)
    SystemConfig.create(item_name:"email_config_port", item_value: "465", item_desc:"发送邮件的端口",parent_id:email_conf.id)
    SystemConfig.create(item_name:"email_config_ssl", item_value: "true", item_desc:"是否使用sll验证",parent_id:email_conf.id)
    SystemConfig.create(item_name:"email_config_authentication", item_value: "login", item_desc:"认证方式",parent_id:email_conf.id)
  end

  def down
    email_conf = SystemConfig.where(["item_name=?","email_config_enable"]).first
    email_conf.destroy
    SystemConfig.where(parent_id:email_conf.id).destroy_all
  end
end
```

- smtp_settings  monkey patch

```
  ...
  # default from: Settings.email_config.email_from
  default from: Proc.new{ get_from_email }


  private

  def get_from_email
    email_config_enable = SystemConfig.find_by_item_name("email_config_enable")
    if email_config_enable && email_config_enable.item_value == "true"
      SystemConfig.find_by_item_name("email_config_user_name").try("item_value")
    else
      Settings.email_config.email_from
    end
  end

  # import monkey patch 
  def self.smtp_settings
    email_config_enable = SystemConfig.find_by_item_name("email_config_enable")
    if email_config_enable && email_config_enable.item_value == "true"
      config_hash = {}
      configs = SystemConfig.where(parent_id: email_config_enable.id)
      configs.each do |config|
        key = config.item_name.to_s.sub(/^email_config_/, "")
        config_hash[key.to_sym] = config.item_value if key.present?
      end
      config_hash[:ssl] = config_hash[:ssl]=="false" ? false : true

      super.merge!(config_hash)
    else
      config_hash = Settings.email_config
      config_hash.delete(:email_from)
      super.merge!(config_hash.symbolize_keys)
    end
  end
  ...

```
