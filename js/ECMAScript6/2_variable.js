/**
 * 1. 数组的解构赋值
 * 本质上，这种写法属于“模式匹配”，只要等号两边的模式相同，左边的变量就会被赋予对应的值。
 * 如果等号的右边不是数组（或者严格地说，不是可遍历的结构，参见《Iterator》一章），那么将会报错。
 * 对于 Set 结构，也可以使用数组的解构赋值。
 * 只要某种数据结构具有 Iterator 接口，都可以采用数组形式的解构赋值
 */

let [a, b, c] = [1, 2, 3];
let [foo, [[bar], baz]] = [1, [[2], 3]];

let [ , , third] = ["foo", "bar", "baz"];
third // "baz"

let [head, ...tail] = [1, 2, 3, 4];
head // 1
tail // [2, 3, 4]

let [x, y, ...z] = ['a']; // 'a' undefined []
let [x1, y1, z1] = new Set(['a', 'b', 'c']);

/**
 * 1.1. 默认值
 * ES6 内部使用严格相等运算符（===），判断一个位置是否有值。
 * 所以，如果一个数组成员不严格等于undefined，默认值是不会生效的。
 * 
 */
let [x2 = 1] = []; // 1
let [x3 = 1] = [undefined]; // 1
let [x4 = 1] = [null]; // null  因为null不严格等于undefined。
let [x5 = 1, y5 = x5] = [];     // x5=1; y5=1
let [x6 = 1, y6 = x6] = [2];    // x6=2; y6=2
let [x7 = 1, y7 = x7] = [1, 2]; // x7=1; y7=2
// let [x8 = y8, y8 = 1] = [];     // ReferenceError

/**
 * 2. 对象的解构赋值
 */

let { bar1, foo1, baz1 } = { foo1: "aaa", bar1: "bbb" };
console.log(bar1, foo1, baz1) // bbb aaa undefined

let { foo2: baz2 } = { foo2: "aaa", bar: "bbb" };
console.log(baz2) // "aaa"
// foo2 // error: foo is not defined

/**
 * 3. 字符串的解构赋值
 */
const [a1, b1, c1, d1, e1] = 'hello';
let {length : len} = 'hello';
len // 5

/**
 * 4. 数值和布尔值的解构赋值
 * 解构赋值时，如果等号右边是数值和布尔值，则会先转为对象。
 * 由于undefined和null无法转为对象，所以对它们进行解构赋值，都会报错。
 */
let {toString: s} = 123;
console.log(s === Number.prototype.toString);
/**
 * 5. 函数参数的解构赋值
 */
function move({x = 0, y = 0} = {}) {
  return [x, y];
}
console.log(move({x: 3}))
/**
 * 6. 可以使用圆括号的情况只有一种：赋值语句的非模式部分，可以使用圆括号。
 */

/**
 * 7. 用途
 * ①交换变量的值
 * ②从函数返回多个值
 * ③函数参数的定义
 * ④提取JSON数据
 * ⑤函数参数的默认值
 * ⑥遍历Map结构
 * ⑦输入模块的指定方法
 */

// 1
let x9 = 1;
let y9 = 2;
[x9, y9] = [y9, x9];

// 2
function example() {
  return [1, 2, 3];
}
let [a2, b2, c2] = example();

// 4
let jsonData = {
  id: 42,
  status: "OK",
  data: [867, 5309]
};
let { id, status, data: number } = jsonData;
console.log(id, status, number);

// 6
var map = new Map();
map.set('first', 'hello');
map.set('second', 'world');
for (let [key, value] of map) {
  console.log(key + " is " + value);
}