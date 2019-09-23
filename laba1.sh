#!/bin/bash
(echo "Название,Расширение,Размер,Время изменения,Длительность видео и аудио")>./files.xls
files()
{
	(
	for file in "$1"/*
	do
		ras=$(echo "$file"|rev|cut -f1 -d.|rev)
		if [[ ".$ras" == "$file" ]]; then
			ext='-'
		else
			ext=$ras
		fi
		path=$file
		name=$(echo "$path"|rev|cut -f1 -d /|rev)
		if [[ $ext == "mkv" || $ext == "mp4" ]]; then
			echo $name,$ext,$(stat --printf="%s,%z" "$path"),$(mediainfo "$path"|head -n7|tail -n1|cut -c44-)
		elif [[ $ext == "mp3" ]]; then
			echo $name,$ext,$(stat --printf="%s,%z" "$path"),$(mediainfo "$path"|head -n5|tail -n1|cut -c44-)
		elif [[ $ext == "avi" ]]; then
			echo $name,$ext,$(stat --printf="%s,%z" "$path"),$(mediainfo "$path"|head -n6|tail -n1|cut -c44-)
		elif [[ $name == "*" ]]; then
			continue
		elif [[ -d "$path" && $(echo "$path"|wc -l) -ne 0 ]]; then
			files "$path"
		else
			echo $name,$ext,$(stat --printf="%s,%z" "$path")
		fi
	done)>>./files.xls
}
files .
