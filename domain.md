# Spring 2024 Random Coffee

Структура абзацев:

Понятие на русском `Concept in English` Тип понятия
Описание понятия

Типы понятий:

| E | Entity | Сущность

Описывает понятие которое имеет идентичность и жизненный цикл (часто не описаный явно) |
| --- | --- | --- |
| T | Type | Тип, обычно str enum 

Определяет ограничения на значения, которые может принимать переменная величина. Описание понятия призвано явно описать что значит эта величина. |
| S | Service | Сервис

Описывает бизнес-логику |


### Организация `Organisation` E

Организация, в которой могут состоять сотрудники. Имеет

1. Название

### Человек `Person` E

1. ФИО
2. Город дислокации (необязательно)
3. Предпочтения по формату встречи (онлайн/оффлайн) (?)

### Сотрудник `Employee` E

Человек, который имеет должность в какой-либо организации.

1. Организация
2. Должность
3. Подразделение (необязательно)

Сотрудник может быть прикреплен сразу к нескольким организациям.

### Роль `Role` T

Роль (должность) человека *в нашем приложении*. Есть следующие роли

1. Сотрудник организации `Employee`
2. Администратор организации `Administrator`
3. Участник встречи `Meeting participant`

Определенная роль позволяет выполнять человеку определенный набор действий.

Замечательно, что бывают роли, которые позволяют человеку действия только в рамках другой сущности. Например, если человек является сотрудником организации А, это означает, что он может встречаться с сотрудниками из организации А.

Примеры из речи:

> Сотрудник организации А может назначать встречи в организации А.
> 

> Администратор организации А может просматривать статистику встреч пользователей из организации А.
> 

По умолчанию, все люди являются сотрудниками какой-либо организации. Однако если человека исключают из организации, он перестает им быть. Но роли участника встречи сохраняются.

### Должность `Organisation Post` T

Должность сотрудника в организации. Каждая организация имеет свой набор должностей.

### Подразделение организации `Organisation Unit` E

В подразделение входят сотрудники, которые занимаются задачами определенной направленности. Каждая организация имеет свой, уникальный набор подразделений.

### Встреча `Meeting` E

Встреча, которая планируется при помощи нашего приложения. Имеет

1. Состояние `Meeting State`. Определяет этап жизненного цикла.
2. Набор участников (два и более)
3. Обстоятельства встречи

За назначение встреч отвечает сервис метчинга.

### Обстоятельства встречи `Meeting circumstances` E

Конкретные обстоятельства при которых проходит встреча, которые определяются в ходе произвольного разговора участников встречи.

1. Место проведения
2. Дата и время проведения
3. Длительность

### Сервис мэтчинга `Matching service` S

Данный сервис ответственен за определение групп людей, которые должны встретится. Сервис может обрабатывать две ситуации

1. Нужно поделить по группам множество людей, которые должны встретится. Такой кейс обычно возникает при назначении встреч по расписанию.
2. Нужно найти пару человеку, который хочет встретится вне общего расписания. Выбор пары происходит только из таки-же людей.

Данный сервис должен работать с предпочтениями человека, побирая для него наиболее релевантные встречи. 

Первый вариант должен обрабатывать различные корнер кейсы, которые могут возникнуть в условиях второго варианта. Думаю, второй вариант можно свести к первому, так будет лучше. Например, сделать, чтобы все pending встречи каждый день проходили процесс метчинга между собой. Это позволит сделать подбор более точным, не сильно повлияв на сторонний пользовательский опыт.

### Мэтчинг группа `Matching group` E

Группа людей, которые ждут мэтчинга (присоединения к какой-то встрече).

### Сервис встреч `Meeting service` S

Данный сервис отвечает за логику создания встреч.

Встреча может быть создана двумя путями

1. По инициативе сотрудника
2. По расписанию

Во всех случаях собеседник выбирается случайно через сервис мэтчинга.

### Участник встречи `Meeting participant` E

Сотрудник в контексте участия в какой-либо встрече. Сущность пока не имеет особых свойств.

### Состояние встречи `Meeting state` T

Может иметь следующие значения

1. В ожидании `Pending`. У встречи определен только один участник. Ожидание второго участника.
2. Встреча отменена до создания `Stale`. Отмена встречи после безрезультатного ожидания второго участника.
3. Создана `Created`. Встреча считается созданной, когда встреча полностью создана, но в ней, не определены конкретные обстоятельства. Участники встречи должны лично договориться о месте и времени проведения встречи.
4. Запланирована `Planned`. Встреча считается запланированной сразу после начала.
5. Происходит `Occur`. Встреча происходит в данный момент.
6. Завершена `Completed`. Встреча успешно состоялась.
7. Отменена `Cancelled`. Встреча по какой-то причине была отменена.
8. Отклонена `Rejected`. Участники не смогли запланировать встречу.

```mermaid
stateDiagram-v2
	[*] --> Planned: Мэтч участников встречи
	Planned --> Scheduled: Определение точного времени и места
	Planned --> Rejected: Не договорились
	Scheduled --> Occur: Время встречи пришло
	Scheduled --> Cancelled: Планы поменялись
	Occur --> Completed: Встреча закончилась
	Occur --> Cancelled: Планы поменялись
	
```