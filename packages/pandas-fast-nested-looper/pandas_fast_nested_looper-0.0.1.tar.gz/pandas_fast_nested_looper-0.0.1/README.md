## Суулгах:



https://github.com/ganbaaelmer/pandas-fast-nested-looper.git

эсвэл

```

pip install pandas-fast-nested-looper

```

## Ашиглах заавар:

```

from pandas-fast-nested-looper import pandas-fast-nested-looper

file1_name = "your_file1.csv"

file2_name = "your_file2.csv"

file1_column_A = 'your_file1_column_A'

file1_column_B = 'your_file1_column_B'

file2_column_A = 'your_file2_column_A'

file2_new_column_name = "your_file2_new_column_name"

file2_column_B_list, file2_df = pandas_fast_nested_looper.pandas_fast_nested_looper(file1_name,file1_column_A, file1_column_B, file2_name, file2_column_A, file2_new_column_name)

```

## Үр дүн:

file2_column_B_list лист үүснэ

file2_df dataframe дотор таны өгсөн file2_new_column_name багана бүхий мэдээлэл үүснэ

df2_with_new_column.csv файл дискэн дээр үүснэ.

## Тайлбар:

2 өөр pandas dataframe ийн тоон утгатай багануудын хооронд хийгддэг асар том for loop ээс үүсэх урт хугацааг numba ашиглан хэмнэх зорилготой хийсэн болно.

Numba ашигласнаар том хэмжээний for loop ийн хугацаа нь numba тохиргоо болон cpu, gpu ашигласанаас хамаарч 110-477%-р багасдаг.

Жишээ нь: Numba ашиглан 222,746,218,752 давталтыг 15 минутад хийж гүйцэтгэсэн. 247,495,798 it/s гэсэн үг юм.

Их хэмжээний дата дээр хийгдсэн for loop давталтуудын хугацааны ялгааг эндээс харна уу:

https://medium.com/@mflova/making-python-extremely-fast-with-numba-advanced-deep-dive-2-3-f809b43f8300


## Анхаарах зүйлс:

- numpy болон numba ашиглаж байгаа учир зөвхөн тоон утгатай багануудын хооронд үйлдэл хийдэг. 
