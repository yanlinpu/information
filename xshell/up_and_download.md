## xshell 上传rz、下载文件sz

- sz中的s意为send（发送），告诉客户端，我（服务器）要发送文件 send to cilent，就等同于客户端在下载。

  - 下载一个文件 sz filename
  - 下载多个文件 sz filename1 filename2
  - 下载dir目录下的所有文件，不包含dir下的文件夹 sz dir/*
 
- rz中的r意为received（接收），告诉客户端，我（服务器）要接收文件 received by cilent，就等同于客户端在上传。
  - 输入rz回车后，会出现文件选择对话框，选择需要上传文件，一次可以指定多个文件，上传到服务器的路径为当前执行rz命令的目录。
  
#### [利用SecureCRT上传、下载文件（使用sz与rz命令），超实用！](http://blog.csdn.net/lioncode/article/details/7921525)
