```
> var a = {id: 1, name: 'zhangsan', age: 12}
undefined
> var b = {name: 'lisi', age: 20}
undefined
> Object.assign(a,b)
{ id: 1, name: 'lisi', age: 20 }
> a
{ id: 1, name: 'lisi', age: 20 }
> var c = {age: 25, friends: 'zhangsan'}
undefined
> Object.assign(a,c)
{ id: 1, name: 'lisi', age: 25, friends: 'zhangsan' }
> a
{ id: 1, name: 'lisi', age: 25, friends: 'zhangsan' }
```

https://stackoverflow.com/questions/171251/how-can-i-merge-properties-of-two-javascript-objects-dynamically
