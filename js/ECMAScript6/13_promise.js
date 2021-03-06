/**
 Promise对象有以下两个特点。

（1）对象的状态不受外界影响。
    Promise对象代表一个异步操作，有三种状态：Pending（进行中）、Resolved（已完成，又称 Fulfilled）和Rejected（已失败）。
    只有异步操作的结果，可以决定当前是哪一种状态，任何其他操作都无法改变这个状态。
    这也是Promise这个名字的由来，它的英语意思就是“承诺”，表示其他手段无法改变。

（2）一旦状态改变，就不会再变，任何时候都可以得到这个结果。
    Promise对象的状态改变，只有两种可能：从Pending变为Resolved和从Pending变为Rejected。
    只要这两种情况发生，状态就凝固了，不会再变了，会一直保持这个结果。
    如果改变已经发生了，你再对Promise对象添加回调函数，也会立即得到这个结果。
    这与事件（Event）完全不同，事件的特点是，如果你错过了它，再去监听，是得不到结果的。
 */
function timeout(ms){
    return new Promise((resolve, reject) => {
        setTimeout(resolve, ms, 'done');
    })
}
timeout(10000).then((value) => {
    console.log(value)
})