# Домашнее задание к занятию «GitLab» - `Иванов Федор`


### Инструкция по выполнению домашнего задания

   1. Сделайте `fork` данного репозитория к себе в Github и переименуйте его по названию или номеру занятия, например, https://github.com/имя-вашего-репозитория/git-hw или  https://github.com/имя-вашего-репозитория/7-1-ansible-hw).
   2. Выполните клонирование данного репозитория к себе на ПК с помощью команды `git clone`.
   3. Выполните домашнее задание и заполните у себя локально этот файл README.md:
      - впишите вверху название занятия и вашу фамилию и имя
      - в каждом задании добавьте решение в требуемом виде (текст/код/скриншоты/ссылка)
      - для корректного добавления скриншотов воспользуйтесь [инструкцией "Как вставить скриншот в шаблон с решением](https://github.com/netology-code/sys-pattern-homework/blob/main/screen-instruction.md)
      - при оформлении используйте возможности языка разметки md (коротко об этом можно посмотреть в [инструкции  по MarkDown](https://github.com/netology-code/sys-pattern-homework/blob/main/md-instruction.md))
   4. После завершения работы над домашним заданием сделайте коммит (`git commit -m "comment"`) и отправьте его на Github (`git push origin`);
   5. В личном кабинете прикрепите и отправьте ссылку на решение в виде md-файла в вашем Github.
   6. Любые вопросы по выполнению заданий спрашивайте в разделе “Вопросы по заданию” в личном кабинете.
   
Желаем успехов в выполнении домашнего задания!
   
### Дополнительные материалы, которые могут быть полезны для выполнения задания

1. [Руководство по оформлению Markdown файлов](https://gist.github.com/Jekins/2bf2d0638163f1294637#Code)

---

### Задание 1

Разверните GitLab локально, используя Vagrantfile и инструкцию, описанные в этом репозитории.
Создайте новый проект и пустой репозиторий в нём.
Зарегистрируйте gitlab-runner для этого проекта и запустите его в режиме Docker. Раннер можно регистрировать и запускать на той же виртуальной машине, на которой запущен GitLab.

`Приведите ответ в свободной форме........`

1. `запускаем vagrant и разворачиваем GitLab`
2. `Создаем новый проект projekt8.03, скриншот 1`
3. `Регистрируем gitlab-runner скриншот 2 и 3`


![Скриншот-1](https://github.com/zef33/DZ8.03/tree/8336521078ee1c60f45a5a50dcc756acdbcbef5f/img/скрин1.png)
![Скриншот-2](https://github.com/zef33/DZ8.03/tree/8336521078ee1c60f45a5a50dcc756acdbcbef5f/img/скрин2.png)
![Скриншот-3](https://github.com/zef33/DZ8.03/tree/8336521078ee1c60f45a5a50dcc756acdbcbef5f/img/скрин3.png)


---

### Задание 2
Что нужно сделать:

Запушьте репозиторий на GitLab, изменив origin. Это изучалось на занятии по Git.
Создайте .gitlab-ci.yml, описав в нём все необходимые, на ваш взгляд, этапы.

1. Создаем в проекте projekt8.03 .gitlab-ci.yml
2. Запускаем задачи и проверяем работоспо собность

```
Поле для вставки кода...
stages:
  - test
  - build

test:
  stage: test
  image: golang:1.17
  script: 
   - go test .
  tags:
     - netology

static-analysis:
 stage: test
 image:
  name: sonarsource/sonar-scanner-cli
  entrypoint: [""]
 variables:
 script:
  - sonar-scanner -Dsonar.projectKey=netology -Dsonar.sources=. -Dsonar.host.url=http://gitlab.localdomain:9000 -Dsonar.login=sqp_9f0ab50a2ed92fa6e6af66061be9612ba57ed3f9
 tags:
     - netology

build:
  stage: build
  image: docker:latest
  script:
   - docker build .
  

build:
  stage: build
  image: docker:latest
  script:
   - docker build .
  tags:
      - netology

```
![Скриншот-4](https://github.com/zef33/DZ8.03/tree/8336521078ee1c60f45a5a50dcc756acdbcbef5f/img/скрин4.png)
![Скриншот-5](https://github.com/zef33/DZ8.03/tree/8336521078ee1c60f45a5a50dcc756acdbcbef5f/img/скрин5.png)
![Скриншот-6](https://github.com/zef33/DZ8.03/tree/8336521078ee1c60f45a5a50dcc756acdbcbef5f/img/скрин6.png)
