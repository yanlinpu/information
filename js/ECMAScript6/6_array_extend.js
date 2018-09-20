/**
 * Array.from()
 * 用于将两类对象转为真正的数组
 * 任何有length属性的对象，都可以通过Array.from方法转为数组
 * Array.from还可以接受第二个参数，作用类似于数组的map方法，用来对每个元素进行处理，将处理后的值放入返回的数组。
 * 如果map函数里面用到了this关键字，还可以传入Array.from的第三个参数，用来绑定this。
 */

let arrayLike = {
    '0': 1,
    '1': 3,
    '2': 9,
    '3': 10,
    length: 3
}
// ES6的写法
console.log(Array.from(arrayLike)); // [ 1, 3, 9 ]
console.log(Array.from({ length: 3 })) // [ undefined, undefined, undefined ]

console.log(Array.from(arrayLike, x => x * x));
// 等同于 [ 1, 9, 81 ]
console.log(Array.from(arrayLike).map(x => x * x));
console.log(Array.from([1, , 2, , 3], (n) => n || 0)); // [ 1, 0, 2, 0, 3 ]

/**
 * Array.of()
 * 用于将一组值，转换为数组。
 */

/**
 * 数组实例的find()和findIndex() 
 */

console.log(`${[-1, 4, -5, 10].find((n) => n > 0)}`) // 4

/**
 * 数组实例的entries()，keys()和values()
 * 它们都返回一个遍历器对象（详见《Iterator》一章），可以用for...of循环进行遍历，
 * 唯一的区别是keys()是对键名的遍历、values()是对键值的遍历，entries()是对键值对的遍历。
 */

for (let [index, elem] of ['a', 'b'].entries()) {
  console.log(index, elem);
}
// 0 "a"
// 1 "b"

/**
 * 数组实例的 includes()
 * return true or false
 */
