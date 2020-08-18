import autoit

title = 'MANDLOH'
print(autoit.win_get_title(title))
print(autoit.win_get_class_list(title))
#autoit.control_send(title, "RenderWindow1", "a")
#autoit.control_click(title, "RenderWindow1", x=683, y=76)