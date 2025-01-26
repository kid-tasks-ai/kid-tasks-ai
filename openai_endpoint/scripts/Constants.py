'''
Excpected incoming data structure:
{
    "child_description": {
        "age": 8,
        "gender": "male" / "female",
        "interests": "interes description"
    },
    "tasks_description": {
        "chore_tasks": ["make the bed", "do dishes"],
        "creative_tasks": {
            "amount": 3,
            "topics": ["space advanture"]
        }
    }
}
'''

CHILD_DESCRIPTION = "child_description"
CHILD_AGE = "age"
CHILD_GENDER = "gender"
CHILD_GENDER_MALE = "male"
CHILD_GENDER_FEMALE = "female"
CHILD_INTERESTS = "interests"

TASKS_DESCRIPTION = "tasks_description"
CHORE_TASKS = "chore_tasks"
CREATIVE_TASKS = "creative_tasks"
CREATIVE_TASKS_NUMBER = "amount"
CREATIVE_TASKS_TOPICS = "topics"

DEFAULT_INVENTORY='игрушки, бумага и карандаши, клей карандаш, ножницы'

PROMPT_CHILD_DESCRIPTION = """
Создай список задач для {age} {gender}, который любит {interests}. У ребенка есть доступ к следующим материалам: {materials}.

"""
PROMPT_TASKS_DESCRIPTION_BEGINNING = """
Список должен включать:
"""
PROMPT_TASKS_DESCRIPTION_CHORE = """
{chore_number} задачь по дому, которые помогут развивать ответственность. Задачи должны быть из спика: {chore_activity}.
"""

PROMPT_TASKS_DESCRIPTION_CREATIVE = """
{creative_number} креативных заданий, связанных с темой {creative_topics}.
Задачи должны быть оформлены в виде увлекательного приключения или игры, чтобы мотивировать ребенка. Включи подсказки, поощрения и позитивные описания, которые подойдут для его возраста. Например, добавь фантастические или приключенческие элементы, такие как 'спасти лесных жителей', 'создать волшебный замок' или 'помочь роботу'.

"""

PROMPT_DIFFICULTY_EXAMPLES = """
Пример сложности задач для возрастной группы ребенка:
\"\"\"
{tasks_examples}
\"\"\"
"""


PROMPT_STRUCTURE = """
Сгенерированные задачи необходимо вернуть в виде json объект со следующей структурой:
{
    "tasks": [
        {
            "title": "название задания",
            "type": "chore" или "creative",
            "text": "текст задания"
        }, ...
    ]
}

Вот пример ответа:
{
    "tasks": [
        {
            "title": "👑 Миссия 1: Наведи порядок в своем королевстве!",
            "type": "chore",
            "text": "Рыцарь или Принцесса, твоя комната – это твое королевство. Помоги своим игрушечным подданным найти свои места. Сложи книги в замке знаний, а одежду отправь в хранилище волшебной ткани."
        },
        {
            "title": "Создай замок для фей",
            "type": "creative",
            "text": "Нарисуй или вырежь из бумаги свой волшебный замок. Укрась его блестящими звездами, окошками и волшебными воротами."
        }
    ]
}
"""

DIFFICULTY_6_8_GENERAL = """
Нарисовать свой дом мечты снаружи и изнутри.
Придумать супергероя и нарисовать его костюм и суперсилу.
Сделать открытку для друга или члена семьи.
Собрать простую фигуру из конструктора (например, башню, мост или машинку).
Придумать и нарисовать карту сокровищ, добавив спрятанные клады.
Слепить животное из пластилина или глины.
Создать простую мозаичную картину из цветной бумаги.
"""

DIFFICULTY_6_8_BOYS = """
Нарисовать и раскрасить космический корабль.
Построить гараж для игрушечных машинок.
Сложить из бумаги простую модель самолета и устроить соревнования.
Придумать и нарисовать своего робота.
Построить башню из кубиков, чтобы она выдержала небольшой груз.
"""

DIFFICULTY_6_8_GIRLS = """
Нарисовать и раскрасить модное платье для принцессы.
Сделать браслет или ожерелье из бусин или макарон.
Придумать и написать короткую сказку о дружбе.
Создать мини-альбом для фотографий из картона и бумаги.
Смастерить кукольную мебель из картона.
"""

DIFFICULTY_8_10_GENERAL = """
Нарисовать иллюстрацию к любимой сказке или книге.
Создать объемное дерево из цветной бумаги.
Написать рассказ о волшебном мире.
Придумать рецепт и "нарисовать" блюдо на бумаге.
Сделать бумажный фонарик и украсить его узорами.
Разработать приглашение на воображаемый праздник.
"""

DIFFICULTY_8_10_BOYS = """
Построить крепость из картонных коробок.
Создать модель ракеты или самолета из бумаги.
Нарисовать комикс о приключениях супергероя.
Сделать машинку из картонных рулонов и крышек от бутылок.
Написать сценарий для короткого мультфильма.
"""

DIFFICULTY_8_10_GIRLS = """
Сшить простую игрушку из ткани или фетра.
Нарисовать замок принцессы и придумать историю о нем.
Сделать объемную открытку с цветами.
Создать мини-аквариум с бумажными рыбками в коробке.
Написать письмо феям и украсить его блестками и рисунками.
"""

DIFFICULTY_10_12_GENERAL = """
Создать объемную модель города из бумаги или картона.
Нарисовать свою версию обложки для любимой книги.
Написать рассказ о том, как ты стал(а) ученым, изобретателем или путешественником.
Придумать и нарисовать рекламу необычного продукта.
Сделать рамку для фотографий из подручных материалов.
Смастерить фигуру животного оригами.
"""

DIFFICULTY_10_12_BOYS = """
Построить мост из дерева или картона и проверить, что он выдержит вес.
Разработать и нарисовать план космической базы.
Сделать модель машины или танка из бумаги.
Написать историю о путешествии на другую планету.
Построить работающую катапульту из палочек и резинок.
"""

DIFFICULTY_10_12_GIRLS = """
Придумать дизайн своей одежды и сделать "коллекцию".
Создать украшение для комнаты, например, гирлянду из бумаги.
Составить рассказ о путешествии в волшебное королевство.
Сделать коробочку для мелочей и украсить ее.
Создать красивую закладку для книги.
"""