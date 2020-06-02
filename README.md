# music-dl
##### A youtube-dl spiritual sequel but it is just for music(music.163.com and y.qq.com)
P.S. 第一次发，代码写得有点乱，别介意 😱

## Features

  #####  下载网易云音乐单曲（不包括试听）
  #####  下载网易云音乐歌单（不包括试听）
  #####  下载QQ音乐单曲

## Description

```
#Main Arg, 主要参数：

#-i / --input URL input to download(the main arg), 下载文件的url

#Something not important, 不重要参数：

#-o / --output The download path(default is root dir), 下载路径（默认根目录）

#-ac / --AutoCreate Auto create the download path(default is True), 是否自动创建下载路径（默认是）

#-ar / --AutoReplace Auto Replace Illicit Characte, r Such as: \, /, :, *, ?, \", <, >, |, 自动替换非法字符，比如：\, /, :, *, ?, \", <, >, |
```

## Examples

#### some command line example
```bash
music-dl -i https://music.163.com/song?id=27588123

music-dl -i https://music.163.com/song?id=27588123 -o c:\music\

music-dl -i https://music.163.com/song?id=27588123 -o c:\music\ -ac

music-dl -i https://music.163.com/song?id=27588123 -o c:\music\ -ac -ar

```

## Build

#### Using python 3.x with pyinstaller
```
pyinstaller -F music-dl.py
```

## Using

#### [surmon](https://github.com/surmon-chinae "surmon")
#### [jsososo](https://github.com/jsososo "jsososo")

