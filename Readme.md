# Barsxml библитека для фрмирования zip пакетов файлов xml

## Назначение

Библиотека предназначена для формирования фрйлов xml на основе правил ФФОМС (Федеральный фонд ОМС).
Записи в файлах включают в себя случаи оказания медпомощи по ОМС пациентам в МО на территории
Приморского края.

Каждый сфорированный файл подписывается КУЭП, и далее все файлы упаковываются в архив zip.

## Установка

Проект был задуман в виде дистрибутива устанавлмваемого с

[https://test.pypi.org/simple/](https://test.pypi.org/simple/)

или

[https://test.pypi.org/simple/](https://test.pypi.org/simple/)

В текущей версии библотеки, эта идея до конца не реализвана. Предлагается устанавливать биюлиотеку
в виртуальное окружение Python непосредственно из репозитория

[git@github.com:SLikhachev/barsxml.git](git@github.com:SLikhachev/barsxml.git)

Зависимости перечислены в файле `requirements.txt`.

После установки внешних зависимостей, необходимо установить в виртуальное окружение и саму
библиотеку (так, что после обновления основной ветки репозитория в текущий каталог, будут
доступны самые последние изменения в библотеке):

`pip install -e .`

## Тестирование

Тесты написаны для небольшого количества случаев использования библиотеки и находятся в каталоге

`./src/brasxml/tests/`

В этом же каталоге должен находится подкаталог `data/`. Этот подкаталог не должен индексироваться git.
В __data__ будут формироватся тестовые пакеты для проверки работосбособности кода.
Примеры конфигураций для различных источников данных для библиотеки приведены в какталоге __tests__.

Для текстирования используется библиотека __pytest__, так что, она должна быть установлена в виртуальное
окрузение.

Для запуска тестов рекомендуется в корне пректа создать файл

`pytest_YOUR_TESTS_NAME.ini`

где `YOUR_TESTS_NAME` строка описывающая ваш конкретный набор тестов и тестовое окружение.

В качестве шаблона можно использовать прилагаемый файл

`pytest_demo.ini`

Запуск тестов производится командой:

`(venv)> pytest -c pytest_demo.ini`

Для запуска только опреленной функции тестового файла можно использовать команду:

`(venv)> pytest -c pytest_demo.ini src/barsxml/tests/test_pg_app.py::test_app`

__За подробной документацией обращайтест к автору проекта по электропочте;__

[polaughing@yahoo.com](polaughing@yahoo.com)

[aughing@hotmail.com](aughing@hotmail.com)
