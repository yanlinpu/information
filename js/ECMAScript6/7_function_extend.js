/**
 * 函数参数的默认值
 */

// 写法一
function m1({x = 0, y = 0} = {}) {
  console.log([x,y]);
}

// 写法二
function m2({x, y} = { x: 0, y: 0 }) {
  console.log([x,y]);
}
// 上面两种写法都对函数的参数设定了默认值，区别是写法一函数参数的默认值是空对象，但是设置了对象解构赋值的默认值；
// 写法二函数参数的默认值是一个有具体属性的对象，但是没有设置对象解构赋值的默认值。
// 函数没有参数的情况
m1() // [0, 0]
m2() // [0, 0]

// x和y都有值的情况
m1({x: 3, y: 8}) // [3, 8]
m2({x: 3, y: 8}) // [3, 8]

// x有值，y无值的情况
m1({x: 3}) // [3, 0]
m2({x: 3}) // [3, undefined]

// x和y都无值的情况
m1({}) // [0, 0];
m2({}) // [undefined, undefined]

m1({z: 3}) // [0, 0]
m2({z: 3}) // [undefined, undefined]
