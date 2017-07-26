# mocha + expect

## mocha

mocha 提供 TDD（测试驱动开发）、BDD (行为驱动开发) 和 exports 风格的接口。

BDD风格（Behavior-Driven Development）:

BDD认为，不应该针对代码的实现细节写测试，而是要针对行为写测试。BDD测试的是行为，即软件应该怎样运行。

BDD接口提供以下方法：

1. describe()：测试套件

    ```
    describe("A suite", function() {
        // ...
    });
    ```
1. it()：测试用例
1. before()：所有测试用例的统一前置动作
1. after()：所有测试用例的统一后置动作
1. beforeEach()：每个测试用例的前置动作
1. afterEach()：每个测试用例的后置动作

BDD hook:

hook也可以理解为是一些逻辑，通常表现为一个函数或者一些声明，当特定的事件触发时 hook 才执行。

提供方法有：before()、beforeEach() after() 和 afterEach()。

```
describe('hooks', function() {
    before(function() {
        //在执行本区块的所有测试之前执行
    });

    after(function() {
        //在执行本区块的所有测试之后执行
    });

    beforeEach(function() {
        //在执行本区块的每个测试之前都执行
    });

    afterEach(function() {
        //在执行本区块的每个测试之后都执行
    });

    //测试用例

});
```

仅执行指定测试(.only) `describe.only` || `it.only`

忽略指定测试(.skip) `describe.skip` || `it.skip`


## 断言库Chaijs API

- The `Expect` / `Should` API covers the BDD assertion styles.
- The `Assert` API covers the TDD assertion style.

    expect和should都是BDD风格的，二者使用相同的链式语言来组织断言，但不同在于他们初始化断言的方式：expect使用构造函数来创建断言对象实例，而should通过为Object.prototype新增方法来实现断言（所以should不支持IE）；expect直接指向chai.expect，而should则是chai.should()。

    个人比较建议使用expect，should不仅不兼容IE，在某些情况下还需要改变断言方式来填坑。详细的比较可以看看官网 `http://chaijs.com/guide/styles/`，说的很清楚。

## 文档

- [chaijs api](http://chaijs.com/api/)
- [chaijs BDD API](http://chaijs.com/api/bdd/)