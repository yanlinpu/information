## module.export 和 export方法的区别

======

1. me.js

```
exports.name = function() {
    console.log('My name is ylp');
};
```

2. me_test.js

```
var rocker = require('./me.js');
rocker.name(); // 'My name is ylp'
```

3. 其实，Module.exports才是真正的接口，exports只不过是它的一个辅助工具。　最终返回给调用的是Module.exports而不是exports。

```

/**
 *  所有的exports收集到的属性和方法，都赋值给了Module.exports。
 *  这有个前提，就是Module.exports本身不具备任何属性和方法。
 *  如果，Module.exports已经具备一些属性和方法，那么exports收集来的信息将被忽略。
 */


// me2.js
module.exports = 'ME';
exports.name = function() {
    console.log('My name is Lemmy Kilmister');
};

// me2_test.js
var rocker = require('./me2.js');
rocker.name(); // TypeError: Object ME has no method 'name'

/**
 *  模块并不一定非得返回“实例化对象”。你的模块可以是任何合法的JavaScript对象
 *  boolean, number, date, JSON, string, function, array等等。
 *  你的模块可以是任何你设置给它的东西。
 *  如果你没有显式的给Module.exports设置任何属性和方法，
 *  那么你的模块就是exports设置给Module.exports的属性。
 *  me3模块是一个类
 */

// me3.js
function APIClient(apiBase, appId, apiKey, name) {
    this.api_base = apiBase;
    this.app_id = appId;
    this.api_key = apiKey;
    this.name = name;
}
require("./lib/name.js")(APIClient.prototype);
module.exports = APIClient;

// name.js
module.exports = function (proto) {
    proto.me = function(age){
        return `my name is ${this.name}, and my age is ${age}.`
    }
};

// me3_test.js
var ME = require('./me.js');
var myself = new ME('apibase', 'appid', 'apikey', 'ylp');
console.log(myself.me(28)); // my name is ylp, and my age is 28.
```
