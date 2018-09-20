/**
 * 字符串的遍历器接口
 * ES6为字符串添加了遍历器接口（详见《Iterator》一章），使得字符串可以被for...of循环遍历。
 */

for (let codePoint of 'foo') {
  console.log(codePoint)
}

/**
 * at()
 * npm install string.prototype.at
 * require('string.prototype.at');
 */

require('string.prototype.at');
console.log('abc'.at(0)) // "a"
console.log('𠮷1'.at(0)) // "𠮷"
console.log('𠮷1'.at(2)) // "1"

/**
 * includes(), startsWith(), endsWith()
 * 这三个方法都支持第二个参数，表示开始搜索的位置。
 */

var s = 'Hello world!';
console.log(s.startsWith('world', 6)) // true
console.log(s.endsWith('Hello', 5)) // true
console.log(s.includes('Hello', 6)) // false

/**
 * repeat()
 * repeat方法返回一个新字符串，表示将原字符串重复n次。
 */

/**
 * padStart()，padEnd()
 * 字符串补全长度的功能
 * padStart()用于头部补全，padEnd()用于尾部补全
 */

/**
 * 模板字符串
 * 是增强版的字符串，用反引号（`）标识。它可以当作普通字符串使用，也可以用来定义多行字符串，或者在字符串中嵌入变量。
 */

console.log(`string text line 1
string text line 2`);

// 字符串中嵌入变量
var name = "Bob", time = "today";
console.log(`Hello ${name}, how are you ${time}?`)

