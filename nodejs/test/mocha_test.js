// 1. npm install -g mocha
// demo1. Synchronous 同步代码
var assert = require('assert'),
    chai = require('chai'),
    expect = chai.expect;
describe('DEMO1. Array', function() {
    describe('#indexOf()', function() {
        it('should return -1 when the value is not present', function() {
            // assert.equal (exp1, exp2) 断言判断exp1结果是否等于exp2, 这里采取的等于判断是== 而并非 === 。即 assert.equal(1, ‘1’) 认为是True。
            assert.equal(-1, [1,2,3].indexOf(4));
        });
    });
});

/**
 * demo2. Asynchronous 异步代码
 *      很简单，在你最深处的回调函数中加done()表示结束。
 *      按照瀑布流编程习惯，取名done是表示你回调的最深处，也就是结束写嵌套回调函数。
 *      但对于回调链来说done实际上意味着告诉mocha从此处开始测试，一层层回调回去。
 */
var fs = require('fs');  
describe('DEMO2. File', function(){  
    describe('#readFile()', function(){  
        it('should read test.ls without error', function(done){  
            fs.readFile('README.md', function(err){  
                if (err) throw err;  
                done();  
            });  
        })  
    })  
})  


/**
 * demo3. Pending
 *      即省去测试细节只保留函数体。
 *      一般适用情况比如负责测试框架的写好框架让组员去实现细节，或者测试细节尚未完全正确实现先注释以免影响全局测试情况。
 *      这种时候mocha会默认该测试pass。
 */

describe('DEMO3. Array', function(){  
    describe('#indexOf()', function(){  
        it('should return -1 when the value is not present')  
    })  
}); 

/**
 * demo4. Exclusive && Inclusive
 *      分别对应only和skip函数。
 */

describe('DEMO4. File', function(){  
    describe('#readFile()', function(){  
        it.skip('should read README.md without error', function(){  
            fs.readFile('README.md', function(err){  
                if (err) throw err;  
                done();  
            });  
        })  
        it('should read test.js without error')  
    })  
}) 

/**
 * demo5. hook(Before && After)
 */
  
  
describe('DEMO5. Array', function(){
    beforeEach(function(){
        console.log('beforeEach Array')
    })
    before(function(){
        console.log('before Array')
    })
    before(function(){
        console.log('before Array second time')
    })
    after(function(){
        console.log('after Array')
    })
    describe('#indexOf()', function(){
        it('should return -1 when the value is not present', function(){
            expect([1,2,3].indexOf(0)).to.be.equal(-1);
        })
        it('should return 1 when the value is not present')
    })
    describe('File', function(){
        beforeEach(function(){
            console.log('beforeEach file test!'); 
        })
        afterEach(function(){
            console.log('afterEach File test!')
        })
        describe('#readFile()', function(){
            it('should read README.md without error', function(done){
                fs.readFile('README.md', function(err){
                    if(err)
                        throw err
                    done()
                })
            })
            it('should read README.js without error', function(done){
                fs.readFile('README.md', function(err){
                    if(err)
                        throw err
                    done()
                })
            })
        })
    })
})