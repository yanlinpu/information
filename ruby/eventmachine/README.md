异步 (async) 基本和并发 (concurrent) 一个意思, 但和并行 (parallel) 完全是两回事. eventmachine 和 nodejs 都是通过多进程实现并行, 通过异步 IO 实现并发的. 顺序不等于同步, 并发不等于并行.

