/**
 * 1. let基本用法
 * ES6 新增了let命令，用来声明变量。它的用法类似于var，但是所声明的变量，只在let命令所在的代码块内有效。
 * for循环的计数器，就很合适使用let命令。
 * 计数器i只在for循环体内有效，在循环体外引用就会报错。
 */

{
  let a = 10;
  var b = 1;
}
b
// a // *************** ===> ReferenceError: a is not defined.

/**
 * 变量i是var命令声明的，在全局范围内都有效，所以全局只有一个变量i。
 * 每一次循环，变量i的值都会发生改变，而循环内被赋给数组a的函数内部的console.log(i)，里面的i指向的就是全局的i。
 * 也就是说，所有数组a的成员里面的i，指向的都是同一个i，导致运行时输出的是最后一轮的i的值，也就是10。
 * 如果使用let，声明的变量仅在块级作用域内有效，最后输出的是6。
 */
var a = [];
for (var i = 0; i < 10; i++) {
  a[i] = function () {
    console.log(i);
  };
}
a[6](); // 10

var b = [];
for (let i = 0; i < 10; i++) {
  b[i] = function () {
    console.log(i);
  };
}
b[6](); // 6

/**
 * 2. let不存在变量提升
 * var命令会发生”变量提升“现象，即变量可以在声明之前使用，值为undefined。
 */

// 变量foo用var命令声明，会发生变量提升，即脚本开始运行时，变量foo已经存在了，但是没有值，所以会输出undefined。
console.log(foo); // 输出undefined 
var foo = 2;

// 变量bar用let命令声明，不会发生变量提升。这表示在声明它之前，变量bar是不存在的，这时如果用到它，就会抛出一个错误。
// console.log(bar); // *************** ===> ReferenceError: bar is not defined
// let bar = 2;

/**
 * 3. let暂时性死区
 * 只要块级作用域内存在let命令，它所声明的变量就“绑定”（binding）这个区域，不再受外部的影响。
 * ES6明确规定，如果区块中存在let和const命令，这个区块对这些命令声明的变量，从一开始就形成了封闭作用域。凡是在声明之前就使用这些变量，就会报错。
 * 在代码块内，使用let命令声明变量之前，该变量都是不可用的。
 * “暂时性死区”也意味着typeof不再是一个百分之百安全的操作。
 */
let tmp = 456;
if (true) {
  // tmp = 'abc'; // ReferenceError: tmp is not defined
  // console.log(tmp); // ReferenceError
  console.log(typeof(x)); // undefined
  // console.log(typeof(tmp)); // ReferenceError
  let tmp;
  console.log(tmp); // undefined
  tmp = 123;
  console.log(tmp); // 123
}

/**
 * 4. let不允许重复声明
 * 不能重复声明同一个变量
 * 不能在函数内部重新声明参数
 */

/**
 * 5. ES6 的块级作用域
 * ①内层变量可能会覆盖外层变量
 * ②用来计数的循环变量泄露为全局变量
 * 
 * let实际上为 JavaScript 新增了块级作用域。
 */

// 内层变量可能会覆盖外层变量
var tmp2 = new Date();
function f() {
  console.log(tmp2);
  if (false) {
    var tmp2 = 'hello world';
  }
}
f(); // undefined
// 用来计数的循环变量泄露为全局变量
var s = 'hello';
for (var i = 0; i < s.length; i++) {}
console.log(i); // 5

function f1() {
  let n = 5;
  if (true) {
    let n = 10;
  }
  console.log(n); // 5
}
f1()
/**
 * 6. 块级作用域与函数声明
 * ①允许在块级作用域内声明函数。
 * ②函数声明类似于var，即会提升到全局作用域或函数作用域的头部。
 * ③同时，函数声明还会提升到所在的块级作用域的头部。
 * ES6 的块级作用域允许声明函数的规则，只在使用大括号的情况下成立，如果没有使用大括号，就会报错。
 */

/**
 * 7. do表达式
 * 本质上，块级作用域是一个语句，将多个操作封装在一起，没有返回值。
 * 使得块级作用域可以变为表达式，也就是说可以返回值，办法就是在块级作用域之前加上do，使它变为do表达式。
 */

/**
 * 8. const 命令
 * const声明一个只读的常量。一旦声明，常量的值就不能改变。
 * const一旦声明变量，就必须立即初始化，不能留到以后赋值。
 * const的作用域与let命令相同：只在声明所在的块级作用域内有效。
 * const声明的常量，也与let一样不可重复声明。
 */

/**
 * 9. 顶层对象的属性
 * 顶层对象，在浏览器环境指的是window对象，在Node指的是global对象
 */