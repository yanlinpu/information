# No.1 深度优先搜索

## 模型
```
def dfs(step)
  #判断边界
  #尝试每一种可能
  for i in 1..9
    #递归继续下一步
    dfs(step+1)
  end
  #返回
  return
end
```
## demo1 奥数
```
=begin
口口口+口口口=口口口  
将数字1..9 分别填入口中 使等式成立     
173+286=459 286+173=459 是一个组合 所以最后除以2         
问共有多少种组合
=end
@total = 0
@a, @book = [], []                                                                                    
def dfs(step) #step 表示现在站在第几个盒子面前                                                        
  #如果站在第10个盒子面前，则表示前9个盒子已经放好扑克牌                                              
  if step == 10 
    #puts @a.to_s
    #判断是否满足等式 口口口+口口口=口口口                                                            
    if @a[1]*100 + @a[2]*10 + @a[3] + @a[4]*100 + @a[5]*10 + @a[6] == @a[7]*100 + @a[8]*10 +@a[9]     
      @total += 1
      puts "#{@a[1]}#{@a[2]}#{@a[3]}+#{@a[4]}#{@a[5]}#{@a[6]}=#{@a[7]}#{@a[8]}#{@a[9]}"               
    end
  end
  #此时站在第n个盒子面前
  #按照1,2,3...9的顺序一一尝试                                                                        
  for i in 1..9
    #puts "test #{i}"
    #puts "#{@book.to_s} ----"                                                                        
    #判断扑克牌i是否在手上 nil表示还在手上                                                            
    if @book[i].to_s == ""                                                                            
      # 将扑克牌i放入到第step个盒子中                                                                 
      @a[step] = i 
      @book[i] = 1 # 1 表示不在手上                                                                   
      #puts @book[i]
      #下个盒子递归                                                                                   
      dfs(step+1)                                                                                     
      # 一定要将刚才从尝试的扑克牌收回，才能进行下一次尝试                                            
      @book[i] = "" 
    end
  end
  return 
end
dfs(1)
puts @total/2
```
## demo2 迷宫
```
=begin
  1 2 3 4 
1 F   X
2 
3     X
4   X E
5       X

  1 2 3 4 
1 0 0 1 0
2 0 0 0 0
3 0 0 1 0
4 0 1 0 0
5 0 0 0 1
从F走到E 最短步数
=end
@end = [3, 4]
@x, @y, @min = 4, 5, 999999
#障碍物
@book = @obj = Array.new(6){Array.new(5, 0)}
@obj[3][1] = @obj[3][3] = @obj[2][4] = @obj[4][5] = 1
#puts @obj.to_s
#下/右/上/左
@next = [[0,1],[1,0],[0,-1],[-1,0]]
def dfs(x, y, step)
  #判断是否达到@end
  if x==@end.first && y==@end.last
    #更新最小值
    @min = step if step<@min
    return
  end

  #4种走法 上下左右
  for i in 0..3
    #计算下一步
    tx = x + @next[i].first
    ty = y + @next[i].last
    #判断是否越界
    if tx < 1 || tx > @x || ty < 1 || ty > @y 
      next
    end
    #判断是否是障碍物或者已经在路线中
    if @obj[tx][ty]==0 && @book[tx][ty]==0
      @book[tx][ty]=1
      dfs(tx, ty, step+1)
      @book[tx][ty] = 0
    end
  end
  return
end
dfs(1,1,0)
puts @min
```
# No.2 广(宽)度优先搜索

## 用队列来模拟这个过程
## demo3迷宫 同 demo2
```
@end = [3, 4]
@x, @y = 4, 5
@book = @obj = Array.new(6){Array.new(5, 0)}
#障碍物
@obj[3][1] = @obj[3][3] = @obj[2][4] = @obj[4][5] = 1
#puts @obj.to_s
#下/右/上/左
@next = [[0,1],[1,0],[0,-1],[-1,0]]
#x,y坐标, f父亲在队列中的标号, s步数
Struct.new("Note", :x, :y, :f, :s)
#初始化队列
head = tail = 1
que = []
flag = 0 # 表示没有达到目标
#入口坐标
que[tail] = Struct::Note.new(1,1,0,0)
#puts que
tail += 1
@book[1][1] = 1
while head < tail
  #4个方向
  for i in 0..3
    #计算下一个点坐标
    tx = que[head].x + @next[i][0]
    ty = que[head].y + @next[i][1]
    #判断是否越界
    if tx < 1 || tx > @x || ty < 1 || ty > @y 
      next
    end
    #判断是否是障碍物或者已经在路线中
    if @obj[tx][ty]==0 && @book[tx][ty]==0
      #把这个点标记为走过
      @book[tx][ty]=1
      #插入新的点到队列中
      que[tail]=Struct::Note.new(tx, ty, head, que[head].s+1)
      tail += 1
    end
    #判断是否达到@end
    if tx==@end.first && ty==@end.last
      flag = 1
      break
    end
  end
  break if flag == 1
  # head 出队列
  head += 1
end
tail.times do |i|
  next if i == 0
  puts "#{i}=========#{que[i]}"
end
puts que[tail-1].s
```
## demo4 宝岛探险
```
=begin 
0 表示海洋 1~9 表示陆地
求(6,8)所在岛的面积 
上下左右相连接的陆地视为同一岛屿
  1 2 3 4 5 6 7 8 9 10
1 1 2 1 0 0 0 0 0 2 3
2 3 0 2 0 1 2 1 0 1 2
3 4 0 1 0 1 2 3 2 0 1
4 3 2 0 0 0 1 2 4 0 0
5 0 0 0 0 0 0 1 5 3 0
6 0 1 2 1 0 1 5 4 3 0
7 0 1 2 3 1 3 6 2 1 0
8 0 0 3 4 8 9 7 5 0 0
9 0 0 0 3 7 8 6 0 1 2
0 0 0 0 0 0 0 0 0 1 0
=end
```
