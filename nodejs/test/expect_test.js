/**
 * Chaijs Expect Chains
 */

 /**
  * Chains（语义链 ------- 仅为增强可读性, 无实际的断言功能）:
  *     to be been is that which and has have with at of same but does
  *     [ 'to', 'be', 'been', 'is', 'and', 'has', 'have', 'with', 'that', 'which', 'at', 'of', 'same' ].forEach(function (chain) {
  *         Assertion.addProperty(chain, function () {
  *             return this;
  *         });
  *     });
  */

// Flag 只为断言设置标识(Assertion的属性__flags)
"use strict"
var chai = require('chai');
var expect = chai.expect;

describe('BDD Expect', function() {
    it('should be passed all', function() {
        /**
         * .not
         *      设置取反标识: __flags.negate
         */
        expect(function () {}).to.not.throw();
        expect({a: 1}).to.not.have.property('b');
        expect([1, 2]).to.be.an('array').that.does.not.include(3);
        expect(2).to.equal(2); // Recommended
        // expect(2).to.equal('2'); // expected 2 to equal '2'
        expect(2).to.not.equal(1); // Not recommended
        /**
         * .deep
         *      设置deep标识: __flags.deep
         *      设置deep标记，然后使用equal, include, members, keys, 和property断言。
         *      该标记可以让其后的断言不是比较对象本身，而是递归比较对象的键值对
         */
        // Target object deeply (but not strictly) equals `{a: 1}`
        expect({a: 1}).to.deep.equal({a: 1});
        expect({a: 1}).to.not.equal({a: 1});

        // Target array deeply (but not strictly) includes `{a: 1}`
        expect([{a: 1}]).to.deep.include({a: 1});
        expect([{a: 1}]).to.not.include({a: 1});

        // Target object deeply (but not strictly) includes `x: {a: 1}`
        expect({x: {a: 1}}).to.deep.include({x: {a: 1}});
        expect({x: {a: 1}}).to.not.include({x: {a: 1}});

        // Target array deeply (but not strictly) has member `{a: 1}`
        expect([{a: 1}]).to.have.deep.members([{a: 1}]);
        expect([{a: 1}]).to.not.have.members([{a: 1}]);

        // Target set deeply (but not strictly) has key `{a: 1}`
        expect(new Set([{a: 1}])).to.have.deep.keys([{a: 1}]);
        expect(new Set([{a: 1}])).to.not.have.keys([{a: 1}]);

        // Target object deeply (but not strictly) has property `x: {a: 1}`
        expect({x: {a: 1}}).to.have.deep.property('x', {a: 1});
        expect({x: {a: 1}}).to.not.have.property('x', {a: 1});

        expect({ foo: { bar: { baz: 'quux'}}})
            .to.have.property('foo').to.have.property('bar').to.have.property('baz', 'quux');
        expect({"foo.bar": "baz"}).to.have.deep.property("foo.bar", "baz"); 

        /**
         * .nested
         *      Enables dot(.)- and bracket-notation in all .property and .include assertions that follow in the chain.
         */
        expect({ foo: { bar: { baz: 'quux'}}})
            .to.have.nested.property('foo.bar.baz', 'quux');
        expect({ foo: { bar: { baz: 'quux'}}})
            .to.have.nested.include({'foo.bar.baz': 'quux'});
        expect({'.a': {'[b]': 'x'}}).to.have.nested.property('\\.a.\\[b\\]');
        expect({'.a': {'[b]': 'x'}}).to.have.nested.property('\\.a.\\[b\\]', 'x');

        /**
         * .own
         *      Causes all .property and .include assertions that follow in the chain to ignore inherited properties.
         *      忽略继承的属性
         *      .own cannot be combined with .nested.
         */
        
        expect({a: 1}).to.have.own.property('a');
        // Object.prototype.b=2;
        // expect({a: 1}).to.have.property('b').but.not.own.property('b');

        /**
         * .orderd
         *      Causes all .members assertions that follow in the chain to require that members be in the same order.
         *      同样的排序
         */
        expect([1, 2, 3]).to.have.ordered.members([1, 2, 3])
            .but.not.have.ordered.members([2, 1]);
        // When .include and .ordered are combined, the ordering begins at the start of both arrays.
        expect([1, 2, 3]).to.include.ordered.members([1, 2])
            .but.not.include.ordered.members([2, 3]);

        /**
         * .any .all
         *      设置deep标识: __flags.any和__flags.all 同时设置, 互异影响的后续断言: keys
         */
        expect({a: 1, b: 2}).to.not.have.any.keys('c', 'd');
        expect({a: 1, b: 2}).to.have.all.keys('a', 'b');
        
        /**
         * .a/an(type[,msg])
         * .include(val[, msg])
         * .equal(val[, msg]) (===)
         * .eql(obj[, msg])
         *      Asserts that the target is deeply equal to the given obj
         */
        expect('foo').to.be.a('string');
        expect({a: 1}).to.be.an('object');
        expect(null).to.be.a('null');
        expect(undefined).to.be.an('undefined');
        expect(new Error).to.be.an('error');
        expect(Promise.resolve()).to.be.a('promise');
        expect(new Float32Array).to.be.a('float32array');
        expect(Symbol()).to.be.a('symbol');
        // It’s often best to use .a to check a target’s type before making more assertions on the same target.
        // That way, you avoid unexpected behavior from any assertion that does different things based on the target’s type.
        expect([]).to.be.an('array').that.is.empty;
        expect('foobar').to.not.include('taco');
        expect([1, 2, 3]).to.not.include(4);
        // Target object is deeply (but not strictly) equal to {a: 1}
        expect({a: 1}).to.eql({a: 1}).but.not.equal({a: 1});

        /**
         * .above(n[, msg])
         *      number or date > n
         * .least(n[, msg])
         *      number or date >= n
         * .below(n[, msg])
         *      number or date < n
         * .most(n[, msg])
         *      number or date <= n
         * .within(start, finish[, msg])
         *      >= start && <= finish
         * .closeTo(expected, delta[, msg])
         *      >= expect-delta <= expect+delta
         */
        expect('foo').to.have.lengthOf(3); // Recommended
        expect('foo').to.have.lengthOf.above(2); // Not recommended

        /**
         * .instanceof(constructor[, msg])
         */
        function Cat () { }
        expect(new Cat()).to.be.an.instanceof(Cat);
        expect([1, 2]).to.be.an.instanceof(Array);
        /**
         * .ok(==true) .true(===) .false(===) .null(===) .undefined(===) .NaN .exist(==null || undefined) 
         * .empty(target’s length property is strictly (===) equal to 0)
         * .members(set[, msg])
         * .arguments
         */
        expect(1).to.equal(1); // Recommended
        expect(1).to.be.ok; // Not recommended
        expect(true).to.be.true; // Recommended
        expect(true).to.be.ok; // Not recommended
        expect([1, 2, 3]).to.have.members([2, 1, 3]);
        //members are compared using strict (===) equality
        expect([{a: 1}]).to.have.deep.members([{a: 1}]);
        expect([{a: 1}]).to.not.have.members([{a: 1}]);
        /**
         * .property(name[, val[, msg]])
         */
        expect({a: 1}).to.have.property('a').that.is.a('number');
        /**
         * .ownPropertyDescriptor(name[, descriptor[, msg]])
         */
        expect({a: 1}).to.have.ownPropertyDescriptor('a', {
            configurable: true,
            enumerable: true,
            writable: true,
            value: 1,
        });
        /**
         * .lengthOf(n[, msg])
         * .match(re[, msg])
         * .string(str[, msg])
         * .keys(key1[, key2[, …]])
         * .oneOf(list[, msg])
         * .change(subject[, prop[, msg]])
         *      断言目标方法会改变指定对象的指定属性
         * .increase(subject[, prop[, msg]])
         *      断言目标方法会增加指定对象的属性
         * .decrease(subject[, prop[, msg]])
         *      断言目标方法会减少指定对象的属性
         * .by(delta[, msg])
         *      expect(addTwo).to.increase(myObj, 'val').by(2);
         */

        expect({a: 1, b: 2}).to.have.all.keys('a', 'b');
        expect(['x', 'y']).to.have.all.keys(0, 1);
        expect({a: 1, b: 2}).to.have.all.keys({a: 4, b: 5}); // ignore 4 and 5
        expect(['x', 'y']).to.have.all.keys({0: 4, 1: 5}); // ignore 4 and 5
        var myObj = {val: 1}
            , addTwo = function () { myObj.val += 2; };

        expect(addTwo).to.increase(myObj, 'val').by(2);
        /**
         * .throw([errorLike], [errMsgMatcher], [msg])
         */
        var err = new TypeError('Illegal salmon!');
        var badFn = function () { throw err; };
        expect(badFn).to.throw();
        expect(badFn).to.throw(TypeError);
        expect(badFn).to.throw(err);
        expect(badFn).to.throw(TypeError, 'salmon');
        expect(badFn).to.throw(TypeError, /salmon/);
        expect(badFn).to.throw(err, 'salmon');
        expect(badFn).to.throw(err, /salmon/);

        var goodFn = function () {};
        expect(goodFn).to.not.throw();
        /**
         * .respondTo(method[, msg])
         *      asserts that the target has a method with the given name method
         */
        /**
         * .itself
         *      + respondTo
         */
        /**
         * .satisfy(matcher[, msg])
         *      method：Function，测试器，接受一个参数表示目标值，返回一个布尔值。 
         *      断言目标值能够让给定的测试器返回真值
         */
        expect(1).to.satisfy(function(num) {
            return num > 0; 
        });

        /**
         * .extensible
         *      断言目标对象是可扩展的（可以添加新的属性）
         *      Object.preventExtensions({}), Object.seal({}), Object.freeze({});
         * .sealed
         *      断言目标对象是封闭的（无法添加新的属性并且存在的属性不能被删除但可以被修改）
         * .frozen
         *      断言目标对象是冻结的（无法添加新的属性并且存在的属性不能被删除和修改）
         * .finite
         *      Asserts that the target is a number, and isn’t NaN or positive/negative Infinity
         * .fail(actual, expected, [message], [operator])
         *      throw a failure.
         */
    });

});