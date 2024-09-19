#include <Python.h>
#include <math.h>
#include <time.h>

// Функция для вычисления квадратного корня
static PyObject* sqrt_function(PyObject* self, PyObject* args) {
    double number;

    // Разбираем аргументы Python (ожидается один аргумент - число)
    if (!PyArg_ParseTuple(args, "d", &number)) {
        return NULL; // Возвращаем NULL, если аргумент неправильный
    }

    // Вычисляем квадратный корень
    double result = sqrt(number);

    // Возвращаем результат в виде объекта Python
    return PyFloat_FromDouble(result);
}

// Функция для получения текущей даты и времени
static PyObject* current_datetime(PyObject* self, PyObject* args) {
    // Получаем текущее время
    time_t now = time(NULL);
    struct tm* local = localtime(&now);

    // Форматируем дату и время
    char date_str[11];  // Дата в формате YYYY-MM-DD
    char time_str[9];   // Время в формате HH:MM:SS
    strftime(date_str, sizeof(date_str), "%Y-%m-%d", local);
    strftime(time_str, sizeof(time_str), "%H:%M:%S", local);

    // Создаем Python-словарь для возврата данных
    PyObject* result = PyDict_New();
    if (!result) {
        return NULL;
    }

    // Добавляем ключи "DATE" и "TIME" в словарь
    PyDict_SetItemString(result, "DATE", PyUnicode_FromString(date_str));
    PyDict_SetItemString(result, "TIME", PyUnicode_FromString(time_str));

    // Возвращаем словарь
    return result;
}

// Описание методов модуля
static PyMethodDef UtilMethods[] = {
    {"sqrt", sqrt_function, METH_VARARGS, "Compute the square root of a number."},
    {"current_datetime", current_datetime, METH_NOARGS, "Return the current date and time as a dictionary."},
    {NULL, NULL, 0, NULL}  // Завершающий элемент
};

// Описание самого модуля
static struct PyModuleDef utilmodule = {
    PyModuleDef_HEAD_INIT,
    "utilmodule",   // Имя модуля
    NULL,           // Документация модуля (можно оставить NULL)
    -1,             // Размер состояния, -1 для статических модулей
    UtilMethods     // Методы модуля
};

// Инициализация модуля
PyMODINIT_FUNC PyInit_utilmodule(void) {
    return PyModule_Create(&utilmodule);
}
