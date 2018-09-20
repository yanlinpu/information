/**
 * 1. RegExp构造函数
 * 如果RegExp构造函数第一个参数是一个正则对象，那么可以使用第二个参数指定修饰符。
 * 而且，返回的正则表达式会忽略原有的正则表达式的修饰符，只使用新指定的修饰符。
 */

console.log(new RegExp(/abc/ig, 'i').flags); // i

/**
 * 字符串的正则方法
 * 字符串对象共有4个方法，可以使用正则表达式：
 *      match()、replace()、search()和split()。
 */

