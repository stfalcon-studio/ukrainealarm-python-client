## Описание
Скрипт для мониторинга и уведомления о воздушных тревогах

Источник данных https://api.ukrainealarm.com/

## Описание файла конфигурации config.yaml
Для запуска и конфигурирования необходим конфигурационный файл config.yaml
Описание параметров 

```yaml
# Ключ к апи 
# тип - строка
api_key: ХХХХХХХХХХХХХХХХХХХХХХХХХХХ 
# Ссыла на апи
# тип - строка  
url: https://api.ukrainealarm.com/api/v3
# Таймаут между запросами к АПИ
# тип - целове число в секундах
time_delay: 60
# Таймаут перед перезапуском программы при ошибке (например сети)
# тип - целове число в секундах
recovery_timeout: 60
# Имя файла для журнала
# тип - строка 
log: log.txt
# Уровель логирования, должен быть один из набора ["INFO", "DEBUG", "WARN", "CRITICAL"]
# тип строка
log_level: "INFO"
# Максимальный размер файла журнала
# тип - целое число
log_size_bytes: 5000000
# Максимальный количество сохраняемых файлов журнала
# тип - целое число
log_backup_count: 5
# ИД региона для мониторинга. Можно найти в regions.yaml (создается при первом запуске)
# тестовый регион = 0
# тип - целое число
region_id: 14
# Название магазина. Не используется
# тип - строка
store_name: ""
# Имя файла сертификата
# тип - строка
local_cert_name: ""
# Запускается ли скрипт не в сети компании
# тип - логический, по умолчанию False
use_local: False
# Имя службы проигрывания музыки еоторую необходимо остановить для проигрывания тревоги
# тип - строковый 
voice_service_name: VLC
# Режим позволяющий останавливать системную службу проигрывания музыки в магазине 
# тип - логический, по умолчанию False
stop_voice_service_mode: False
# Имя файла который проигрывается при обьявлении тревоги 
# тип - строка
start_alert_filename: female_air_on.wav
# Имя файла который проигрывается при отбое тревоги 
# тип - строка
finish_alert_filename: female_air_off.wav
# Старт с какого времени уведомления 
# тип - время
start_alerting: 7:00:00
# Старт до какого времени уведомления 
# тип - время
finish_alerting: 23:00:00
```

### Дополнительно

При первом запуске автоматически создатется файл regions.yaml - список регионов с их id. 
Если в конфиге не уканан регион будет использоваться регион 14 - Киевская область


Для работы не локально выставить параметр use_local равным False 

Для работы в тестовом режиме выставить regionId = 0. Cкрипт не обращается к АПИ, но каждые 5 запросов ставит/отменяет тревогу