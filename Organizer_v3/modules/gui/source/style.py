from ttkbootstrap import Style


LJF_BUTTON_LAYOUT = []


def style_init(name: str = '') -> None:
    """
        Ф-я для инициализации общих используемых стилей. 
        Вызывается после инициализации основного объекта ttkbootstrap.
    """

    style = Style()

    if name:
        style.theme_use(name)
    else:
        # Определение стиля для кнопки с выравниванием текста по левому краю.
        LJF_BUTTON_LAYOUT.extend(style.layout('TButton'))
        link = LJF_BUTTON_LAYOUT[0][1]['children'][0][1]['children'][0][1]['children'][0][1]
        link['sticky'] = 'ws'
    
    ljf_names = (
        'ljf.TButton',
        'ljf.danger.TButton',
        'ljf.warning.TButton',
        'ljf.Link.TButton',
        'ljf.secondary.Link.TButton'
    )

    for name in ljf_names:
        style.configure(name)
        style.layout(name, LJF_BUTTON_LAYOUT)
