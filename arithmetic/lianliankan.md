## 基本算法实现连连看
```
=begin                                                                                                                                                                                                       
0 代表是空的道路初始0代表边界
  0 1 2 3 4 5
0 0 0 0 0 0 0 
1 0 1 3 1 1 0
2 0 2 2 2 4 0
3 0 3 3 4 4 0
4 0 2 1 3 4 0
5 0 0 0 0 0 0
=end
# 初始化棋盘
@obj = Array.new(6){Array.new(6, 0)} 
@obj[1][1], @obj[1][2], @obj[1][3], @obj[1][4] = 1, 3, 1, 1
@obj[2][1], @obj[2][2], @obj[2][3], @obj[2][4] = 2, 2, 2, 4
@obj[3][1], @obj[3][2], @obj[3][3], @obj[3][4] = 3, 3, 4, 4
@obj[4][1], @obj[4][2], @obj[4][3], @obj[4][4] = 2, 1, 3, 4
# 打印键盘
def print_obj
  @obj.size.times do |i| 
    puts @obj[i].to_s
  end 
end

print_obj
puts "====================="
@lines, @rows = @obj.size, @obj.first.size
Struct.new("Note", :x, :y) 
# puts "输出第一个点的坐标用逗号隔开 如 1,1 "
# notes = gets.chomp.split(",").map(&:to_i)
# note1 = Struct::Note.new(notes[0], notes[1])
# puts "第#{note1.x+1}行, #{note1.y+1}列, 数字为#{@obj[note1.x][note1.y]}"
# puts "输出第二个点的坐标用逗号隔开 如 1,1 "
# notes = gets.chomp.split(",").map(&:to_i)
# note2 = Struct::Note.new(notes[0], notes[1])
# puts "第#{note2.x+1}行, #{note2.y+1}列, 数字为#{@obj[note2.x][note2.y]}"
#note1, note2 = [Struct::Note.new(3,2),Struct::Note.new(3,3)]
#第三行第1列和第2列
#note1, note2 = [Struct::Note.new(3,2),Struct::Note.new(3,1)]
#第3,4行 第4列
#note1, note2 = [Struct::Note.new(3,4),Struct::Note.new(4,4)]
note1, note2 = [Struct::Note.new(1,1),Struct::Note.new(1,3)]

def get_val(note)
  @obj[note.x][note.y]
end
# 是否可以直连
def match_block?(note1, note2)
  return false unless note1.x == note2.x || note1.y == note2.y
  # 水平
  if note1.x == note2.x
    min, max= [note1.y, note2.y].sort
    for i in (min+1)...max
      return false if @obj[note1.x][i] > 0
    end
  # 垂直
  else
    min, max= [note1.x, note2.x].sort
    for i in (min+1)...max
      return false if @obj[i][note1.y] > 0
    end
  end
  return true
end

# 一折连
def match_block_one?(note1, note2)
  # 以st1 st2为矩形对角 寻找矩形另外2点
  st1, st2 = [Struct::Note.new(note1.x, note2.y), Struct::Note.new(note2.x, note1.y)]
  # 矩形另外2点都不会空 则跳过这种情况
  v1, v2 = [get_val(st1), get_val(st2)]
  return false if v1 > 0 && v2 > 0
  puts v1, v2
  if v2 == 0
    puts st2, note1, note2
    puts  match_block?(st2, note1)
    puts  match_block?(st2, note2)
  end
  return true if v1==0 && match_block?(st1, note1) && match_block?(st1, note2)
  return true if v2==0 && match_block?(st2, note1) && match_block?(st2, note2)
  return false
end
# 两折连
# 判断图片A与图片B能否经过有两个转角的路径连通实质上可以转化为判断能否找到一个点C，
# 这个C点与A可以直线连通，且C与B可以通过有一个转角的路径连通。若能找到这样一个C点，
# 那么A与B就可以经过有两个转角的路径连通
def match_block_two?(note1, note2)
  # 上 
  for i in 0...note1.x
    note3 = Struct::Note.new(i, note1.y)
    puts note1
    puts note2
    puts note3
    puts match_block?(note1, note3)
    puts match_block_one?(note2, note3)
    return true if get_val(note3)==0 && match_block?(note1, note3) && match_block_one?(note2, note3)
  end
  # 下 
  for i in (note1.x+1)...@lines
    note3 = Struct::Note.new(i, note1.y)
    return true if get_val(note3)==0 && match_block?(note1, note3) && match_block_one?(note2, note3)
  end
  # 左 
  for i in 0...note1.y
    note3 = Struct::Note.new(note1.x, i)
    return true if get_val(note3)==0 && match_block?(note1, note3) && match_block_one?(note2, note3)
  end
  # 右
  for i in (note1.y+1)...@rows
    note3 = Struct::Note.new(note1.x, i)
    return true if get_val(note3)==0 && match_block?(note1, note3) && match_block_one?(note2, note3)
  end
  return false
end
unless @obj[note1.x][note1.y] == @obj[note2.x][note2.y]
  puts "两点值不一样"
  exit
end

able = match_block?(note1, note2) || match_block_one?(note1, note2) || match_block_two?(note1, note2)

if able
  @obj[note1.x][note1.y] = @obj[note2.x][note2.y] = 0 
  print_obj
end
```
## 广度优先搜索法实现连连看

[连连看f算法](http://blog.csdn.net/whatday/article/details/8988932)
