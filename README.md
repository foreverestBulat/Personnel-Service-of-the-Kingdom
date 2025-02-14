# Реализация

## App
Модели: User, Subject, King, Kingdom, TestCase, Question, CandidateTestTrial, Notification
- У `User` две роли, которые определяются через проверку user.king is not None то King иначе Subject. Связаны через ForeignKey. Есть related поле `notfications` - уведомления
- `Subject` - подданный, связан с королем (один ко многим, у короля много подданных, у подданного один король) и с королевством (тоже один ко многим)
- `King` - король, related поле `subjects`, ограничение сделано с помощью триггера (вторая миграция 0002_add_trigger)
- `Kingdom` сделано все как в тз
- `TestCase` - нужен для хранения ответов кандидатов на вопросы, которые хранятся в поле `answers` типа JSON, есть поле `status`, который отображает решал или не решал кандидат. После первой же отправки, снова решить тест не получится.
- `Question` - поля: `text` - текст вопроса, `answer_options` - варианты ответа, также хранит верные ответы: пример `answer_options`:
```
{
    "answer_options": {
        "1": "Эддард Старк", 
        "2": "Джон Сноу", 
        "3": "Роберт Баратеон", 
        "4": "Дейенерис Таргариен"
    }, 
    "correct_answers": [1]
}
```
- `CandidateTestTrial` - поля `name_test`, `kingdom_code`, `kingdom` и `questions`. Поле `questins` через ManyToMany, чтобы был больше выбор вопросов (даже те которые уже используются другими королевствами)
- `Notification` - уведомления, `user` - кому, `message` - сообщение, `read` - прочитано или нет, `created_at` - когда создано

## Database
Используется PostgreSQL

## Docker
Есть два контейнера: приложение и база данных
Для базы данных сделал тестовые данные в команде create_data (app/management/commands/create_data.py)
Есть суперпользователь:
```
username = admin
password = admin
```