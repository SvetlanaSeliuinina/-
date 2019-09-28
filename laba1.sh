#!/bin/bash
#Запись названия столбцов в файл
(echo "Название,Расширение,Размер,Время изменения,Длительность видео и аудио")>./files.xls
#Создание функции
files()
{
	(
	#Проверка всех файлов из заданной директрории
	for file in "$1"/*
	do
		#Поиск расширения как текста после последней точки
		ras=$(echo "$file"|rev|cut -f1 -d.|rev)
		#Если расширения нет, в файл будет записано -
		if [[ ".$ras" == "$file" ]]; then
			ext='-'
		else
			ext=$ras
		fi
		path=$file
		#Выделение имени из пути к файлу
		name=$(echo "$path"|rev|cut -f1 -d /|rev)
		#Определение типа файла и подготовка информации к записи
		#Если файл является видео, то нужно определить его длину
		if [[ $ext == "mkv" || $ext == "mp4" ]]; then
			echo $name,$ext,$(stat --printf="%s,%z" "$path"),$(mediainfo "$path"|head -n7|tail -n1|cut -c44-)
		elif [[ $ext == "avi" ]]; then
			echo $name,$ext,$(stat --printf="%s,%z" "$path"),$(mediainfo "$path"|head -n6|tail -n1|cut -c44-)
		#И длину аудио файлов
		elif [[ $ext == "mp3" ]]; then
			echo $name,$ext,$(stat --printf="%s,%z" "$path"),$(mediainfo "$path"|head -n5|tail -n1|cut -c44-)
		elif [[ $name == "*" ]]; then
			continue
		#Если найдена не пустая директория функция вызывается и для нее
		elif [[ -d "$path" && $(echo "$path"|wc -l) -ne 0 ]]; then
			files "$path"
		#Все остальные файлы
		else
			echo $name,$ext,$(stat --printf="%s,%z" "$path")
		fi
	#Запись данных в файл
	done)>>./files.xls
}
#Вызов функции для текущей директории
files .
