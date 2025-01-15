from tabulate import tabulate

#Граматика
#Глагол biti
verb_biti_desk = "Глагол biti"
verb_biti_table = [
    ["Лицо", "ед.ч", "мн.ч"],
    ["1", "ја сам", "ми смо"],
    ["2", "ти си", "ви сте"],
    ["3", "он(она,оно) je", "они(оне,она) су"],
]
verb_biti_table_text = tabulate(verb_biti_table, headers="firstrow", tablefmt="grid", colalign=["center", "center", "center"])

rules_categories = {
    "Глагол biti": (verb_biti_desk, verb_biti_table_text)
}