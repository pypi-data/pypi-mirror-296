# v0.0.7

## Суулгах:

https://github.com/ganbaaelmer/pandas-fast-nested-looper.git

https://pypi.org/project/pandas-fast-nested-looper

эсвэл

```

pip install pandas-fast-nested-looper

```
## Тайлбар:

2 өөр pandas dataframe ийн тоон утгатай багануудын хооронд хийгддэг асар олон тооны давталттай for loop ээс үүсэх урт хугацааг numba ашиглан хэмнэх зорилготой хийсэн болно.

Numba ашигласнаар том хэмжээний for loop ийг гүйцэтгэх хурд нь numba тохиргоо болон cpu, gpu ашигласанаас хамаарч 110%-477%-р хурдасдаг.

Их хэмжээний дата дээр хийгдсэн for loop давталтуудын хугацааны ялгааг эндээс харна уу:

https://www.codearmo.com/python-tutorial/speed-looping-through-pandas-dataframe-numba

https://medium.com/@mflova/making-python-extremely-fast-with-numba-advanced-deep-dive-2-3-f809b43f8300

## Ашиглах заавар:

```

from pandas_fast_nested_looper import pandas_fast_nested_looper


file1_name = "your_file1.csv"

file2_name = "your_file2.csv"

file1_column_A = 'your_file1_column_A'

file1_column_B = 'your_file1_column_B'

file2_column_A = 'your_file2_column_A'

file2_new_column_name = "your_file2_new_column_name"

file2_column_B_list, file2_df = pandas_fast_nested_looper.pandas_fast_nested_looper(file1_name, file1_column_A, file1_column_B, file2_name, file2_column_A, file2_new_column_name)

```

## Үндсэн үйлдэлүүд:

#### option1:

```

for i in range(file2_column_A.shape[0]):

    for i in range(file1_column_A.shape[0])

        if file1_column_A[i] == file2_column_A[j]:

            file2_column_B_list[i] = file1_column_B[j]

        else:

            pass

```

#### option2:

    ...

## Үр дүн:

file2_column_B_list лист үүснэ

file2_df dataframe дотор таны өгсөн file2_new_column_name багана бүхий мэдээлэл үүснэ

df2_with_new_column.csv файл диск дээр үүснэ.

## Анхаарах зүйлс:

- numpy болон numba ашиглаж байгаа учир зөвхөн тоон утгатай багануудын хооронд үйлдэл хийдэг. 
