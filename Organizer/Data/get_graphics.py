def __median(book_list):
    s_l = sorted(book_list)
    list_len = len(s_l)
    i_v = int(list_len / 2)
    if list_len % 2 == 0:
        if s_l[i_v - 1] == 0 and s_l[i_v] == 0:
            return 0
        else:
            return round((s_l[i_v - 1] + s_l[i_v]) / 2, 1)
    elif list_len % 2 != 0:
        return int(s_l[i_v])
    else:
        return int(s_l[0])


def show_graphics(day_dict_list):
    # Задаются размеры окна графика
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 7)
    # Получаем список дней для координаты Х
    day_list = [day for day in day_dict_list]
    prod_type_list = ('Фотокнига Стандарт', 'Фотокнига ЛЮКС', 'Фотокнига Flex Bind', 'Фотокнига Классик',
                      'Фотопланшет Стандарт', 'Layflat', 'Фотоальбом полиграфический', 'Фотоальбом PUR',
                      'Фотожурнал', 'Фотопапка', 'Фотопечать')
    # Получаем списки продуктов для координаты У
    for name in prod_type_list:
        if name in day_dict_list[day_list[0]]:
            book_list = [day_dict_list[day][name] for day in day_dict_list]
            m_v = int(sum(book_list) / len(book_list))
            med = __median(book_list)
            plt.plot(day_list, book_list, 'o-', label=f"{name} (μ = {m_v}, m = {med})")
    # Ветка суммарного количества
    summ_list = []
    # Перебирем циклом дни
    for day in day_dict_list:
        # С помощью генератора списка получаем список значений всех продуктов суммируем их и записываем по дням
        summ_list.append(sum([day_dict_list[day][name] for name in day_dict_list[day]]))
    plt.plot(day_list, summ_list, '--', color="#b3b3b3", label="Общее количество")
    # Ветка среднего значения
    mean_value = sum(summ_list) / len(summ_list)
    mean_list = [mean_value] * len(day_dict_list)
    plt.plot(day_list, mean_list, ':', color="#b3b3b3", label=f"μ за период: {int(mean_value)}")
    # Ветка медианы
    all_med = __median(summ_list)
    all_med_list = [all_med] * len(day_dict_list)
    plt.plot(day_list, all_med_list, ':', color="#b3b3b3", label=f"m за период: {all_med}")
    # Рисуем график
    plt.ylim(ymin=0)
    plt.xticks(rotation=90)
    plt.legend().set_draggable(True)
    plt.grid(True)
    plt.show()
