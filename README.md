# Домашнее задание к занятию «Очереди RabbitMQ» - `Иванов Федор`

### Задание 1

Задание 1. Установка RabbitMQ
Используя Vagrant или VirtualBox, создайте виртуальную машину и установите RabbitMQ. Добавьте management plug-in и зайдите в веб-интерфейс.

1. Устанавливаем RabbitMQ скриншот 1
![Скриншот-1](https://github.com/zef33/DZ8.03/blob/main/img/скрин1.png)
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
![Скриншот-4](https://github.com/zef33/DZ8.03/blob/main/img/скрин4.png)
![Скриншот-5](https://github.com/zef33/DZ8.03/blob/main/img/скрин5.png)
![Скриншот-6](https://github.com/zef33/DZ8.03/blob/main/img/скрин6.png)
